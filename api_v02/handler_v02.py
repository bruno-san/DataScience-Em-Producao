# import pickle
import pickle
# import pandas
import pandas as pd
# import flask
from flask import Flask, request, Response
#import Rossmann class
from rossmann.Rossmann_v02 import Rossmann_v02

# load model
model = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/model/model_xgb_rossmann_v02.pkl', 'rb') )

# initialize API
app = Flask( __name__ )

# create endpoint (URL)
# Post method = send data in order to receive data.
@app.route( '/rossmann/predict', methods=['POST'] )
# function to get the received data
def rossmann_predict():
    test_json = request.get_json()
    
    #check received data (json)
    if test_json: # there is data
        if isinstance( test_json, dict): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
        
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() ) # keys = chaves do json. Serão as colunas do df.
        
        # Instantiate Rossmann class
        pipeline = Rossmann_v02()
        
        # data cleaning
        df1 = pipeline.data_cleaning( test_raw )
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 )
        
        return df_response
        
    else: # there is no data
        return Response( '{}', status=200, mimetype='application/json' )

# check main function in the script
if __name__ == '__main__':
    app.run( '127.0.0.1' ) # local host