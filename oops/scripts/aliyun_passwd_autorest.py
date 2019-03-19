#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings
settings.SECRET_KEY

client = AcsClient('<accessKeyId>', '<accessSecret>', 'default')


request = CommonRequest()
request.set_accept_format('json')
request.set_domain('ram.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2015-05-01')
request.set_action_name('UpdateLoginProfile')

request.add_query_param('UserName', 'qcs_backend')
request.add_query_param('Password', 'Abcd1234!')

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding = 'utf-8'))