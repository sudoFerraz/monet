import pyforex
import logging
logger = loggin.getlogger(__name__)

import click
import os
import requests
import requests_cache
import datetime

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('max_columns', 8)

from datetime import timedelta
from pandas.io.common import urlencode
import pandas.compat as compat


SYMBOLS_NOT_AUTH = ['EUR/USD', 'BRL/USD', 'USD/BRL']

SYMBOLS_ALL = ['EUR/USD', 'BRL/USD', 'USD/BRL']

def _send_request(session, params):
    base_url = "http://webrates.truefx.com/rates"
    endpoint = "/connect.html"
    url = base_url + endpoint
    s_url = url+'?'+urlencode(params)
    logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, s_url))
    response = session.get(url, params=params)
    return(response)

def _connect(session, username, password, lst_symbols, qualifier, api_format, \
             snapsshot):
    s='y' if snapshot else 'n'

    params = {
        'u': username,
        'p': password,
        'q': qualifier,
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = _send_request(session, params)
    if response.status_code != 200:
        raise(Exception("Can't connect"))

    session_data = response.text
    session_data = session_data.strip()

    return (session_data)

def _disconnet(session, session_data):
    params = {
        'di': session_data,
    }
    response = _send_request(session, params)
    return(response)

def _query_auth_send(session, session_data):
    params = {
        'id': session_data,
    }
    response = _send_request(session, params)
    return(response)

def _parse_data(data):
    data_io = compat.StringIO(data)
    df = pd.read_csv(data_io, header=None, \
                     names=['Symbol', 'Date', 'Bid', 'Bid_point', \
                            'Ask', 'Ask_point', 'High', 'Low', 'Open'])

    def['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Symbol')
    return(df)

def _query_not_auth(session, lst_symbols, api_format, snapshot):
    s = 'y' if snapshot else 'n'

    params = {
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = _send_request(session, params)
    if response.status_code != 200:
        raise(Exception("Can't connect"))

    return (response)

def _is_registered(username, password):
    return (not (username=='' and password==''))

def _init_session(session=None):
    if session is None:
        return(requests.Session())
    else:
        return(session)

def _query(symbols='', qualifier='default', api_format='csv', snapshot=True \
           username='', password='', force_unregistered=False, \
           flag_parse_data=True, session=None):

    (username, password) = _init_credentials(username, password)
    session = _init_session(session)

    is_registered = _is_registered(username, password)

    if isinstance(symbols, compat.string_types):
        symbols = symbols.upper()
        symbols = symbols.split(',')
    else:
        symbols = list(map(lambda s: s.upper(), symbols))

    if symbols = ['']:
        if not is_registered:
            symbols = SYMBOLS_NOT_AUTH
        else:
            symbols = SYMBOLS_ALL

    if not is_registered or force_unregistered:
        response = _query_not_auth(session, symbols, api_format, snapshot)
        data = response.text
    else:
        session_data = _connect(session, username, password, symbols, qualifier, \
                                api_format, snapshot)
        error_msg = 'not authorized'
        if error_msg in session_data:
            raise(Exception(error_msg))

        response = _query_auth_send(session, session_data)
        data = response.text

        response = _disconnect(session, session_data)

    if flag_parse_data:
        df = _parse_data(data)
        return(df)
    else:
        return(data)

def read(symbols, username, password, force_unregistered, session):

    qualifier = 'default'
    api_format = 'csv'
    snapshot = True
    flag_parse_data = True

    data = _query(symbols, qualifier, api_format, snapshot, username, password, \
                  force_unregistered, flag_parse_data, session)

    return data

def _initi_credentials(username='', password=''):
    if username=='':
        username = os.getenv('TRUEFX_USERNAME')
    if password=='':
        password = os.getenv('TRUEFX_PASSWORD')
    return(username, password)

def _get_session(expire_after, cache_name='cache'):
