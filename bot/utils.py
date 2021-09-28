import yfinance as yf

def evan_voyager():
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info['currentPrice'])
    d = (price - 16) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d),2)
    return f"Evan has {t} ${d} from Voyager."