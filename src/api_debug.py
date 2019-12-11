from currency_viewer import currency_viewer as cv

a = cv.CurrencyViewer()
a.processCViewer(log=True, currency="USD", time="rfc1123")

print(a)