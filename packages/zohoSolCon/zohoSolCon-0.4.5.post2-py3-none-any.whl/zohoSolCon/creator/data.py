import requests
import json
import csv
from datetime import datetime
import os


def make_header(token, environment="development"):
    return {
        'Authorization': f'Zoho-oauthtoken {token.access}',
        'environment': environment
    }


class DataOperations:
    def __init__(self, token, environment, account_link_name, app_link_name, form_link_name):
        self.token = token
        self.environment = environment
        self.account_name = account_link_name
        self.app_name = app_link_name
        self.form_name = form_link_name
        self.result = None
        self.last_operation = None
        

    def add_record(self, data_object):
        url = f'https://creator.zoho.com/api/v2/{self.account_name}/{self.app_name}/form/{self.form_name}'
        headers = make_header(token, environment=self.environment)
        data = json.dumps(data_object).encode('utf-8')

        self.response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 401:
            self.token.generate()
            self.add_record(data_object)
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.result = content['result'][0]


    def add_records(self, data_object_list):
        url = 
                                 
