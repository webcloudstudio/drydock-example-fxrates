from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from fastapi import FastAPI, HTTPException, Query
from config import database_dsn
from persistence import open_database

def parsed_date(value):
    try:
        if len(value)!=10 or date.fromisoformat(value).isoformat()!=value: raise ValueError
        return value
    except (ValueError,TypeError): raise HTTPException(422,'invalid date')

def all_rates():
    with open_database(database_dsn()) as db: return db.rates.all()

def create_app():
    app=FastAPI(title='FxRates')
    @app.get('/health')
    def health(): return {'status':'ok'}
    @app.get('/stats')
    def stats():
        rows=all_rates(); ds=sorted({r.date for r in rows})
        return {'dates':len(ds),'rates':len(rows),'first':ds[0] if ds else None,'last':ds[-1] if ds else None}
    @app.get('/currencies')
    def currencies(): return {'base':'EUR','currencies':sorted({r.currency for r in all_rates()})}
    @app.get('/rates/latest')
    def latest():
        with open_database(database_dsn()) as db:
            latest_rows=db.rates.latest()
            rows=db.rates.for_date(date=latest_rows[0].date) if latest_rows else []
        if not rows: raise HTTPException(404,'no rates')
        return {'date':rows[0].date,'requested':'latest','base':'EUR','rates':{r.currency:r.rate for r in rows}}
    @app.get('/rates/{requested}')
    def rates(requested:str):
        requested=parsed_date(requested)
        with open_database(database_dsn()) as db:
            candidates=db.rates.latest_on_or_before(requested_date=requested)
            rows=db.rates.for_date(date=candidates[0].date) if candidates else []
        if not rows: raise HTTPException(404,'no rates')
        return {'date':rows[0].date,'requested':requested,'base':'EUR','rates':{r.currency:r.rate for r in rows}}
    @app.get('/convert')
    def convert(from_:str=Query(alias='from'),to:str=Query(),amount:str=Query(),date_:str|None=Query(default=None,alias='date')):
        if not __import__('re').fullmatch(r'[0-9]+(?:\.[0-9]+)?',amount): raise HTTPException(422,'invalid amount')
        req=parsed_date(date_) if date_ is not None else None
        with open_database(database_dsn()) as db:
            candidates=db.rates.latest() if req is None else db.rates.latest_on_or_before(requested_date=req)
            rows=db.rates.for_date(date=candidates[0].date) if candidates else []
        if not rows: raise HTTPException(404,'no rates')
        by={r.currency:Decimal(r.rate) for r in rows}; by['EUR']=Decimal(1)
        if from_ not in by or to not in by: raise HTTPException(404,'unknown currency')
        rate=by[to]/by[from_]; result=Decimal(amount)*by[to]/by[from_]
        return {'date':rows[0].date,'from':from_,'to':to,'amount':amount,'rate':format(rate.quantize(Decimal('.000001'),rounding=ROUND_HALF_EVEN),'.6f'),'result':format(result.quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN),'.2f')}
    @app.get('/history/{code}')
    def history(code:str,start:str|None=None,end:str|None=None):
        start=parsed_date(start) if start is not None else '0001-01-01'; end=parsed_date(end) if end is not None else '9999-12-31'
        with open_database(database_dsn()) as db:
            known=db.rates.history(currency=code,start_date='0001-01-01',end_date='9999-12-31')
            rows=db.rates.history(currency=code,start_date=start,end_date=end)
        if not known: raise HTTPException(404,'unknown currency')
        values=[Decimal(r.rate) for r in rows]; n=len(rows)
        mean=(sum(values)/n).quantize(Decimal('.000001'),rounding=ROUND_HALF_EVEN) if n else None
        return {'currency':code,'base':'EUR','count':n,'min':str(min(values)) if n else None,'max':str(max(values)) if n else None,'mean':f'{mean:.6f}' if mean is not None else None,'points':[{'date':r.date,'rate':r.rate} for r in rows]}
    return app
app=create_app()
