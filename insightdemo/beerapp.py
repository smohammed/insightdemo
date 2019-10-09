from flask import Flask,render_template,url_for,request, flash, redirect
import os
import csv
import pickle
import string
import numpy as np
import pandas as pd 
from operator import itemgetter
from wtforms import StringField
from nltk.corpus import stopwords
from insightdemo import flask_instance
from nltk.stem.wordnet import WordNetLemmatizer
from insightdemo.grababeer import *


@flask_instance.route('/', methods=['GET', 'POST'])
def homepage():
    print(request)
    keyword = request.args.get('userinput')
    if keyword is None:
        return render_template("model_input.html")

    print('using post method')
    print(keyword)
    #grababeer = getbeerrec(keyword)
    
    return render_template('model_output.html', result = grababeer)

'''
@flask_instance.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        return render_template("model_input.html")
'''

@flask_instance.route('/model_output')
def output():
    keyword = request.form.get('keyword')
    print(keyword)
    print('now on output page')
    return render_template('model_output.html', result=keyword)

if __name__ == '__main__':
    app.run(debug=True)