from flask import Flask,render_template,url_for,request, flash, redirect
import pandas as pd 
import numpy as np
import pickle
import string
import csv
from insightdemo import flask_instance

@flask_instance.route('/')
def homepage():
    return render_template("model_input.html")

'''
@app.route('/predict',methods=['POST'])
def predict():
    
    df=pd.read_csv('df_vect.csv', index_col=0)
    df.replace(' ', np.nan, inplace=True)
    df.dropna(inplace=True)
    y = df['phq']
    X = df['alltext']
    
    cv = TfidfVectorizer(ngram_range = (1,3))
    X = cv.fit_transform(X) # Fit the Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    lr = LinearRegression()
    lr.fit(X_train,y_train)

           
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = lr.predict(vect)
        predictions.append(my_prediction)
        field = ['PHQ Score', 'Response']
        with open('fulfilled_predictions.csv','a', newline= "") as inFile:
            writer = csv.DictWriter(inFile, fieldnames=field)
            writer.writerow({'Response': message, 'PHQ Score': my_prediction})
    return render_template('results2.html',prediction = my_prediction)
'''


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)