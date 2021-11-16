from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIxMTAxODA4MTkiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDQ4TVI3IiwiaWQiOiJJQk1pZC01NTAwMDQ4TVI3IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNGFlZTFjYTAtZmMyNi00NDkyLTk2MDktNTUzZWJjZjYxNTUwIiwiaWRlbnRpZmllciI6IjU1MDAwNDhNUjciLCJnaXZlbl9uYW1lIjoiU2FoYW5hIiwiZmFtaWx5X25hbWUiOiJMIEIiLCJuYW1lIjoiU2FoYW5hIEwgQiIsImVtYWlsIjoic2FoYW5hbGI5OUBnbWFpbC5jb20iLCJzdWIiOiJzYWhhbmFsYjk5QGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InNhaGFuYWxiOTlAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNTUwMDA0OE1SNyIsIm5hbWUiOiJTYWhhbmEgTCBCIiwiZ2l2ZW5fbmFtZSI6IlNhaGFuYSIsImZhbWlseV9uYW1lIjoiTCBCIiwiZW1haWwiOiJzYWhhbmFsYjk5QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6IjNmMWM4ZThhZGU3MTRmZGVhZmQwYjk1ZjFhNjRhOTdkIiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjM3MDMzNDk3LCJleHAiOjE2MzcwMzcwOTcsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.VGvP36n7UcaYvQ0wJZTr06zpx5ggMaPT2wSQnYD4Ts9ccl1E0_FyFNNpm8oB0k8BSy-3AT0j-B6tBNKCyRBurEQypSvU3fZITKDmbmpL2QODH5BKNK7VzNLTSwXR47852x1R2NtRffA_3Hf9SeDKzM0zZUUWQsTccXZQHujK6LZUydojDwM7i0juuaLC4x8JI5Wz_rCxowkacrITL-wSmqdsyxSS06_fUyYFYcLYDUk4FtNpDmUGtFrDLZoysX1RBtWP940FoKi2h8ayZZqVBjYVtkw6UPihBPc7YcR_XIPLcVbTbXoWQuRW3wFmvHs2VeLOM7o6YCZ5UhWFQSQvAQ"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3baa72a2-8a2b-44e5-80de-b80db092d879/predictions?version=2020-09-01", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)