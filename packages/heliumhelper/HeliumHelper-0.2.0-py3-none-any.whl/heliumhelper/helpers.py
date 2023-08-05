import requests
import time
from datetime import datetime, timedelta
import pandas as pd
import flatdict


def get_price(block: int) -> float:
    """
    Use this to find price of HNT at a specific block
    :param block: Helium block to request price for
    :return: Helium price in $ at block
    """
    url = f'https://api.helium.io/v1/oracle/prices/{block}'
    resp: dict = api_handler(url)
    price = resp['data']['price'] / 10 ** 8
    return price


def api_looper(url: str, params: dict, time_format: str, ts_start) -> list[dict]:
    """
    Calls specified api repeatedly until specified time, replacing the cursor each time to get the next
    page
    :param url: url for api endpoint
    :param params: Any params to be passed when calling endpoint
    :param time_format: Time format returned by the endpoint being called e.g. 'timestamp' or 'datetime'
    :param ts_start: the stopping point for the data you want returned in the format specified in time_format
    :return: The data from the repeated calls in one list of dicts
    """
    print('API Call', end='')
    data = []
    current_month = None

    while True:
        print(".", end="")
        resp = api_handler(url, params)
        if len(resp) < 2:
            print('')
            print('len < 2')
            break
        if time_format == 'timestamp' and len(resp['data']) > 0 and resp['data'][0]['time'] < ts_start:
            print('')
            print('time < start')
            break
        try:
            if time_format == 'datetime' and len(resp['data']) > 0:
                s = resp['data'][0]['timestamp']
                time_dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
                time_ts = time_dt.timestamp()
                if time_ts < ts_start:
                    print('')
                    print('time < start')
                    break
                if time_dt.month != current_month:
                    print('')
                    print(time_dt.strftime('%B'))
                    print('API Call', end='')
                current_month = time_dt.month
        except:
            print(resp)
            raise Exception
        params['cursor'] = resp['cursor']
        data.extend(resp['data'])
    return data


def account_hotspots(account_address) -> pd.DataFrame:
    """
    Used to get data on all the hotspots listed under an account
    :param account_address: Helium account address as found in the wallet or explorer
    :return: dataframe of data on hotspots
    """
    url = f'https://api.helium.io/v1/accounts/{account_address}/hotspots'
    resp = api_handler(url)

    hotspot_list = []
    for hotspot in resp['data']:
        flat = flatdict.FlatDict(hotspot)
        hotspot_flat = dict(flat)
        hotspot_list.append(hotspot_flat)
    df = pd.DataFrame(hotspot_list)
    return df


def wait_handler(r: requests.Response):
    """
    Helium endpoints sometimes get overloaded and will return a wait period rather than data, this function handles
    that
    :param r: response from API call
    :return: no return
    """
    resp = r.json()
    wait = resp['come_back_in_ms']
    print(f'Waiting {wait} ms')
    time.sleep(wait / 1000)
    return


def api_down_handler(r: requests.Response):
    """
    Sometimes the Helium API is down, this function waits for 1 minute
    :param r: response from API
    :return: no return
    """
    print(r.content)
    print('API down retry in 1 minute')
    time.sleep(60)
    return


def api_handler(url: str, params: dict = None) -> dict:
    """
    Calls the specified endpoint and handles status codes
    :param url: url to API endpoint
    :param params: any parameters to be passed to the endpoint
    :return: returns the response as a json dictionary
    """
    while True:
        r = requests.get(url, params)
        if r.status_code == 200:
            resp = r.json()
            break
        elif r.status_code == 403:
            wait_handler(r)
        elif r.status_code == 503:
            api_down_handler(r)
        else:
            print(f'Unknown status code {r.status_code}')
            print(r)
            print(r.json())
            raise Exception
    return resp


def get_current_price() -> float:
    """

    :return: Current oracle price in dollars
    """
    url = f'https://api.helium.io/v1/oracle/prices/current'
    resp = api_handler(url)
    price = resp['data']['price'] / 10 ** 8
    return price


def get_hotspot_rewards_sum(hotspot_address: str, period: str) -> [float, int]:
    """
    Provides rewards record for a hotspot over a give period from today. Valid periods are day, week, two week, month,
    and year
    :param hotspot_address: hotspot address as seen on the Helium explorer
    :param period: how far back the earnings should be bucketed
    :return: Number of HNT mined by a hotspot in the given period as well as how many days that period is
    """
    url = f'https://api.helium.io/v1/hotspots/{hotspot_address}/rewards/sum'
    today = datetime.today()
    if period == 'day':
        days = 1
    elif period == 'week':
        days = 7
    elif period == 'two weeks':
        days = 14
    elif period == 'month':
        days = 30
    elif period == 'year':
        days = 365
    else:
        raise Exception('Invalid period, try: day, week, year')
    earlier = today + timedelta(days=-days)
    p = {
        'max_time': today.strftime('%Y-%m-%dT00:00:00Z'),
        'min_time': earlier.strftime('%Y-%m-%dT00:00:00Z')
    }
    resp = api_handler(url, p)
    return resp['data']['total'], days
