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
    grababeer = getbeerrec(keyword)
    grabbeer = grababeer[0]
    grabbrew = grababeer[1]
    grabstyle = grababeer[2]

    grab1 = 'Your 1ST ROUND draft pick is: '+grabbeer[0]+' from '+grabbrew[0]
    grab2 = 'Your 2ND ROUND draft pick is: '+grabbeer[1]+' from '+grabbrew[1]
    grab3 = 'Your 3RD ROUND draft pick is: '+grabbeer[2]+' from '+grabbrew[2]
    grab4 = 'Your 4TH ROUND draft pick is '+grabbeer[3]+' from '+grabbrew[3]
    grab5 = 'Your 5TH ROUND draft pick is '+grabbeer[4]+' from '+grabbrew[4]
    grab6 = 'Your 6TH ROUND draft pick is '+grabbeer[5]+' from '+grabbrew[5]
    grab7 = 'Your 7TH ROUND draft pick is '+grabbeer[6]+' from '+grabbrew[6]

    return render_template('model_output.html', result1=grab1, result2=grab2, result3=grab3, result4=grab4, result5=grab5, result6=grab6, result7=grab7)

'''
@flask_instance.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        return render_template("model_input.html")

@flask_instance.route('/model_output')
def output():
    keyword = request.form.get('keyword')
    print(keyword)
    print('now on output page')
    return render_template('model_output.html', result=keyword)
'''


if __name__ == '__main__':
    app.run(debug=True)