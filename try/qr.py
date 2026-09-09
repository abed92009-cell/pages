import segno
url = "https://abed92009-cell.github.io/pages/try/w/"
q = segno.make(url, error='h')           # high correction: survives a phone screen and print
q.save("detter-try.png", scale=12, border=4, dark="#1c1c1a", light="#ffffff")
q.save("detter-try.svg", scale=12, border=4, dark="#1c1c1a", light="#ffffff")
print("encoded:", url)
print("version", q.version, "| error correction", q.error, "| symbol", q.symbol_size(scale=1))
