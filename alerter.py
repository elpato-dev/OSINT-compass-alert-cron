import requests
from dotenv import load_dotenv
import os

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
4 change_by
5 starting_score
6 contact_method
7 contact_details
'''

## for every row it checks if criteria is met and sends alert accordingly
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

            if row[6] == "telegram":
                send_telegram(message, row[7])