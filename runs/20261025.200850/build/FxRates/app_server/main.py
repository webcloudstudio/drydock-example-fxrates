"""FastAPI application factory and ASGI entry point."""

from fastapi import FastAPI, HTTPException, Query
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
import os, re
from persistence import open_database

def _db():
    return open_database(os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db")

def _valid(day: str) -> bool:
    try:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", day)) and date.fromisoformat(day).isoformat() == day
    except ValueError:
        return False

def _effective(day: str | None):
    with _db() as db:
        rows = db.rates.list(end_date=day) if day else db.rates.list()
    if not rows: return None, []
    eff = rows[-1].date
    return eff, [r for r in rows if r.date == eff]


def create_app() -> FastAPI:
    app = FastAPI(title="FxRates")
    @app.get("/health")
    def health(): return {"status":"ok"}
    @app.get("/stats")
    def stats():
        with _db() as db: rows=db.rates.list()
        dates=sorted({r.date for r in rows})
        return {"dates":len(dates),"rates":len(rows),"first":dates[0] if dates else None,"last":dates[-1] if dates else None}
    @app.get("/currencies")
    def currencies():
        with _db() as db: rows=db.rates.list()
        return {"base":"EUR","currencies":sorted({r.currency for r in rows})}
    @app.get("/rates/latest")
    def latest(): return rate_payload("latest", None)
    @app.get("/rates/{requested}")
    def rate_date(requested: str):
        if not _valid(requested): raise HTTPException(422)
        return rate_payload(requested, requested)
    def rate_payload(label, requested):
        eff, rows=_effective(requested)
        if eff is None: raise HTTPException(404)
        return {"date":eff,"requested":label,"base":"EUR","rates":{r.currency:r.rate for r in rows}}
    @app.get("/convert")
    def convert(source: str=Query(alias="from"), target: str=Query(alias="to"), amount: str=Query(...), requested: str|None=Query(None,alias="date")):
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", amount) or (requested is not None and not _valid(requested)): raise HTTPException(422)
        eff, rows=_effective(requested)
        if eff is None: raise HTTPException(404)
        rates={r.currency:Decimal(r.rate) for r in rows}; rates["EUR"]=Decimal(1)
        if source not in rates or target not in rates: raise HTTPException(404)
        raw_rate=rates[target]/rates[source]
        quantum=Decimal("0.000001"); result_quantum=Decimal("0.01")
        shown=raw_rate.quantize(quantum,rounding=ROUND_HALF_EVEN)
        result=(Decimal(amount)*raw_rate).quantize(result_quantum,rounding=ROUND_HALF_EVEN)
        return {"date":eff,"from":source,"to":target,"amount":amount,"rate":f"{shown:.6f}","result":f"{result:.2f}"}
    @app.get("/history/{code}")
    def history(code: str, start: str|None=None, end: str|None=None):
        if (start and not _valid(start)) or (end and not _valid(end)): raise HTTPException(422)
        filters={"currency":code}
        if start is not None: filters["start_date"]=start
        if end is not None: filters["end_date"]=end
        with _db() as db: rows=db.rates.list(**filters); all_rows=db.rates.list(currency=code)
        if not all_rows: raise HTTPException(404)
        values=[Decimal(r.rate) for r in rows]
        if values:
            low=min(range(len(values)),key=values.__getitem__); high=max(range(len(values)),key=values.__getitem__)
            mean=(sum(values,Decimal(0))/len(values)).quantize(Decimal("0.000001"),rounding=ROUND_HALF_EVEN)
            minimum,maximum=rows[low].rate,rows[high].rate
        else: minimum=maximum=mean=None
        return {"currency":code,"base":"EUR","count":len(rows),"min":minimum,"max":maximum,"mean":f"{mean:.6f}" if mean is not None else None,"points":[{"date":r.date,"rate":r.rate} for r in rows]}
    return app


app = create_app()
