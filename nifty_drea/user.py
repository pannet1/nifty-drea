from toolkit.fileutils import Fileutils
from omspy_brokers.angel_one import AngelOne
from requests import get
import json


class User(object):

    def __init__(self, **kw):
        self._userid = kw['user_id']
        self._password = kw['password']
        self._totp = kw['totp']
        self._api_key = kw['api_key']
        self._multiplier = kw['multiplier']
        self._max_loss: float = abs(kw['max_loss'])
        self._target: float = abs(kw['target'])
        self._disabled = True

    def auth(self):
        self._broker = AngelOne(user_id=self._userid,
                                api_key=self._api_key,
                                totp=self._totp,
                                password=self._password)
        if self._broker.authenticate():
            self._disabled = False
        else:
            print(vars(self))

    def ltp(self, **kwargs):
        return self._broker.obj.ltpData(
            kwargs['exchange'], kwargs['symbol'], kwargs['token'])

    def get_symbols(self, search, dumpfile):
        retn = '0'
        f = open(dumpfile)
        data = json.load(f)
        lenh = len(search)
        for i in data:
            if i['symbol'][:lenh] == search:
                print(i)
                retn = i.get('token', '0')
                break
        f.close()
        return retn

    def get_token(self, search, dumpfile):
        retn = '0'
        f = open(dumpfile)
        data = json.load(f)
        for i in data:
            if i['symbol'] == search:
                retn = i['token']
                break
        f.close()
        return retn

    def place_order(self, kwargs):
        params = {
            "variety": kwargs["variety"],
            "symbol": kwargs["symbol"],
            "token": kwargs["token"],
            "side": kwargs["side"],
            "exchange": kwargs["exchange"],
            "order_type": kwargs["order_type"],
            "product": kwargs["product"],
            "duration": 'DAY',
            "price": kwargs.get('price', 0),
            "quantity": kwargs["quantity"]
        }
        params['trigger_price'] = kwargs.get('trigger_price', '0')
        print(params)
        return self._broker.order_place(**params)

    def contracts(self, dumpfile):
        headers = {
            "Host": "angelbroking.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        resp = get(url, headers=headers)
        with open(dumpfile, "w") as json_file:
            json_file.write(resp.text)


if __name__ == "__main__":
    futil = Fileutils()
    users = futil.xls_to_dict("../../../users_ao.xls")
    for u in users:
        au = User(**u)
        au.auth()
        if not au._disabled:
            print(au)
