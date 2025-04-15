from flask import Flask, request, jsonify, render_template
import os
import joblib

app = Flask(__name__)

# Modell lokal laden (nicht von Azure!)
model = joblib.load("hotel_price_prediction_model.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        score = float(data['score'])
        reviews_count = int(data['reviews_count'])
        prediction = model.predict([[score, reviews_count]])
        return jsonify({'predicted_price': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)