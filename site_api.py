import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def translate_text(text: str, lang_in: str, lang_out: str) -> str:
    url = os.getenv('url')
    payload = "q= {0}&target={1}&source={2}".format(text, lang_out, lang_in)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": os.getenv('API-Key'),
        "X-RapidAPI-Host": os.getenv('API-Host')
    }

    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers).json()

    return response['data']['translations'][0]['translatedText']
