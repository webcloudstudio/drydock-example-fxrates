#!/usr/bin/env python3
# emit_fx.py <datadir> — run the FxRates reference through the grader's sequence and print the
# grader's check and http blocks.
import json, os, socket, subprocess, sys, tempfile, time, urllib.error, urllib.request
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fxrates.py")
data = os.path.abspath(sys.argv[1]); work = tempfile.mkdtemp()
env = dict(os.environ, DATABASE_URL=os.path.join(work, "fx.db"))
JAN, FEB, BAD = "eurofxref-hist_2025-01.csv", "eurofxref-hist_2025-02-03_04.csv", "eurofxref-hist_bad.csv"
def sub(a): return a.replace("$DATA", data).replace("$WORK", work)
def cli(cid, *args):
    p = subprocess.run([sys.executable, REF, *[sub(a) for a in args]], env=env, capture_output=True, text=True)
    shown = " ".join(f'"{a}"' if "$" in a else a for a in args)
    if p.stdout: print(f"check {cid} {p.returncode} {shown} <<'EOF'\n{p.stdout}EOF")
    else: print(f"check {cid} {p.returncode} {shown} < /dev/null".replace("  <", " <"))
s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
server = None
def start():
    global server
    server = subprocess.Popen([sys.executable, REF, "serve", "--port", str(port)], env=env)
    time.sleep(1)
def http(cid, path):
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}{path}"); status, body = r.status, r.read()
    except urllib.error.HTTPError as e: status, body = e.code, e.read()
    if status == 200:
        print(f"http {cid} 200 '{path}' <<'EOF'\n{json.dumps(json.loads(body), separators=(',', ':'))}\nEOF")
    else:
        print(f"http {cid} {status} '{path}' < /dev/null")
try:
    for line in open(os.path.join(os.path.dirname(REF), "fx_checks.txt")):
        line = line.rstrip("\n")
        if not line or line.startswith("#"): print(line); continue
        kind, cid, *rest = line.split(" ")
        if kind == "cli": cli(cid, *rest)
        elif kind == "http": http(cid, rest[0])
        elif kind == "start": start(); print("start_server")
finally:
    if server: server.terminate()
