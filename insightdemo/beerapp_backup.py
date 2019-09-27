from flask import render_template
from insightdemo import app
from insightdemo.a_model import ModelIt
import pandas as pd
from flask import request

# here's the homepage
@app.route('/')
def homepage():
    return render_template("firstpage.html")

# example page for linking things
@app.route('/example_linked')
def linked_example():
    return render_template("example_linked.html")

#here's a page that simply displays the births data
@app.route('/example_dbtable')
def birth_table_page():
    births = []
    # let's read in the first 10 rows of births data - note that the directory is relative to run.py
    dbname = './flaskexample/static/data/births2012_downsampled.csv'
    births_db = pd.read_csv(dbname).head(10)
    # when passing to html it's easiest to store values as dictionaries
    for i in range(0, births_db.shape[0]):
        births.append(dict(index=births_db.index[i], attendant=births_db.iloc[i]['attendant'],
                           birth_month=births_db.iloc[i]['birth_month']))
    # note that we pass births as a variable to the html page example_dbtable
    return render_template('/example_dbtable.html', births=births)

# now let's do something fancier - take an input, run it through a model, and display the output on a separate page

@app.route('/model_input')
def birthmodel_input():
   return render_template("model_input.html")

@app.route('/model_output')
def birthmodel_output():
   # pull 'birth_month' from input field and store it
   patient = request.args.get('birth_month')

   # read in our csv file
   dbname = './flaskexample/static/data/births2012_downsampled.csv'
   births_db = pd.read_csv(dbname)

   # let's only select cesarean births with the specified birth month
   births_db = births_db[births_db['delivery_method'] == 'Cesarean']
   births_db = births_db[births_db['birth_month'] == patient]

   # we really only need the attendant and birth month for this one
   births_db = births_db[['attendant', 'birth_month']]

   # just select the Cesareans  from the birth dtabase for the month that the user inputs
   births = []
   for i in range(0, births_db.shape[0]):
      births.append(dict(index=births_db.index[i], attendant=births_db.iloc[i]['attendant'],
                        birth_month=births_db.iloc[i]['birth_month']))
   the_result = ModelIt(patient, births)
   return render_template("model_output.html", births=births, the_result=the_result)
