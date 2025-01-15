from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

# Replace with your Azure ML endpoint URL and API key
endpoint_url = "https://mlproject-cgukz.uksouth.inference.ml.azure.com/score"
api_key = "35TggteAJSvZy9d2F8gLwfOtEhlsnusc"

@app.route("/")
def home():
    return render_template("salary_prediction.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Collect form data
    data = {
        "input_data": {
            "columns": ["Age", "Gender", "Education Level", "Job Title", "Years of Experience"],
            "data": [[
                int(request.form["Age"]),
                request.form["Gender"],
                request.form["Education Level"],
                request.form["Job Title"],
                int(request.form["Years of Experience"])
            ]]
        }
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    
    # Send request to Azure ML endpoint
    try:
        response = requests.post(endpoint_url, headers=headers, json=data)
        prediction = response.json().get("predictions", "No prediction returned")
    except Exception as e:
        prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
