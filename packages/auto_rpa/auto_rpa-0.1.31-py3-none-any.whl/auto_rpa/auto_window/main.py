import warnings
import requests
from .client import Client
import argparse
from datetime import datetime as dt
import os

warnings.filterwarnings('ignore')

class Main():

    def __init__(self, actuator=None):

        self.conf = {}
        self.actuator = actuator

    def get_acc_conf_from_req(self,account_id):

        res = requests.get('http://192.168.1.68:40088/api/account/list')
        account_infos = res.json()['Data']
        account_info = None
        for ac in account_infos:
            if ac['accountId'] == str(account_id):
                account_info = ac
                break
        if account_info is None:
            raise Exception('找不到账户信息')

        return account_info

    def set_account_conf(self, account):

        self.conf['account_conf'] = self.get_acc_conf_from_req(account)

    def set_base_conf(self):

        self.conf['base_conf'] = {}

    def set_oprate_conf(self):

        self.conf['oprate_conf'] = {}

    def set_date(self,_date=None):

        if _date is None:
            self.conf['_date'] = dt.now().strftime('%Y%m%d')
        self.conf['_date'] = _date

    def set_conf(self,account,_date=None):

        self.set_account_conf(account)
        self.set_base_conf()
        self.set_oprate_conf()
        self.set_date(_date)

    def set_pid(self):

        pid = os.getpid()
        with open('./pid.txt','w+') as f:
            f.write(str(pid))

    def kill_proc_by_pid(self):

        with open('./pid.txt', 'w+') as f:
            pid = f.read()
            if pid != '':
                pid = int(pid)
                os.popen('taskkill -f -pid {}'.format(pid))

    def run(self, account, _date=None, step_name=None, oprate='start'):

        self.set_conf(account,_date)
        actuator = self.actuator(self.conf)
        if oprate == 'start':
            # self.set_pid()
            actuator.run(step_name)
        elif oprate == 'stop':
            Client.close_client(actuator.config.client_path)
        # try:
        #     self.kill_proc_by_pid()
        # except:
        #     pass

    def run_by_args(self):

        parser = argparse.ArgumentParser(description='手动执行脚本')
        parser.add_argument('-a', '--account', type=str, default=None, help='账号id',
                            required=False, metavar='')
        parser.add_argument('-d', '--_date', type=str, default=None, help='日期,默认为当天', required=False,
                            metavar='')
        parser.add_argument('-s', '--step_name', type=str, default=None, help='步骤名称，默认执行所有步骤', required=False,
                            metavar='')
        parser.add_argument('-o', '--oprate', type=str, default='start', help='start,stop', required=False, metavar='')
        args = parser.parse_args()
        account = args.account
        _date = args._date
        step_name = args.step_name
        oprate = args.oprate
        if account is None or account == '':
            raise Exception('缺少账号参数')
        self.run(account, _date=_date, step_name=step_name, oprate=oprate)

if __name__ == '__main__':
    Main().run_by_args()






