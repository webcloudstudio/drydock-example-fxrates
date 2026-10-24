from __future__ import annotations
import csv, io, re, urllib.request, zipfile
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from config import database_dsn
from persistence import open_database

class RejectedFile(Exception): pass
class OperationalFailure(Exception): pass
RATE_RE=re.compile(r'[0-9]+(?:\.[0-9]+)?\Z')
CURRENCY_RE=re.compile(r'[A-Z]{3}\Z')

def load_text(text):
    try: rows=list(csv.reader(io.StringIO(text, newline='')))
    except Exception as e: raise RejectedFile('invalid CSV') from e
    if not rows: raise RejectedFile('empty CSV')
    header=rows[0]
    if header and header[-1]=='': header=header[:-1]
    if len(header)<2 or header[0]!='Date' or any(not CURRENCY_RE.fullmatch(c) for c in header[1:]) or len(set(header[1:]))!=len(header[1:]): raise RejectedFile('invalid header')
    data=[]; dates=set()
    for row in rows[1:]:
        if row and row[-1]=='': row=row[:-1]
        if len(row)!=len(header): raise RejectedFile('invalid row shape')
        try: date.fromisoformat(row[0])
        except (ValueError, TypeError): raise RejectedFile('invalid date')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',row[0]) or row[0] in dates: raise RejectedFile('duplicate or invalid date')
        dates.add(row[0]);
        for currency,value in zip(header[1:],row[1:]):
            if value=='N/A': continue
            if not RATE_RE.fullmatch(value) or Decimal(value)==0: raise RejectedFile('invalid rate')
            data.append((row[0],currency,value))
    return dates,data

def persist(data):
    with open_database(database_dsn()) as db:
        for d,c,r in data: db.rates.replace_rate(date=d,currency=c,rate=r)

def load_file(path):
    try:
        with open(path,encoding='utf-8',newline='') as f: text=f.read()
    except OSError as e: raise OperationalFailure(str(e)) from e
    dates,data=load_text(text); persist(data); return len({d for d,c,r in data}),len(data)

def fetch():
    try:
        response = urllib.request.urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip')
        try:
            content = response.read()
        finally:
            close = getattr(response, 'close', None)
            if close is not None:
                close()
        with zipfile.ZipFile(io.BytesIO(content)) as z: text=z.read('eurofxref-hist.csv').decode('utf-8-sig')
    except Exception as e: raise OperationalFailure(str(e)) from e
    dates,data=load_text(text); persist(data); return len({d for d,c,r in data}),len(data)
