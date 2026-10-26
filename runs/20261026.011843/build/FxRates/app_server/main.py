from __future__ import annotations
import re
from decimal import Decimal, ROUND_HALF_EVEN
from fastapi import FastAPI, HTTPException, Query
from services.queries import rows,effective,currency_history,valid_date,decfmt

def create_app() -> FastAPI:
 app=FastAPI(title='FxRates')
 @app.get('/health')
 def health(): return {'status':'ok'}
 @app.get('/stats')
 def stats():
  rs=rows(); ds=sorted({r.date for r in rs})
  return {'dates':len(ds),'rates':len(rs),'first':ds[0] if ds else None,'last':ds[-1] if ds else None}
 @app.get('/currencies')
 def currencies(): return {'base':'EUR','currencies':sorted({r.currency for r in rows()})}
 @app.get('/rates/latest')
 def latest(): return rates_for('latest')
 @app.get('/rates/{requested}')
 def rates_for(requested: str):
  rs=rows()
  if requested=='latest': as_of=max((r.date for r in rs),default=None)
  else:
   if not valid_date(requested): raise HTTPException(422)
   as_of=requested
  if not as_of: raise HTTPException(404)
  selected=effective(as_of)
  if not selected: raise HTTPException(404)
  actual=selected[0].date
  return {'date':actual,'requested':requested,'base':'EUR','rates':{r.currency:r.rate for r in selected}}
 @app.get('/history/{code}')
 def history(code: str,start: str|None=None,end: str|None=None):
  if start is not None and not valid_date(start) or end is not None and not valid_date(end): raise HTTPException(422)
  if start and end and start>end: raise HTTPException(422)
  rs=currency_history(code,start,end)
  if rs is None: raise HTTPException(404)
  if not rs: return {'currency':code,'base':'EUR','count':0,'min':None,'max':None,'mean':None,'points':[]}
  lo=min(rs,key=lambda r:Decimal(r.rate)); hi=max(rs,key=lambda r:Decimal(r.rate)); mean=sum((Decimal(r.rate) for r in rs),Decimal(0))/len(rs)
  return {'currency':code,'base':'EUR','count':len(rs),'min':lo.rate,'max':hi.rate,'mean':decfmt(mean,'0.000001'),'points':[{'date':r.date,'rate':r.rate} for r in rs]}
 @app.get('/convert')
 def convert(source: str=Query(alias='from'),target: str=Query(alias='to'),amount: str=Query(...),date: str|None=None):
  if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',amount): raise HTTPException(422)
  if date is not None and not valid_date(date): raise HTTPException(422)
  rs=rows(); asof=date or max((r.date for r in rs),default=None)
  if not asof: raise HTTPException(404)
  selected=effective(asof)
  if not selected: raise HTTPException(404)
  actual=selected[0].date; rates={r.currency:Decimal(r.rate) for r in selected}; rates['EUR']=Decimal(1)
  if source not in rates or target not in rates: raise HTTPException(404)
  exact=rates[target]/rates[source]; result=Decimal(amount)*exact
  return {'date':actual,'from':source,'to':target,'amount':amount,'rate':decfmt(exact,'0.000001'),'result':decfmt(result,'0.01')}
 return app
app=create_app()
