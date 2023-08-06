import requests
import time
import json
import re
import lyberry_api.channel
import lyberry_api.pub
import lyberry_api.account

class LBRY_Api():
    ONLINE = 0
    OFFLINE = 1
    INITIALISING = 2
    def __init__(self,
            comment_api = 'https://comments.odysee.com/api/v2',
            lbrynet_api = 'http://localhost:5279'
            ):
        self.comment_api = comment_api
        self.lbrynet_api = lbrynet_api

    def connect(self, dur = 10):
        print('connecting to lbrynet')
        attempts = 0
        while attempts < dur:
            try:
                status = self.request("status")
            except ConnectionError:
                yield 1
                attempts += 1
                time.sleep(1)
                continue
            if status['is_running'] if 'is_running' in status else False:
                yield 0
            yield 2
            time.sleep(1)
        raise ConnectionError('Could not connect to lbrynet')

    def initialising(self):
        try:
            status = self.request("status")
        except ConnectionError:
            return False
        if status['is_running'] if 'is_running' in status else False:
            return False
        return True

    def online(self):
        try:
            status = self.request("status")
            return status[ 'is_running' ]
        except:
            return False

    def request(self, method, params = {}):
        try:
            res = requests.post(self.lbrynet_api, json={"method": method, "params": params})
        except requests.exceptions.ConnectionError:
            raise ConnectionError('cannot reach lbrynet')
        if not res.ok:
            raise ConnectionError(res.text)
        res_data = res.json()
        if not 'result' in res_data:
            raise ValueError('LBRYnet returned no result')
        return res_data['result']

    def channels_feed_raw(self, ids, page = 1, page_size = 20):
        return self.request('claim_search', {
            "page": page,
            "page_size": page_size,
            "order_by": "release_time",
            "channel_ids": ids
        })

    def id_from_url(self, lbry_url):
        match = re.match(r'lbry://@.*?[:#]([a-f0-9]*)$', lbry_url);
        if match == None:
            raise ValueError(f'could not find id in lbry url: {lbry_url}')
        return match.group(1)

    def get(self, uri):
        if type(uri) != str:
            raise TypeError('Tried to get a URI that was not a string')
        return self.request('get', {'uri': uri})

    def resolve_raw(self, uri):
        res = self.request('resolve', {'urls': uri})[uri]
        if 'error' in res:
            error = res['error']
            raise ValueError(f"lbrynet returned an error:\n{error}")
        return res

    @property
    def subs_urls(self):
        prefs = self.get_shared_prefs()
        if not 'value' in prefs or not 'subscriptions' in prefs['value']:
            self.init_pref()
            prefs = self.get_shared_prefs()
        val = prefs['value']['subscriptions']
        return val

    def add_sub_url(self, url):
        url_id = self.id_from_url(url)
        subs_urls = self.subs_urls
        if not url in subs_urls:
            subs_urls.append(url)
            self.set_subs(subs_urls)

    def set_subs(self, subs_list):
        self.set_pref('shared', {'value': {'subscriptions': subs_list}})

    def get_shared_prefs(self):
        prefs_raw = self.prefs
        if not 'shared' in prefs_raw:
            self.init_pref()
            prefs_raw = self.prefs
        return prefs_raw['shared']

    @property
    def prefs(self):
        return self.request('preference_get')

    def init_pref(self):
        self.set_subs([])

    def set_pref(self, key, value):
        self.request('preference_set', {'key':key, 'value':value})

    @property
    def subs_ids(self):
        return [self.id_from_url(url) for url in self.subs_urls]

    @property
    def sub_feed(self, page_size = 20):
        return self.channels_feed(self.subs_ids, page_size)

    def channels_feed(self, ids, page_size = 20):
        page = 1
        while True:
            latest_raw = self.channels_feed_raw(ids, page, page_size)
            if len(latest_raw['items']) == 0:
                break
            for item in latest_raw['items']:
                yield lyberry_api.pub.LBRY_Pub(item, self)
            page += 1

    def list_comments(self, claim, parent = None, page = 1, page_size = 20, sort_by = 3):
        params = {
            "claim_id": claim.id,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "top_level": True,
        }
        if parent:
            params["parent_id"] = parent.id
            params["top_level"] = False

        res = requests.post(
            self.comment_api,
            json={
                "method": "comment.List",
                "id": 1,
                "jsonrpc":"2.0",
                "params": params
            }
        ).json()
        return res['result']

    def sign(self, channel, string):
        data = string.encode('utf-8')
        return self.request("channel_sign", {
            "channel_name": channel.name, 
            "hexdata": data.hex(),
            })

    def make_comment(self, commenter, comment, claim, parent = None):
        params = {
            "channel_id": commenter.id,
            "channel_name": commenter.name,
            "claim_id": claim.id,
            "comment": comment,
        }
        params.update(self.sign(commenter, comment))

        if parent:
            params["parent_id"] = parent.id

        try:
            res = requests.post(self.comment_api, json={"method": "comment.Create", "id": 1, "jsonrpc":"2.0", "params": params}).json()
            return res['result']
        except:
            raise Exception(res)

    def channel_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        if 'error' in raw_claim:
            error = raw_claim['error']
            print(f"lbrynet returned an error:\n{error['name']}: {error['text']}")
            return lyberry_api.channel.LBRY_Channel_Err()
        else:
            channel = lyberry_api.channel.LBRY_Channel(raw_claim, self)
            return channel

    def pub_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        return lyberry_api.pub.LBRY_Pub(raw_claim, self)

    def resolve(self, uri):
        raw_claim = self.resolve_raw(uri)
        if raw_claim['value_type'] == 'channel':
            return lyberry_api.channel.LBRY_Channel(raw_claim, self)
        elif raw_claim['value_type'] == 'stream':
            return lyberry_api.pub.LBRY_Pub(raw_claim, self)

    @property
    def my_channels(self):
        raw_channels = self.request("channel_list")["items"]
        channels = []
        for raw_channel in raw_channels:
            channels.append(lyberry_api.channel.LBRY_Channel(raw_channel, self))
        return list(channels)

    def create_account(self):
        pass

    def add_account(self, name, priv_key):
        raw_account = self.request('account_add', {
            "account_name": name,
            "private_key": priv_key})

        return lyberry_api.account.LBRY_Account(raw_account, self)

    def remove_account(self, account_id):
        self.request('account_remove', {'account_id': account_id})

    @property
    def accounts(self):
        raw_account_list = self.request('account_list')['items']
        account_list = [lyberry_api.account.LBRY_Account(account_raw, self) for account_raw in raw_account_list]
        return account_list

    def set_default_account(self, account_id):
        self.request('account_set', {'account_id': account_id,
            'default': True})

    @property
    def default_account(self):
        accounts = self.accounts
        for account in accounts:
            if account.is_default:
                return account
        raise Exception('No default account')
