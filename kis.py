import math

from pykis import PyKis
from dotenv import load_dotenv

import pandas as pd
import os

def create_kis():
    kis_id = os.getenv("KIS_ID")
    mode = os.getenv("KIS_MODE", "VIRTUAL").upper()
    if mode == "PROD":
        account = os.getenv("KIS_PROD_ACCOUNT")
    else:
        account = os.getenv("KIS_VIRTUAL_ACCOUNT")
        
    prod_app_key = os.getenv("KIS_PROD_APP_KEY")
    prod_secret_key = os.getenv("KIS_PROD_APP_SECRET")
    virtual_app_key = os.getenv("KIS_VIRTUAL_APP_KEY")
    virtual_secret_key = os.getenv("KIS_VIRTUAL_APP_SECRET")

    kis = PyKis(
        id=kis_id,
        account=account,
        appkey=prod_app_key,
        secretkey=prod_secret_key,
        virtual_id=kis_id,
        virtual_appkey=virtual_app_key,
        virtual_secretkey=virtual_secret_key,
        keep_token=True,
    )

    return kis

def main():
    load_dotenv()

    kis = create_kis()
    chart = kis.stock("000660").chart("1y", period="week")
    bar_data = [
        {
            "시간": b.time_kst,
            "시가": int(b.open),
            "고가": int(b.high),
            "저가": int(b.low),
            "종가": int(b.close),
            "거래량": int(b.volume),
            "등략율": math.floor((b.change / b.prev_price) * 10000) / 100 if b.prev_price != 0 else 0,
        }
        for b in chart.bars
    ]

    df = pd.DataFrame(bar_data)
    print(df.to_string())


if __name__ == "__main__":
    main()