from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from xgboost import XGBClassifier

app = Flask(__name__)

# Load XGBoost model
model = XGBClassifier()
model.load_model("fraud_detection_model.json")

# Load Label Encoder
encoder = joblib.load("label_encoder.pkl")


# ---------------- DASHBOARD ----------------

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ---------------- PREDICTION ----------------

@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Get data from frontend
        data = request.get_json()

        # Read values
        transaction_type = data["type"]
        amount = float(data["amount"])
        old_balance_org = float(data["oldbalanceOrg"])
        new_balance_org = float(data["newbalanceOrig"])
        old_balance_dest = float(data["oldbalanceDest"])

        # Encode transaction type
        encoded_type = encoder.transform([transaction_type])[0]

        # Create input for ML model
        input_data = pd.DataFrame([{
            "step": 1,
            "type": encoded_type,
            "amount": amount,
            "oldbalanceOrg": old_balance_org,
            "newbalanceOrig": new_balance_org,
            "oldbalanceDest": old_balance_dest,
            "newbalanceDest": old_balance_dest,
            "isFlaggedFraud": 0
        }])

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Prediction probability
        probability = model.predict_proba(input_data)[0][1]

        if prediction == 1:
            result = "Fraud Transaction"
        else:
            result = "Genuine Transaction"

        return jsonify({
            "success": True,
            "prediction": int(prediction),
            "result": result,
            "fraud_probability": round(float(probability) * 100, 2)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# ---------------- SIDEBAR PAGES ----------------

@app.route("/fraud-detection")
def fraud_detection():
    return render_template("fraud_detection.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/model-status")
def model_status():
    return render_template("model_status.html")


@app.route("/api-status")
def api_status():
    return render_template("api_status.html")


# ---------------- START FLASK ----------------

if __name__ == "__main__":
    app.run(debug=True)