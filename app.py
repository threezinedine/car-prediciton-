import sklearn
from flask import Flask, render_template, request
import jsonify
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

with open ('random_forest_regression_model.pkl', 'rb') as file:
    model = pickle.load (file)

app = Flask (__name__)

@app.route ('/', methods = ['GET'])
def home ():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict ():
    if request.method == 'POST':
        Year = int (request.form['Year'])
        Present_Price = float (request.form ['Price'])
        Kms_Driven = float (request.form ['Kms_driven'])
        Owner = int (request.form ['Owner'])
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 0
        Seller_Type_Individual = 0
        Transmission_Manual = 0

        if request.form['Fuel'] == "Petrol":
            Fuel_Type_Petrol = 1
        elif request.form['Fuel'] == "Diesel":
            Fuel_Type_Diesel = 1

        if request.form ['Seller_type'] == "Individual":
            Seller_Type_Individual = 1

        if request.form ['Transmission'] == 'Manual':
            Transmission_Manual = 1

        output = model.predict ([[Present_Price, Kms_Driven, Owner, 2021 - Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round (output[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts = "Sorry I cannot predict the car's price")
        else:
            return render_template('index.html', prediction_texts = f"You can sell your car with price: {output} $")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)