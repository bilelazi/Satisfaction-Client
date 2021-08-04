import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import warnings
import pickle

train = pd.read_csv("C:/Users/info-tech/data.csv")
train.rename(columns = {'Gender' : 'gender', 'Customer Type': 'customer_type', 'Age' : 'age', 
                           'Type of Travel': 'travel_type', 'Class': 'class', 
                           'Flight Distance': 'flight_distance', 
                           'Inflight wifi service': 'wifi_service',
                           'Departure/Arrival time convenient': 'departure_n_arrival_time_convenient', 
                           'Ease of Online booking' : 'easy_onlinebooking',
                           'Gate location' : 'gate_location', 'Food and drink' : 'food_n_drink', 
                           'Online boarding' : 'online_boarding', 'Seat comfort': 'seat_comfort',
                           'Inflight entertainment' : 'inflight_entertainment', 
                           'Baggage handling' : 'baggage_handling',
                           'Inflight service' : 'inflight_service','Cleanliness' : 'cleanliness',
                           'Departure Delay in Minutes': 'departure_delay_min', 
                           'Arrival Delay in Minutes' : 'arrival_delay_minutes',
                           'satisfaction' : 'satisfaction'}, inplace= True)
train.drop(columns = ["Unnamed: 0","id","gender","customer_type","age","travel_type","class","flight_distance","online_boarding","On-board service"
                     ,"Leg room service","Checkin service","Date","departure_delay_min","arrival_delay_minutes"], axis = 1, inplace= True)   
                     
used_data = train.drop(['satisfaction'], axis=1)
x = used_data.values
y = train['satisfaction']

x_train, x_test, y_train, y_test = train_test_split (x, y, test_size=0.3, random_state=42)

cb = CatBoostClassifier(learning_rate= 0.1, l2_leaf_reg= 4, iterations= 300, depth= 10)
cb.fit(x_train, y_train)

pickle.dump(cb,open('model.pkl','wb'))