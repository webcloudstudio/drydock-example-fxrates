from __future__ import annotations
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
import re
from fastapi import FastAPI, HTTPException, Query
from services import rates as service

app=FastAPI(title='FxRates')
def create_app() -> FastAPI: return app

def check_date(value: str):
    if not service.valid_date(value): raise HTTPException(422, 'invalid date')

def effective(requested):
    rows=service.through(requested)
    return rows[0].date if rows else None

def rate_map(d): return {r.currency:r.rate for r in service.by_date(d)}
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/currencies')
def currencies(): return {'base':'EUR','currencies':sorted({r.currency for r in service.all_rows()})}
@app.get('/stats')
def stats():
    rows=service.all_rows(); dates={r.date for r in rows}
    return {'dates':len(dates),'rates':len(rows),'first':min(dates) if dates else None,'last':max(dates) if dates else None}
@app.get('/rates/latest')
def latest():
    rows=service.all_rows()
    if not rows: raise HTTPException(404)
    d=max(r.date for r in rows)
    return {'date':d,'requested':'latest','base':'EUR','rates':rate_map(d)}
@app.get('/rates/{requested}')
def rates(requested: str):
    check_date(requested); d=effective(requested)
    if d is None: raise HTTPException(404)
    return {'date':d,'requested':requested,'base':'EUR','rates':rate_map(d)}
@app.get('/history/{code}')
def currency_history(code: str, start: str|None=None, end: str|None=None):
    if start: check_date(start)
    if end: check_date(end)
    all_points=service.history(code,None,None)
    if not all_points: raise HTTPException(404)
    points=service.history(code,start,end)
    vals=[Decimal(p.rate) for p in points]
    return {'currency':code,'base':'EUR','count':len(points),'min':min(points,key=lambda p:Decimal(p.rate)).rate if points else None,'max':max(points,key=lambda p:Decimal(p.rate)).rate if points else None,'mean':f'{(sum(vals,Decimal(0))/len(vals)).quantize(Decimal("0.000001"),rounding=ROUND_HALF_EVEN):.6f}' if vals else None,'points':[{'date':p.date,'rate':p.rate} for p in points]}
@app.get('/convert')
def convert(source: str=Query(alias='from'), target: str=Query(alias='to'), amount: str=Query(), requested: str|None=Query(default=None,alias='date')):
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',amount): raise HTTPException(422)
    if requested is not None: check_date(requested)
    rows=service.all_rows()
    d=(effective(requested) if requested else max((r.date for r in rows),default=None))
    if d is None: raise HTTPException(404)
    mapping=rate_map(d)
    if source!='EUR' and source not in mapping or target!='EUR' and target not in mapping: raise HTTPException(404)
    a=Decimal(amount); src=Decimal(1) if source=='EUR' else Decimal(mapping[source]); dst=Decimal(1) if target=='EUR' else Decimal(mapping[target])
    ratio=dst/src; result=a*dst/src
    return {'date':d,'from':source,'to':target,'amount':amount,'rate':f'{ratio.quantize(Decimal("0.000001"),rounding=ROUND_HALF_EVEN):.6f}','result':f'{result.quantize(Decimal("0.01"),rounding=ROUND_HALF_EVEN):.2f}'}
