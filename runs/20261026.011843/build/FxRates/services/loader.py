from __future__ import annotations
import csv, re
from datetime import date
from pathlib import Path
from config import get_settings
from persistence import open_database
RATE=re.compile(r'[0-9]+(?:\.[0-9]+)?\Z')

def initialize() -> None:
    db=open_database(get_settings().database_location)
    try: db.execute_script('DROP TABLE IF EXISTS "rates"; CREATE TABLE "rates" ("id" INTEGER PRIMARY KEY, "date" TEXT NOT NULL, "currency" TEXT NOT NULL, "rate" TEXT NOT NULL, UNIQUE ("date", "currency")); CREATE INDEX "rates_date_idx" ON "rates" ("date"); CREATE INDEX "rates_currency_date_idx" ON "rates" ("currency", "date");')
    finally: db.close()

def parse_csv(text: str):
    rows=list(csv.reader(text.splitlines()))
    if not rows or len(rows[0])<2: raise ValueError('invalid header')
    header=rows[0]
    if header[-1]=='': header=header[:-1]
    if header[0]!='Date' or any(not re.fullmatch('[A-Z]{3}',c) for c in header[1:]) or len(set(header[1:]))!=len(header[1:]): raise ValueError('invalid header')
    parsed=[]; seen=set()
    for row in rows[1:]:
        if len(row)==len(header)+1 and row[-1]=='': row=row[:-1]
        if len(row)!=len(header): raise ValueError('wrong field count')
        try:
            d=date.fromisoformat(row[0])
            if d.isoformat()!=row[0]: raise ValueError()
        except ValueError: raise ValueError('invalid date')
        if row[0] in seen: raise ValueError('repeated date')
        seen.add(row[0])
        for cur,val in zip(header[1:],row[1:]):
            if val=='N/A': continue
            if not RATE.fullmatch(val) or not any(ch!='0' for ch in val if ch.isdigit()): raise ValueError('invalid rate')
            parsed.append((row[0],cur,val))
    return parsed

def load_text(text: str):
    parsed=parse_csv(text)
    db=open_database(get_settings().database_location)
    try:
        for d,c,r in parsed: db.rates.upsert(date=d,currency=c,rate=r)
    finally: db.close()
    return len({d for d,_,_ in parsed}),len(parsed)

def load_path(path: str): return load_text(Path(path).read_text(encoding='utf-8'))
