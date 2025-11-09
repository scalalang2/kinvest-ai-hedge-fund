from pykrx import stock

def main():
    for ticker in stock.get_market_ticker_list():
        종목 = stock.get_market_ticker_name(ticker)
        print(ticker, 종목)


if __name__ == "__main__":
    main()