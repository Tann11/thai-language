#!/usr/bin/python
# -*- coding: cp1251 -*-

import sys
import urllib2
from copy import copy
from robotparser import RobotFileParser

'''
����� ����� ������������� �������

������ ������:
http://www.mcu.ac.th/site/articlecontent.php
'''

__author__ = 'Gree-gorey'

# ������������ �� ���������
# TODO: ������� � ���������������� ����
TIMEOUT = 5 # ������������ ����� �������� ������ � ��������

# HTTP-���������, ������� ������������ �� ��������� � ����� ����
# �������������� � ������������ UserAgent
DEFAULT_HEADERS = {
'Accept'           : 'text/html, text/plain',
'Accept-Charset'   : 'windows-1251, koi8-r, UTF-8, iso-8859-1, US-ASCII',
'Content-Language' : 'ru,en',
}
# ��� ��� HTTP-��������� 'User-Agent' � �������� robots.txt
DEFAULT_AGENTNAME = 'Test/1.0'
# email ������; ��� ������ �������� �� ������������
DEFAULT_EMAIL = ''


class RobotsHTTPHandler(urllib2.HTTPHandler):
    """
    �����, ������� ���������� ������������������� ����������
    OpenDirector.
    ������, ��� ���������� ������, ���������, ��� �� �������
    �� ��������� ������� ������ robots.txt.

    ���������:
    agentname -- ��� ��������
    """
    # TODO: ���������� ���� ��� ���������� ������, ����� ��� ���������
    #       �������� � ������ ����� �� ������ ������ ��������.
    def __init__(self, agentname, *args, **kwargs):
     urllib2.HTTPHandler.__init__(self, *args, **kwargs)
     self.agentname = agentname

def http_open(self, request):
     """
     ���������� ������������� ������. ���� � ����� �������
     ������� robots.txt c �������� �� ��������� ���������
     �������, ������������ ���������� RuntimeError.

     request -- ��������� urllib2.Request
     """
     url = request.get_full_url()
     host = urlsplit(url)[1]
     robots_url = urlunsplit(('http', host, '/robots.txt', '', ''))
     rp = RobotFileParser(robots_url)
     rp.read()
     if not rp.can_fetch(self.agentname, url):
         # ���������
         raise RuntimeError('Forbidden by robots.txt')
     # �� ���������, �������� �������
     return urllib2.HTTPHandler.http_open(self, request)

class UserAgent(object):
    """
    �������.

    ����������� ��������� ������������ � �������� �� ���������:
    name -- ��� ('Test/1.0')
    email -- ����� ������������ (������ ������)
    headers -- ������� HTTP-���������� (DEFAULT_HEADERS)
    """
    def __init__(self,
              agentname=DEFAULT_AGENTNAME,
              email=DEFAULT_EMAIL,
              new_headers={}):

     self.agentname = agentname
     self.email = email
     # ��� ���������� ����� �������������� OpenDirector,
     # �������� � robots.txt.
     self.opener = urllib2.build_opener(
         RobotsHTTPHandler(self.agentname),
     )
     # ��������������� ���������� �� ���������
     headers = copy(DEFAULT_HEADERS)
     headers.update(new_headers)
     opener_headers = [ (k, v) for k, v in headers.iteritems() ]
     opener_headers.append(('User-Agent', self.agentname))
     # ���� email �� �����, HTTP-��������� 'From' �� �����
     if self.email:
         opener_headers.append(('From', self.email))

     self.opener.addheaders = opener_headers

    def open(self, url):
     """
     ���������� file-like object, ���������� � ��������� ������.
     � ������ ������ ���������� HTTPError, URLError ��� IOError.
     """
     return self.opener.open(url, None, TIMEOUT)