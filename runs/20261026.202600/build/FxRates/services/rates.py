from __future__ import annotations
import csv, os, re, tempfile, urllib.request, zipfile, io
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from config import database_dsn
from persistence import open_database

RATE = re.compile(r'[0-9]+(?:\.[0-9]+)?\Z')
CODE = re.compile(r'[A-Z]{3}\Z')
ECB_HISTORY_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'

def fetch_file() -> tuple[int, int]:
    with urllib.request.urlopen(ECB_HISTORY_URL) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        csv_payload = archive.read('eurofxref-hist.csv')
    with tempfile.NamedTemporaryFile() as source:
        source.write(csv_payload)
        source.flush()
        return load_file(source.name)

def db(): return open_database(database_dsn())
def valid_date(value: str) -> bool:
    try: return date.fromisoformat(value).isoformat() == value
    except ValueError: return False

def load_file(path: str) -> tuple[int,int]:
    with open(path, newline='', encoding='utf-8-sig') as f: rows=list(csv.reader(f))
    if not rows: raise ValueError('empty CSV')
    header=rows[0]
    if header and header[-1]=='': header=header[:-1]
    if len(header)<2 or header[0]!='Date' or any(not CODE.fullmatch(c) for c in header[1:]) or len(set(header[1:]))!=len(header[1:]): raise ValueError('invalid header')
    parsed=[]; seen=set()
    for row in rows[1:]:
        if row and row[-1]=='': row=row[:-1]
        if len(row)!=len(header) or not valid_date(row[0]) or row[0] in seen: raise ValueError('invalid row')
        seen.add(row[0]); values=[]
        for code,value in zip(header[1:],row[1:]):
            if value=='N/A': continue
            if not RATE.fullmatch(value) or Decimal(value)==0: raise ValueError('invalid rate')
            values.append((row[0],code,value))
        parsed.extend(values)
    with db() as store:
        for d,c,r in parsed: store.rates.upsert(date=d,currency=c,rate=r)
    return len({d for d,_,_ in parsed}),len(parsed)

def initialize(store=None):
    if store is None:
        from pathlib import Path
        with db() as store:
            store.execute_script((Path(__file__).resolve().parent.parent / 'schema.sql').read_text(encoding='utf-8'))
            for row in store.rates.list():
                store.rates.delete(date=row.date, currency=row.currency)
        return
    if store is not None:
        for row in store.rates.list():
            store.rates.delete(date=row.date, currency=row.currency)

def all_rows():
    with db() as store: return store.rates.list()
def through(d):
    with db() as store: return store.rates.publications_through(requested_date=d)
def by_date(d):
    with db() as store: return store.rates.by_date(date=d)
def history(c,s,e):
    # The generated repository compares both bounds unconditionally. Supply the
    # full ISO date domain for an omitted bound so open-ended history still works.
    with db() as store:
        return store.rates.history(
            currency=c,
            start_date=s if s is not None else '0001-01-01',
            end_date=e if e is not None else '9999-12-31',
        )
