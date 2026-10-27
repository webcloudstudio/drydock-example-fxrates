"""Shared router registry. Feature stories attach their routes here; static routes go first."""

import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from fxrates_app import convert as convert_service
from fxrates_app import currencies as currency_service
from fxrates_app import history as history_service
from fxrates_app import rates as rate_service
from fxrates_app import stats as stats_service

router = APIRouter()
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
AMOUNT_PATTERN = r"^[0-9]+(\.[0-9]+)?$"


def _calendar_date(value: str) -> str:
    """Return `value` as an ISO calendar date; 422 for a well-formed string that is not a real date."""
    try:
        return datetime.date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise HTTPException(status_code=422, detail=f"not a real calendar date: {value}") from error


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. It reaches no store, so it answers even when the database is absent."""
    return {"status": "ok"}


@router.get("/stats")
def stats() -> dict[str, int | str | None]:
    """Counts of stored dates and rates, and the first and last publication dates."""
    return stats_service.stats()


@router.get("/currencies")
def currencies() -> dict[str, str | list[str]]:
    """The base currency and every stored currency code, ascending."""
    return {"base": rate_service.BASE, "currencies": currency_service.currencies()}


@router.get("/rates/latest")
def rates_latest() -> dict[str, str | dict[str, str]]:
    """The rates of the latest publication, with requested "latest"; 404 when nothing is stored."""
    found = rate_service.latest_rates()
    if found is None:
        raise HTTPException(status_code=404, detail="no publication is stored")
    effective, rates = found
    return {"date": effective, "requested": "latest", "base": rate_service.BASE, "rates": rates}


@router.get("/rates/{date}")
def rates_on_date(date: Annotated[str, Path(pattern=DATE_PATTERN)]) -> dict[str, str | dict[str, str]]:
    """The rates of the latest publication on or before `date`; 422 for an impossible date, 404 when none exists."""
    try:
        requested = datetime.date.fromisoformat(date).isoformat()
    except ValueError as error:
        raise HTTPException(status_code=422, detail=f"not a real calendar date: {date}") from error
    found = rate_service.rates_on(requested)
    if found is None:
        raise HTTPException(status_code=404, detail=f"no publication on or before {requested}")
    effective, rates = found
    return {"date": effective, "requested": requested, "base": rate_service.BASE, "rates": rates}


@router.get("/convert")
def convert_amount(
    source: Annotated[str, Query(alias="from")],
    target: Annotated[str, Query(alias="to")],
    amount: Annotated[str, Query(pattern=AMOUNT_PATTERN)],
    date: Annotated[str | None, Query(pattern=DATE_PATTERN)] = None,
) -> dict[str, str]:
    """Convert `amount` from one currency to another on `date`, or on the latest publication when omitted."""
    requested = None if date is None else _calendar_date(date)
    try:
        converted = convert_service.convert(source, target, amount, requested)
    except convert_service.UnknownCurrency as error:
        raise HTTPException(status_code=404, detail=f"no stored rate for {error}") from error
    except convert_service.UnusableRate as error:
        raise HTTPException(status_code=422, detail=f"stored rate is zero for {error}") from error
    if converted is None:
        detail = "no publication is stored" if requested is None else f"no publication on or before {requested}"
        raise HTTPException(status_code=404, detail=detail)
    return converted


@router.get("/history/{code}")
def history(
    code: str,
    start: Annotated[str | None, Query(pattern=DATE_PATTERN)] = None,
    end: Annotated[str | None, Query(pattern=DATE_PATTERN)] = None,
) -> dict[str, str | int | None | list[dict[str, str]]]:
    """A currency's stored rates from `start` through `end` inclusive, ascending by date, with count, min, max, and mean.

    404 for a currency with no stored rate at all; 422 for a malformed bound.
    """
    lower = None if start is None else _calendar_date(start)
    upper = None if end is None else _calendar_date(end)
    try:
        points = history_service.history_points(code, lower, upper)
    except history_service.UnknownCurrency as error:
        raise HTTPException(status_code=404, detail=f"no stored rate for {error}") from error
    summary = history_service.history_summary(points)
    return {"currency": code, "base": rate_service.BASE, **summary, "points": points}
