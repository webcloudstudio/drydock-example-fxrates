"""FastAPI application factory and module-level ASGI application."""

from datetime import date

from fastapi import FastAPI, HTTPException, Query

from services import all_rates, convert, effective, history


def create_app() -> FastAPI:
    application = FastAPI(title="FxRates")

    @application.get("/health")
    def health():
        return {"status": "ok"}

    @application.get("/stats")
    def stats():
        rows = all_rates()
        dates = sorted({row.date for row in rows})
        return {"dates": len(dates), "rates": len(rows), "first": dates[0] if dates else None, "last": dates[-1] if dates else None}

    @application.get("/currencies")
    def currencies():
        return {"base": "EUR", "currencies": sorted({row.currency for row in all_rates()})}

    @application.get("/rates/latest")
    def latest_rates():
        resolved = effective(None)
        if resolved is None:
            raise HTTPException(404)
        day, rates = resolved
        return {"date": day, "requested": "latest", "base": "EUR", "rates": rates}

    @application.get("/rates/{requested}")
    def rates(requested: str):
        _date(requested)
        resolved = effective(requested)
        if resolved is None:
            raise HTTPException(404)
        day, values = resolved
        return {"date": day, "requested": requested, "base": "EUR", "rates": values}

    @application.get("/convert")
    def conversion(source: str = Query(alias="from"), target: str = Query(alias="to"), amount: str = Query(...), requested: str | None = Query(default=None, alias="date")):
        if not source.isalpha() or len(source) != 3 or source.upper() != source or not target.isalpha() or len(target) != 3 or target.upper() != target:
            raise HTTPException(404)
        if requested is not None:
            _date(requested)
        from decimal import Decimal, InvalidOperation
        try:
            parsed = Decimal(amount)
            if not parsed.is_finite() or parsed <= 0:
                raise InvalidOperation
        except InvalidOperation:
            raise HTTPException(422)
        value = convert(source, target, amount, requested)
        if value is None:
            raise HTTPException(404)
        return value

    @application.get("/history/{currency}")
    def currency_history(currency: str, start: str | None = None, end: str | None = None):
        if not currency.isalpha() or len(currency) != 3 or currency.upper() != currency:
            raise HTTPException(404)
        if start is not None:
            _date(start)
        if end is not None:
            _date(end)
        value = history(currency, start, end)
        if value is None:
            raise HTTPException(404)
        return value

    return application


def _date(value: str) -> None:
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except ValueError:
        raise HTTPException(422)


app = create_app()
