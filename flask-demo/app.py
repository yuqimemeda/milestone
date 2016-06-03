from flask import Flask, render_template, request, redirect, url_for
from pandas import *
import pandas
import numpy as np
import json
import requests
import time
from datetime import *
from bokeh.plotting import *
from bokeh import embed
import cgi
from bokeh.embed import components 

#build the app
app = Flask(__name__)
#selector
app.vars={}
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html')
def plotting():
    
    # get list of the checked features
    features = request.form.getlist('feature')
    #user's input
    ticker = request.form['ticker']
    #calculate the time one month before
    now = datetime.now()
    #calculate the time difference
    start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    #fetch the dataset
    URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=WVEFZw8uyJzuvHE3VsQW'
    r = requests.get(URL)
    
    
    #pass to pandas dataframe
    raw_data = DataFrame(r.json())
    #clean up the data
    df = DataFrame(raw_data.ix['data','dataset'] , columns = raw_data.ix['column_names','dataset'])
    #set the column names with lower case
    df.columns = [x.lower() for x in df.columns]
    #set the index to the date column
    df = df.set_index(['date'])
    #convert the index to datetime 
    df.index = to_datetime(df.index)
    
    #create the plot
    p = figure(x_axis_type = "datetime")
    if 'open' in features:
        p.line(df.index, df['open'], color='blue', legend='opening price')
    if 'high' in features:
        p.line(df.index, df['high'], color='red', legend='highest price')
    if 'close' in features:
        p.line(df.index, df['close'], color='green', legend='closing price')
    return p

@app.route('/chart_page',methods=['GET','POST'])
def chart():
    plot = plotting()
    script, div = embed.components(plot)
    return render_template('bokeh.html', script=script, div=div)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
 
    #app.run(debug=True)