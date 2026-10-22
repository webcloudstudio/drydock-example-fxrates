#!/usr/bin/env python3
# Reference implementation of the FxRates contract, used only to validate the grader.
# Standard-library HTTP server in place of FastAPI; same routes, bodies, and status codes.
import csv, datetime, json, os, re, sqlite3, sys
from decimal import Decimal, ROUND_HALF_EVEN
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
def die(code, m): print(m, file=sys.stderr); sys.exit(code)
DB = (os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db").removeprefix("sqlite://")
def conn():
    os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)
    return sqlite3.connect(DB)
DATE = r"\d{4}-\d{2}-\d{2}"
def valid_date(s):
    if not re.fullmatch(DATE, s): return False
    try: datetime.date.fromisoformat(s); return True
    except ValueError: return False
RATE = r"[0-9]+(\.[0-9]+)?"
def q(x, places):
    e = Decimal(1).scaleb(-places)
    if (x / e) % 1 == Decimal("0.5"): raise SystemExit(f"TIE {x}")
    return str(x.quantize(e, ROUND_HALF_EVEN))
def cmd_init():
    c = conn(); c.execute("DROP TABLE IF EXISTS rates")
    c.execute("CREATE TABLE rates (date TEXT, currency TEXT, rate TEXT, PRIMARY KEY (date, currency))"); c.commit()
def cmd_load(path):
    try: rows = list(csv.reader(open(path, encoding="utf-8", newline="")))
    except OSError as e: die(1, str(e))
    if not rows or not rows[0] or rows[0][0] != "Date": die(3, "header")
    cur = [h for h in rows[0][1:]]
    if cur and cur[-1] == "": cur = cur[:-1]
    if not all(re.fullmatch(r"[A-Z]{3}", h) for h in cur): die(3, "currency code")
    data = []; dates = set()
    for n, r in enumerate(rows[1:], 2):
        if r and r[-1] == "" and len(r) == len(cur) + 2: r = r[:-1]
        if len(r) != len(cur) + 1: die(3, f"line {n}: fields")
        if not valid_date(r[0]) or r[0] in dates: die(3, f"line {n}: date")
        dates.add(r[0])
        for c, v in zip(cur, r[1:]):
            v = v.strip()
            if v == "N/A": continue
            if not re.fullmatch(RATE, v) or Decimal(v) == 0: die(3, f"line {n}: rate")
            data.append((r[0], c, v))
    try:
        c = conn(); c.executemany("INSERT OR REPLACE INTO rates VALUES (?,?,?)", data); c.commit()
    except sqlite3.Error as e: die(1, str(e))
    print("dates,rates"); print(f"{len({d for d, _, _ in data})},{len(data)}")
def rows(sql, *a): return conn().execute(sql, a).fetchall()
def effective(d): return rows("SELECT MAX(date) FROM rates WHERE date <= ?", d)[0][0]
def rates_on(d): return {c: r for c, r in rows("SELECT currency, rate FROM rates WHERE date = ? ORDER BY currency", d)}
def currencies(): return [c for (c,) in rows("SELECT DISTINCT currency FROM rates ORDER BY currency")]
def route(path, qs):
    p = path.rstrip("/") or "/"
    if p == "/health": return 200, {"status": "ok"}
    if p == "/stats":
        (n, first, last), = rows("SELECT COUNT(DISTINCT date), MIN(date), MAX(date) FROM rates")
        return 200, {"dates": n, "rates": rows("SELECT COUNT(*) FROM rates")[0][0], "first": first, "last": last}
    if p == "/currencies": return 200, {"base": "EUR", "currencies": currencies()}
    m = re.fullmatch(r"/rates/([^/]+)", p)
    if m:
        d = m.group(1)
        if d == "latest": d = effective("9999-12-31")
        elif not valid_date(d): return 422, None
        e = effective(d) if d else None
        if e is None: return 404, None
        return 200, {"date": e, "requested": m.group(1), "base": "EUR", "rates": rates_on(e)}
    if p == "/convert":
        need = ("from", "to", "amount")
        if any(k not in qs for k in need): return 422, None
        f, t, amt = qs["from"][0], qs["to"][0], qs["amount"][0]
        d = qs.get("date", ["latest"])[0]
        if not re.fullmatch(r"[0-9]+(\.[0-9]+)?", amt): return 422, None
        if d != "latest" and not valid_date(d): return 422, None
        e = effective("9999-12-31" if d == "latest" else d)
        if e is None: return 404, None
        rs = rates_on(e); rs["EUR"] = "1"
        if f not in rs or t not in rs: return 404, None
        ratio = Decimal(rs[t]) / Decimal(rs[f])
        exact = Decimal(amt) * Decimal(rs[t]) / Decimal(rs[f])
        return 200, {"date": e, "from": f, "to": t, "amount": amt, "rate": q(ratio, 6), "result": q(exact, 2)}
    m = re.fullmatch(r"/history/([^/]+)", p)
    if m:
        c = m.group(1)
        if c not in currencies(): return 404, None
        s = qs.get("start", ["0000-01-01"])[0]; en = qs.get("end", ["9999-12-31"])[0]
        for v in (s, en):
            if v not in ("0000-01-01", "9999-12-31") and not valid_date(v): return 422, None
        pts = rows("SELECT date, rate FROM rates WHERE currency = ? AND date >= ? AND date <= ? ORDER BY date", c, s, en)
        vals = [Decimal(r) for _, r in pts]
        return 200, {"currency": c, "base": "EUR", "count": len(pts),
                     "min": min(pts, key=lambda x: Decimal(x[1]))[1] if pts else None,
                     "max": max(pts, key=lambda x: Decimal(x[1]))[1] if pts else None,
                     "mean": q(sum(vals) / len(vals), 6) if pts else None,
                     "points": [{"date": d, "rate": r} for d, r in pts]}
    return 404, None
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path); code, body = route(u.path, parse_qs(u.query))
        b = json.dumps(body if body is not None else {"detail": "error"}).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
a = sys.argv[1:]
if not a: die(2, "command")
if a[0] == "init" and len(a) == 1: cmd_init()
elif a[0] == "load" and len(a) == 2: cmd_load(a[1])
elif a[0] == "serve" and len(a) == 3 and a[1] == "--port" and a[2].isdigit():
    ThreadingHTTPServer(("127.0.0.1", int(a[2])), H).serve_forever()
else: die(2, "usage")
