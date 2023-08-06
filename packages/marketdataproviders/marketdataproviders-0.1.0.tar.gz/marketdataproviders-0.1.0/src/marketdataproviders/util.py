import datetime
import urllib

import pandas as pd

FMT_YYYY_MM_DD = "%Y-%m-%d"

def fmt_dt_yyyy_mm_dd(dt: datetime.datetime) -> str:
    return dt.strftime(FMT_YYYY_MM_DD) if dt else None

def url_join(base_url: str, params: dict[str, str]) -> str:
    return base_url + '?' + urllib.parse.urlencode(params)

def parse_dt_yyyy_mm_dd(dtstr: str) -> datetime.datetime:
    return datetime.datetime.strptime(dtstr, FMT_YYYY_MM_DD)

def dump_to_hdf_file(filepath: str, hdf_key: str, df: pd.DataFrame, mode='w'):
    df.to_hdf(filepath, key=hdf_key, mode=mode)

def read_hdf_file(filepath: str, hdf_key: str, mode='r') -> pd.DataFrame:
    return pd.read_hdf(filepath, key=hdf_key, mode=mode)
