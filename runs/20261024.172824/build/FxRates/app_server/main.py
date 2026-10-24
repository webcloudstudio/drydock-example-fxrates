"""FastAPI application factory and ASGI entry point."""

from decimal import Decimal
from fastapi import FastAPI, HTTPException, Query

from services.common import AMOUNT_RE, all_rates, effective, rounded, valid_date


def create_app() -> FastAPI:
    """Build the FxRates HTTP application."""
    api = FastAPI(title="FxRates")

    @api.get("/health")
    def health():
        return {"status": "ok"}

    @api.get("/stats")
    def stats():
        rows = all_rates()
        dates = sorted({row.date for row in rows})
        return {"dates": len(dates), "rates": len(rows), "first": dates[0] if dates else None, "last": dates[-1] if dates else None}

    @api.get("/currencies")
    def currencies():
        return {"base": "EUR", "currencies": sorted({row.currency for row in all_rates()})}

    @api.get("/rates/latest")
    def latest():
        found = effective("latest")
        if found is None:
            raise HTTPException(404)
        day, rates = found
        return {"date": day, "requested": "latest", "base": "EUR", "rates": rates}

    @api.get("/rates/{requested}")
    def rates(requested: str):
        if not valid_date(requested):
            raise HTTPException(422)
        found = effective(requested)
        if found is None:
            raise HTTPException(404)
        day, values = found
        return {"date": day, "requested": requested, "base": "EUR", "rates": values}

    @api.get("/history/{code}")
    def history(code: str, start: str | None = None, end: str | None = None):
        if (start is not None and not valid_date(start)) or (end is not None and not valid_date(end)):
            raise HTTPException(422)
        rows = sorted((r for r in all_rates() if r.currency == code), key=lambda r: r.date)
        if not rows:
            raise HTTPException(404)
        points = [r for r in rows if (start is None or r.date >= start) and (end is None or r.date <= end)]
        if not points:
            return {"currency": code, "base": "EUR", "count": 0, "min": None, "max": None, "mean": None, "points": []}
        low = min(points, key=lambda r: Decimal(r.rate))
        high = max(points, key=lambda r: Decimal(r.rate))
        mean = sum((Decimal(r.rate) for r in points), Decimal(0)) / len(points)
        return {"currency": code, "base": "EUR", "count": len(points), "min": low.rate, "max": high.rate, "mean": rounded(mean, 6), "points": [{"date": r.date, "rate": r.rate} for r in points]}

    @api.get("/convert")
    def convert(source: str = Query(..., alias="from"), to: str = Query(...), amount: str = Query(...), date: str | None = None):
        if not AMOUNT_RE.fullmatch(amount):
            raise HTTPException(422)
        if date is not None and not valid_date(date):
            raise HTTPException(422)
        found = effective(date)
        if found is None:
            raise HTTPException(404)
        day, rates = found
        if (source != "EUR" and source not in rates) or (to != "EUR" and to not in rates):
            raise HTTPException(404)
        source_rate = Decimal(1) if source == "EUR" else Decimal(rates[source])
        target_rate = Decimal(1) if to == "EUR" else Decimal(rates[to])
        exact = target_rate / source_rate
        result = Decimal(amount) * target_rate / source_rate
        return {"date": day, "from": source, "to": to, "amount": amount, "rate": rounded(exact, 6), "result": rounded(result, 2)}

    return api


app = create_app()
