from flask import Flask,render_template,url_for,request, flash, redirect
import pandas as pd 
import numpy as np
import pickle
import string
import csv
from insightdemo import flask_instance
from wtforms import StringField
#import grababeer


@flask_instance.route('/')
def homepage():
    return render_template("model_input.html")

'''
@flask_instance.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        return render_template("model_input.html")
'''

@flask_instance.route('/model_output')
def output():
    return render_template('model_output.html')

'''
@flask_instance.route('/', methods=['GET', 'POST'])
def homepage():
    search = StringField('')
    if request.method == 'POST':
        return search_results(search)
    return render_template('model_input.html', form=search)

@flask_instance.route('/model_output', methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        return search_results(search)
    return render_template('model_output.html', form=search)
'''

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)