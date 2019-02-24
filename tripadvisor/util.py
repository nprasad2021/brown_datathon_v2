import pandas as pd
import datetime
import os
import time
import math
import numpy as np
import geocoder
import pickle

current_path = os.getcwd()

if "om" not in current_path:
    ACTIVITY_DATA = "activity_data.csv"
    HOTEL_DATA = "hotel_data.csv"


def create_rec_data(output_file):
    activity_df = pd.read_csv(ACTIVITY_DATA)
    hotel_df = pd.read_csv(HOTEL_DATA).set_index('hotel_id')
    activity_df.head()

    to_timestamp = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').timestamp()
    activity_df['timestamp'] = activity_df['date'].apply(to_timestamp)

    def encode(a):
        encodings = {'view': 1, 'price_click': 2, 'hotel_website_click': 3, 'booking': 4}
        return encodings[a]

    activity_df['user_action'] = activity_df['user_action'].apply(encode)
    activity_df = pandas.get_dummies(activity_df,columns = ['device', 'user_country'])
    activity_df = activity_df.drop(columns=['date', 'device'])

    hotel_df = hotel_df['hotel_name']

    df = activity_df.join(hotel_df, how='inner', on='hotel_id')
    df.head()

    len(df.user_id.unique()), len(df.hotel_id.unique())

    df.user_id = df.user_id.astype('category').cat.codes.values
    df.hotel_id = df.hotel_id.astype('category').cat.codes.values

    df.to_csv(output_file, index=False)
    return df


def create_sparse_matrix(output_file, replace=True):

    if os.path.exists(output_file) and not replace:
        return pd.read_csv(output_file)

    if not os.path.exists("dfdict.pkl") or replace:
        DISCOUNT = 90  # events become half as valuable after 3 months

        activity_df = pd.read_csv(ACTIVITY_DATA)
        hotel_df = pd.read_csv(HOTEL_DATA).set_index('hotel_id')

        names = {'parent_brand_name': ['Hyatt Hotels Corporation'
            , 'Preferred Hotel Group', 'Wyndham Hotel Group'
            , 'Choice Hotels International, Inc.', 'InterContinental Hotels Group PLC'
            , 'Hilton Worldwide', 'Marriott International, Inc.'],
                 'hotel_type': ['B&B', 'Hostel', 'Condo', 'Hotel']}

        def encode_values(data, feature_list):  # returns columns of one-hot-encoded data with preselected features
            keylist = []
            for key in feature_list.keys():
                if key in data.columns:
                    data.loc[(~data[key].isin(feature_list[key])) & (~data[key].isnull()), key] = 'other'
                    data.loc[data[key].isnull(), key] = 'null'
                    keylist.append(key)
            return pd.get_dummies(data, columns=keylist).select_dtypes('uint8')

        to_timestamp = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').timestamp()
        activity_df['timestamp'] = activity_df['date'].apply(to_timestamp)

        # PUT IN GEOLOCATOR LATER FOR HOTELS AND FOR USERS

        def encode(a):
            encodings = {'view': 1, 'price_click': 2, 'hotel_website_click': 3, 'booking': 4}
            return encodings[a]

        activity_df['user_action'] = activity_df['user_action'].apply(encode)
        activity_df = pd.get_dummies(activity_df, columns=['device','user_country'])
        activity_df['event_count'] = 1

        def geocode(a):
            g = geocoder.arcgis(a)
            return g.lat, g.lng

        # activity_df['usr_lat'], activity_df['usr_long'] = activity_df['user_country'].apply(geocode)
        activity_df = activity_df.drop(columns=['date'])

        current_time = time.time()
        decay = lambda coef, x: coef * math.e ** ((current_time - x) / -(86400000 * DISCOUNT / 0.693147181))
        cols = list(set(activity_df.columns) - set(['user_id', 'hotel_id', 'timestamp', 'event_count']))

        for col in cols:
            activity_df[col] = decay(activity_df[col], activity_df['timestamp'])

        # VECTOR EMBEDDING OF HOTEL NAME USING NLP AS FEATURE LATER ON
        hotel_df = hotel_df.join(encode_values(hotel_df, names))
        hotel_df = hotel_df.drop(columns=['brand_name'] + list(names.keys()))

        df = activity_df.join(hotel_df, how='inner', on='hotel_id')
        df = df.drop(columns=['timestamp'])
        df = df.groupby(['user_id', 'hotel_id']).sum()
        df['user_action'] = df['user_action'] / df['event_count']
        df.count()


        hotel_ids = list(set(df.index.get_level_values('hotel_id')))
        user_ids = list(set(df.index.get_level_values('user_id')))

        hotel_ids = np.random.choice(hotel_ids, size=1000)
        user_ids = np.random.choice(user_ids, size=25000)

        dfdict = df.to_dict(orient='index')
        print(type(dfdict), "type of dfdict")

        with open('dfdict.pkl', 'wb') as handle:
            pickle.dump(dfdict, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('hotel.pkl', 'wb') as handle:
            pickle.dump(hotel_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('users.pkl', 'wb') as handle:
            pickle.dump(user_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        print("using cached pre-computed files")
        with open('dfdict.pkl', 'rb') as handle:
            dfdict = pickle.load(handle)

        with open('hotel.pkl', 'rb') as handle:
            hotel_ids = pickle.load(handle)

        with open('users.pkl', 'rb') as handle:
            user_ids = pickle.load(handle)

    print(len(hotel_ids))
    print(len(user_ids))

    sparse_dict = {}

    for uid in user_ids:
        for hid in hotel_ids:
            sparse_dict[(uid, hid)] = 0
            if (uid, hid) in dfdict:
                try:
                    sparse_dict[(uid, hid)] = dfdict[(uid, hid)]['user_action']
                except:
                    print((uid, hid))


    keys = list(sparse_dict.keys()); print(type(keys))
    user_id, hotel_id = zip(*keys)

    user_action = [sparse_dict[(user_id[i], hotel_id[i])] for i in range(len(user_id))]

    d = {"user_id":list(user_id), "hotel_id":list(hotel_id), "user_action":list(user_action)}

    sparse_matrix = pd.DataFrame.from_dict(d)
    sparse_matrix.to_csv(output_file, index=False)

    return sparse_matrix







