import yfinance as yf

def pairEUR2USD():
    eur_usd = yf.Ticker("EURUSD=X")
    eur_usd_rate = eur_usd.history(period="1d")['Close'].iloc[-1]
    return eur_usd_rate

def pairUSD2EUR():
    usd_eur = yf.Ticker("USDEUR=X")
    usd_eur_rate = usd_eur.history(period="1d")['Close'].iloc[-1]
    return usd_eur_rate
