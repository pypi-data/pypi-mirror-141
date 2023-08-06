'''
Data from: https://eodhistoricaldata.com/
'''

from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass

import requests
import pandas as pd

from . import util

@dataclass
class EodHistoricalDataReader:
    api_key: str

    def end_of_day_prices(self, symbol: str,  start: datetime, end: datetime=None, period: str='d'):
        '''
        period: 'd' for daily, 'w' for weekly, 'm' for monthly.
        Returns DataFrame:
            index => date
            Columns:
                open, high, low, close, adjusted_close, volume
        '''
        assert period in ('d', 'w', 'm'), 'Invalid period'

        if end is None:
            end = datetime.now()

        json_resp = self.__json_req(
            api_path='eod',
            symbol=symbol,
            params={
                'period': period,
                'from': util.fmt_dt_yyyy_mm_dd(start),  
                'to': util.fmt_dt_yyyy_mm_dd(end),
            }
        )
        idx = []
        data = defaultdict(list)
        for rec in json_resp:
            idx.append(util.parse_dt_yyyy_mm_dd(rec["date"]))
            for col in ['open', 'high', 'low', 'close', 'adjusted_close', 'volume']:
                data[col].append(rec[col])
        return pd.DataFrame(index=idx, data=data)

    def dividends(self, symbol: str, start: datetime, end: datetime=None) -> pd.DataFrame:
        '''
        Returns DataFrame:
            index => date
            Columns:
            value: number
            currency: str
        '''
        assert start is not None, "Must specify start date"
        if end is None:
            end = datetime.now()
        json_resp = self.__json_req(
            api_path='div',
            symbol=symbol,
            params={
                'from': util.fmt_dt_yyyy_mm_dd(start),  
                'to': util.fmt_dt_yyyy_mm_dd(end),
            }
        )
        idx = []
        data = defaultdict(list)
        for rec in json_resp:
            idx.append(util.parse_dt_yyyy_mm_dd(rec["date"]))
            data['value'].append(rec["value"])
            data['currency'].append(rec["currency"])
        return pd.DataFrame(index=idx, data=data)

    
    def __json_req(self, api_path, symbol, params) -> str:
        return self.__req(
            api_path=api_path,
            symbol=symbol,
            params=params,
            fmt='json'
        ).json()

    def __csv_req(self, api_path, symbol, params) -> str:
        return self.__req(
            api_path=api_path,
            symbol=symbol,
            params=params,
            fmt='csv'
        ).text
    
    def __req(self, api_path, symbol, params, fmt: str) -> str:
        p = dict(params)
        p.update({ 'api_token': self.api_key, 'fmt': fmt })
        url = util.url_join(
            f'https://eodhistoricaldata.com/api/{api_path}/{symbol}',
            p
        )
        return requests.get(url)
