from pykis import PyKis
from dotenv import load_dotenv

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
    chart = kis.stock("000660").chart("5d", period=60)
    print(chart)

if __name__ == "__main__":
    main()