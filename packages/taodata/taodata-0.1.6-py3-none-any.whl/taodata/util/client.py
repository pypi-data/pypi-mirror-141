# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from functools import partial
import json
import requests


class DataApi:

    __token = ''
    __http_url = 'http://210.22.185.58:7788/route'
    #__http_url = 'http://localhost:5000'

    def __init__(self, token, timeout=30):
        """
        Parameters
        ----------
        token: str
            API接口TOKEN，用于用户认证
        """
        self.__token = token
        self.__timeout = timeout

    def query(self, api_name, fields=[], **kwargs):
        req_params = {
            'api_name': api_name,
            'token': self.__token,
            'params': kwargs,
            'fields': fields
        }

        #print('request -->',req_params)
        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        #print('response-->',res.text)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            return data
        else:
            return None

    def __getattr__(self, name):
        return partial(self.query, name)

