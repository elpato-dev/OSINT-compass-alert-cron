import requests
from dotenv import load_dotenv
import os
import asyncio

#import modules
from postgreser import get_alerts
from telegramer import send_telegram

load_dotenv()

api_key = os.getenv('OSINT_COMPASS_API_KEY')

## get all alerts from database
rows = get_alerts()
'''
0 id
1 term
2 scorelt
3 scoregt
4 contact_method
5 contact_details
'''

async def send_alerts():
    for row in rows:
        term = row[1]

        ##request to compass API 
        compass_response = requests.get("https://osint-compass-api.onrender.com/term?term=" + term + "&apikey=" + api_key)
        compass_json = compass_response.json()
        twitter_sentiment = round(compass_json["tweets"]["sentiment"],3)
        news_sentiment = round(compass_json["news"]["sentiment"], 3)

        if row[2] != None:
            scorelt = row[2]
            if twitter_sentiment < scorelt or news_sentiment < scorelt:
        
                message = "Alert was triggered for term: '"+ term + "' the sentiment score is lower than " + str(scorelt) +" Twitter score is:" + str(twitter_sentiment) + " and news score is:" + str(news_sentiment)

                if row[4] == "telegram":
                    await send_telegram(message, row[5])
        
        if row[3] != None:
            scoregt = row[3]
            if twitter_sentiment > scoregt or news_sentiment > scoregt:
        
                message = "Alert was triggered for term: '"+ term + "' the sentiment score is greater than " + str(scoregt) +" Twitter score is:" + str(twitter_sentiment) + " and news score is:" + str(news_sentiment)

                if row[4] == "telegram":
                    await send_telegram(message, row[5])