# import os
import os
# import pickle
import pickle
# import pandas
import pandas as pd
# import flask
from flask import Flask, request, Response
#import Rossmann class
from rossmann.Rossmann import Rossmann

# load model
model = pickle.load( open( 'model/model_xgb_rossmann.pkl', 'rb') )

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
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
        
        # Instantiate Rossmann class
        pipeline = Rossmann()
        
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
    port = os.environ.get( 'PORT', 5000 )
    app.run( host = '0.0.0.0', port=port ) # local host