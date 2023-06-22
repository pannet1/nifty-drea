from toolkit.logger import Logger
from toolkit.fileutils import Fileutils
from user import User
from time import sleep

filename = 'users_ao.xls'
sec_dir = "../../../"
dumpfile = sec_dir + "symbols.json"
missing = {"NIFTY": 26000, "BANKNIFTY": 26009}
logging = Logger(20, sec_dir + "drea-nifty.log")  # 2nd param 'logfile.log'
futl = Fileutils()


def load_all_users(fpath=sec_dir + filename):
    lst_truth = [True, 'y', 'Y', 'Yes', 'yes', 'YES']
    users = futl.xls_to_dict(fpath)
    obj_ldr, objs_usr = None, {}
    for u in users:
        is_disabled = u.get('disabled', False)
        if is_disabled not in lst_truth:
            au = User(**u)
            au.auth()
            if not au._disabled:
                if obj_ldr:
                    objs_usr[au._userid] = au
                else:
                    obj_ldr = au
    return obj_ldr, objs_usr


def replace_key(fm_key, to_key, dct_keys):
    if dct_keys.get(fm_key, False):
        dct_keys[to_key] = dct_keys[fm_key]
        dct_keys.pop(fm_key)
    return dct_keys


SET = futl.get_lst_fm_yml(sec_dir + "drea-nifty.yaml")
# get leader and followers instance
obj_ldr, objs_usr = load_all_users()
if futl.is_file_not_2day(dumpfile):
    obj_ldr.contracts(dumpfile)

search = "NIFTY"
resp = obj_ldr.get_token(search, dumpfile)
print(f"token: {resp}")
dct_base = {
    "exchange": "NSE",
    "symbol": search,
    "token": 26009}
resp = obj_ldr.ltp(**dct_base)
while True:
    try:
        print(resp)
    except Exception as e:
        print(f"error {e} in the main loop")
        continue
    finally:
        sleep(1)
