import pickle
import inflection
import pandas as pd
import numpy as np
import math
from datetime import datetime
from datetime import timedelta

class Rossmann_v02( object ):
    def __init__( self ):
        self.competition_distance_scaler        = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/competition_distance_scaler.pkl', 'rb' ) )
        self.competition_time_month_scaler      = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/competition_time_month_scaler.pkl', 'rb' ) )
        self.competition_open_since_year_scaler = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/competition_open_since_year_scaler.pkl', 'rb' ) )
        self.customers_scaler                   = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/customers_scaler.pkl', 'rb' ) )
        self.promo_time_week_scaler             = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/promo_time_week_scaler.pkl', 'rb' ) )
        self.year_scaler                        = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/year_scaler.pkl', 'rb' ) )
        self.promo2_since_year_scaler           = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/promo2_since_year_scaler.pkl', 'rb' ) )
        self.store_type_scaler                  = pickle.load( open( 'C:/Users/santo/repos/DataScience-Em-Producao/parameter02/store_type_scaler.pkl', 'rb' ) )
    
    def data_cleaning( self, df1 ):
        
        ## 1.1. Rename Columns
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday',
                   'SchoolHoliday', 'Customers', 'StoreType', 'Assortment',
                   'CompetitionDistance', 'CompetitionOpenSinceMonth',
                   'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek',
                   'Promo2SinceYear', 'PromoInterval']

        # Apply snakecase to columns names - letras minusculas. Nomes compostos separados por "_".
        snakecase = lambda x: inflection.underscore( x )
        cols_new = list(map(snakecase, cols_old))

        #rename
        df1.columns = cols_new

        ## 1.3. Data Types
        df1['date'] = pd.to_datetime( df1['date'] )

        ## 1.5. Fillout NA
        #competition_distance
        # market analysis assumption: position without values means a far competition distance, higher than the
        # maximum value from the raw data.
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x: 200000.0 if math.isnan(x) else x)

        # competition_open_since_month
        # Assumption: for NA values apply the value from "date" column, because the competition does exist and it can affect
        # over time the sales performance.
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)

        #competition_open_since_year
        # Same assumption as competition_open_since_month
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)

        #promo2_since_week
        # Assumptions: 1. NA values mean the store did not take place in promo2. 2. apply the value from "date" column.
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)

        #promo2_since_year
        # Same assumption as promo2_since_week
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)
        
        # Fill NA values with zero.
        df1['promo_interval'].fillna(0, inplace=True)

        ## 1.6. Change Types

        # change competition_open_since_month type to int
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype('int64')

        # change competition_open_since_year type to int
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype('int64')

        # change promo2_since_week type to int
        df1['promo2_since_week'] = df1['promo2_since_week'].astype('int64')

        # change promo2_since_year type to int
        df1['promo2_since_year'] = df1['promo2_since_year'].astype('int64')
        
        # change customers type to int
        df1['customers'] = df1['customers'].astype('int64')
        
        return df1

    
    def feature_engineering( self, df2 ):
        
        # year
        df2['year'] = df2['date'].dt.year

        # month
        df2['month'] = df2['date'].dt.month

        # day
        df2['day'] = df2['date'].dt.day

        # week of year
        df2['week_of_year'] = df2['date'].dt.weekofyear

        # year week
        df2['year_week'] = df2['date'].dt.strftime( '%Y-%W' )

        # competition since
        # Bring together competition_open_since_month and competition_open_since_year
        # Assumption: day = 1 in order to consider the full month.
        df2['competition_since'] = df2.apply( lambda x: datetime( year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1 ), axis=1)

        # Calculate the difference between date and competition_since. divide by 30 to keep the monthly granularity.
        df2['competition_time_month'] = (( df2['date'] - df2['competition_since'] )/30 ).apply( lambda x: x.days ).astype( int )

        # promo since
        # 1. Create a string 'year-week'
        df2['promo_since'] = df2['promo2_since_year'].astype( str ) + '-' + df2['promo2_since_week'].astype( str )
        # 2. transform the string to date format ('year-month-day'). The day represents the first day of the week.
        df2['promo_since'] = df2['promo_since'].apply( lambda x: datetime.strptime( x + '-1', '%Y-%W-%w' ) - timedelta( days=7) )
        # 3. create promo_time_week column with the difference between date and promo_since in weeks.
        # df2['date'] - df2['promo_since'] divided by 7 beacuse we want it in weeks.
        df2['promo_time_week'] = ( ( df2['date'] - df2['promo_since'] )/7 ).apply( lambda x: x.days).astype( int )

        # assortment
        df2['assortment'] = df2['assortment'].apply( lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended')

        # state holiday
        df2['state_holiday'] = df2['state_holiday'].apply( lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day')

        # 3.0. STEP 03 - VARIABLES FILTERING

        ## 3.1. Line Filtering
        # closed stores (open = 0) means no sales. Therefore, it is not relevant for the sales forecast model. Open = 0 will be removed.
        # sales = 0 will also be removed.
        df2 = df2[df2['open'] != 0]

        ## 3.2. Columns Selection

        # Customers is a variable that is not available at the time of prediction, hence it is a business restriction.
        # To use Customers variable, a new project is needed only for customers forecast in the next 6 weeks, and then use it as input in this sales forecast project.
        # Therefore, the column customers must be removed.
        # open only has values = 1(the lines with zeros were deleted above), hence the column can be removed.
        # promo_interval generated new columns in the feature engineering step and is no longer needed.
        # month_map is an auxiliary column and hence will be removed.
        cols_drop = ['open', 'promo_interval']
        df2 = df2.drop( cols_drop, axis=1 )
        
        return df2


    def data_preparation( self, df5 ):

        ## 5.2. Rescaling
        # competition distance
        df5['competition_distance'] = self.competition_distance_scaler.fit_transform( df5[['competition_distance']].values )

        # competition_time_month
        # Apply RobustScaler due to the presence of outliers.
        df5['competition_time_month'] = self.competition_time_month_scaler.fit_transform( df5[['competition_time_month']].values )
       
        # competition_open_since_year
        df5['competition_open_since_year'] = self.competition_open_since_year_scaler.fit_transform( df5[['competition_open_since_year']].values ) 
    
        # customers
        df5['customers'] = self.customers_scaler.fit_transform( df5[['customers']].values )
    
        # promo_time_week
        # The boxplot graph shows a low outlier influence, hence the MinMaxScaler will be applied.
        df5['promo_time_week'] = self.promo_time_week_scaler.fit_transform( df5[['promo_time_week']].values )
        
        # year - apply MinMaxScaler
        df5['year'] = self.year_scaler.fit_transform( df5[['year']].values )
        
        # promo2_since_year
        df5['promo2_since_year'] = self.promo2_since_year_scaler.fit_transform( df5[['promo2_since_year']].values )


        ### 5.3.1. Encoding

        # state_holiday - apply one-hot encoding with get_dummies from pandas
        df5 = pd.get_dummies( df5, prefix=['state_holiday'], columns=['state_holiday'] )

        # store_type - apply label encoding
        df5['store_type'] = self.store_type_scaler.fit_transform( df5['store_type'] )

        # assortment - apply ordinal encoding
        # dictionary does not need to be pickled because dictionary can be created in deploy.
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map( assortment_dict )

        ### 5.3.3. Nature Transformation

        # Tranformation application: Cyclic Nature Transformation with sin and cos
        # month
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * (2. * np.pi/12 ) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * (2. * np.pi/12 ) ) )

        # day
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * (2. * np.pi/30 ) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * (2. * np.pi/30 ) ) )

        # week of year
        df5['week_of_year_sin'] = df5['week_of_year'].apply( lambda x: np.sin( x * (2. * np.pi/52 ) ) )
        df5['week_of_year_cos'] = df5['week_of_year'].apply( lambda x: np.cos( x * (2. * np.pi/52 ) ) )

        # day of week
        df5['day_of_week_sin'] = df5['day_of_week'].apply( lambda x: np.sin( x * (2. * np.pi/7 ) ) )
        df5['day_of_week_cos'] = df5['day_of_week'].apply( lambda x: np.cos( x * (2. * np.pi/7 ) ) )
        
        # competition_open_since_month
        df5['competition_open_since_month_sin'] = df5['competition_open_since_month'].apply( lambda x: np.sin( x * (2. * np.pi/12 ) ) )
        df5['competition_open_since_month_cos'] = df5['competition_open_since_month'].apply( lambda x: np.cos( x * (2. * np.pi/12 ) ) )

        # promo2_since_week
        df5['promo2_since_week_sin'] = df5['promo2_since_week'].apply( lambda x: np.sin( x * (2. * np.pi/52 ) ) )
        df5['promo2_since_week_cos'] = df5['promo2_since_week'].apply( lambda x: np.cos( x * (2. * np.pi/52 ) ) )
        
        
        
        cols_selected = ['store','customers', 'promo', 'store_type', 'assortment', 'competition_distance',
                         'competition_open_since_year', 'promo2', 'promo2_since_year', 'competition_time_month',
                         'promo_time_week', 'day_of_week_sin', 'day_of_week_cos', 'day_sin', 'day_cos',
                         'month_sin', 'month_cos', 'week_of_year_sin', 'week_of_year_cos',
                         'competition_open_since_month_sin', 'competition_open_since_month_cos',
                         'promo2_since_week_sin', 'promo2_since_week_cos']
        
        return df5[ cols_selected ]
    
    def get_prediction( self, model, original_data, test_data ):
        # prediction
        pred = model.predict( test_data )
        
        # join pred into the original data
        original_data['prediction'] = np.expm1( pred )
        
        return original_data.to_json( orient='records', date_format='iso' )