from flask import flask,request,jsonify,render_template 
import pandas as pd  
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

application = flask(__name__)
app = application






# import ridge regressor and standard scaler pickle files
ridge_model=pickle.load(open('models/ridge.pkl','rb'))
scaler=pickle.load(open('models/scaler.pkl','rb'))










@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()