import io, zipfile
from unittest.mock import patch
from services.rates import load_text, RejectedFile, fetch

def test_load_text_validates_and_preserves_rate_text():
    dates, rates = load_text('Date,USD,JPY,\n2025-01-02,1.00,N/A,\n')
    assert dates == {'2025-01-02'}
    assert rates == [('2025-01-02','USD','1.00')]

def test_load_text_rejects_invalid_rate():
    try: load_text('Date,USD,\n2025-01-02,1.x,\n')
    except RejectedFile: pass
    else: assert False

def test_fetch_uses_archive_csv():
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z: z.writestr('eurofxref-hist.csv','Date,ZZZ,\n2099-01-02,0.943,\n')
    class Response:
        def read(self): return buf.getvalue()
        def __enter__(self): return self
        def __exit__(self,*a): pass
    with patch('urllib.request.urlopen',return_value=Response()):
        # exercise extraction and validation, persistence uses configured DB
        assert fetch()==(1,1)
