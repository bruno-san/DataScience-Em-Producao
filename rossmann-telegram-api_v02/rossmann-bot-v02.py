import os
import requests
import json
import pandas as pd

from flask import Flask, request, Response

# constants
TOKEN = '1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o'

# Info about the Bot
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/getMe
        
# get updates
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/getUpdates

# Webhook local host
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/setWebhook?url=https://e77b0b106c63.ngrok.io

# Webhook Heroku
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/setWebhook?url=https://rossmann-telegram-bot-v02.herokuapp.com

# Webhook Info
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/getWebhookInfo
        
# send message
#https://api.telegram.org/bot1193503727:AAHHZahjuvQVRS3VpTMt3CO1G1auTRTRF5o/sendMessage?chat_id=907910472&text=Hello Bruno, I am doing good, tks!

def send_message( chat_id, text ):
    url = 'https://api.telegram.org/bot{}/'.format( TOKEN )
    url = url + 'sendMessage?chat_id={}'.format( chat_id )
    # request in the API
    r = requests.post( url, json={'text': text })
    print( 'Status Code {}'.format( r.status_code ) )
    
    return None

def load_dataset( store_id ):
    # load test dataset
    df10 = pd.read_csv('test_customers.csv')
    df_store_raw = pd.read_csv('store.csv')

    # merge test dataset + store
    df_test = pd.merge( df10, df_store_raw, how='left', on='Store')

    # choose store for prediction
    df_test = df_test[df_test['Store'] == store_id ]
    
    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop( 'Id', axis=1 )

        # convert Dataframe to json
        data = json.dumps( df_test.to_dict( orient='records' ) )

    else:
        data = 'error'
        
    return data

def predict( data ):
    # API Call
    url = 'https://rossmann-model-v02.herokuapp.com/rossmann/predict' # endpoint heroku
    header = {'Content-type': 'application/json'}
    data = data

    # request
    r = requests.post( url, data=data, headers=header )
    print( 'Status Code {}'.format(r.status_code ) )

    # convert back to data frame
    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys())
    
    return d1

# get chat_id and store_id from sent message
def parse_message( message ):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    store_id = store_id.replace('/', '') # remove '/' from telegram message
    
    try:
        store_id = int( store_id ) # check if the store id from the message is a number
        
    except ValueError:
        store_id = 'error'
    
    return chat_id, store_id

# API initialize
app = Flask( __name__ )

# endpoint
# '/' means endpoint in the root
@app.route('/', methods=['GET', 'POST'] ) 
def index():
    if request.method == 'POST':
        message = request.get_json() # get message received
        
        chat_id, store_id = parse_message( message )
        
        if store_id != 'error':
            # loading data
            data = load_dataset( store_id )
            
            if data != 'error':
                # prediction
                d1 = predict( data )

                # calculation
                d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()
                
                # send message
                msg = 'Store Number {} will sell R$ {:,.2f} in the next 6 weeks.'.format( d2['store'].values[0], d2['prediction'].values[0] )
                
                send_message( chat_id, msg )
                return Response( 'Ok', status=200 )

            else:
                send_message( chat_id, 'Store Not Available' )
                return Response( 'Ok', status=200 )
            
        else:       
            send_message( chat_id, 'Invalid Store ID')
            return Response( 'Ok', status=200 ) # status response to API.
        
    else:
        return '<h1> Rossmann Telegram BOT </h1>' # 'GET' - html header message if the user accesses the endpoint

if __name__ == '__main__':
    port = os.environ.get( 'PORT', 5000 )
    app.run( host='0.0.0.0', port=port )