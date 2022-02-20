import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Predykcja zużycia energii!
Czy dzisiaj grozi nam przeciążenie sieci?
""")
st.sidebar.header('Parametry do wyboru:')

def user_input_features():
    Day_of_year = st.sidebar.slider('Day of year', 1, 366)
    Kitchen = st.sidebar.slider('Kitchen',0.0, 11.1780, 2.0)
    Laundry = st.sidebar.slider('Laundry', 0.0,12.1090, 3.0)
    Heater = st.sidebar.slider('Heater', 0.0, 23.7430, 4.0)
    data = {'Day_of_year': Day_of_year,
            'Kitchen': Kitchen,
            'Laundry': Laundry,
            'Heater': Heater}
    features = pd.DataFrame(data, index=[0])
    return features

user_input = user_input_features()

df =  pd.read_csv("data_app.csv", sep = ",", low_memory=False)

X = df[['Day_of_year','Kitchen','Laundry','Heater']]
Y = df['target']

clf = RandomForestClassifier()
clf.fit(X, Y)

prediction = clf.predict(user_input)
prediction_proba = clf.predict_proba(user_input)

st.subheader('Klasy wraz z ich prawdopodobieństwem:')
st.write(df['target'].drop_duplicates().reset_index(drop=True))

st.subheader('Predykcja szczytu zużycia energii:')
st.write(prediction[0])

st.subheader('Prawdopodobieństwo klasyfikacji:')
st.write(prediction_proba)