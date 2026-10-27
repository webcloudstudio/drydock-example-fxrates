"""Repository contract checks use the provisioned store and rollback fixture."""

from persistence.testing import db_session


def test_upsert_replaces_rate_text() -> None:
    with db_session() as db:
        saved = db.rates.upsert(date="2099-01-02", currency="QAA", rate="1.234")
        replaced = db.rates.upsert(date="2099-01-02", currency="QAA", rate="1.235")
        rows = db.rates.by_date(date="2099-01-02")
        assert (saved.rate, replaced.rate) == ("1.234", "1.235")
        assert [row.rate for row in rows if row.currency == "QAA"] == ["1.235"]


def test_by_date_filters_and_sorts_currencies() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-02-03", currency="QAZ", rate="2.50")
        db.rates.upsert(date="2099-02-03", currency="QAB", rate="2.51")
        rows = db.rates.by_date(date="2099-02-03")
        assert [row.currency for row in rows if row.date == "2099-02-03"] == ["QAB", "QAZ"]


def test_publications_through_are_descending() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-03-01", currency="QAC", rate="3")
        db.rates.upsert(date="2099-03-02", currency="QAC", rate="4")
        rows = db.rates.publications_through(requested_date="2099-03-02")
        dates = list(dict.fromkeys(row.date for row in rows if row.date >= "2099-03-01"))
        assert dates[:2] == ["2099-03-02", "2099-03-01"]


def test_history_uses_inclusive_bounds_and_order() -> None:
    with db_session() as db:
        for date, rate in (("2099-04-01", "1"), ("2099-04-02", "2"),
                           ("2099-04-03", "3"), ("2099-04-04", "4")):
            db.rates.upsert(date=date, currency="QAD", rate=rate)
        rows = db.rates.history(currency="QAD", start_date="2099-04-02", end_date="2099-04-03")
        assert [(row.date, row.rate) for row in rows] == [
            ("2099-04-02", "2"), ("2099-04-03", "3")
        ]


def test_list_includes_stored_published_text() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-05-06", currency="QAE", rate="5.006")
        assert any((row.date, row.currency, row.rate) == ("2099-05-06", "QAE", "5.006")
                   for row in db.rates.list())


def test_init_clears_rates_through_repository() -> None:
    from services.rates import initialize

    with db_session() as db:
        db.rates.upsert(date="2099-11-12", currency="QAR", rate="1.25")
        db.rates.upsert(date="2099-11-13", currency="QAS", rate="2.5")
        initialize(db)
        assert db.rates.list() == []
