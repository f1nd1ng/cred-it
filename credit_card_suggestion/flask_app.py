from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import requests

app = Flask(__name__)
CORS(app)

# Load the dataset
df = pd.read_csv("final.csv")

# Function to calculate credit card scores
def calculate_score(df, user_income, is_salaried, user_expenditure):
    df = df.copy()
    income_col = "Minimum Salaried Income" if is_salaried else "Minimum ITR for Self Employed"
    
    df = df[df[income_col] <= user_income]

    total_expenditure = sum(user_expenditure.values())
    df["Adjusted Annual Fee"] = np.where(df["annual fee waiver"] <= total_expenditure, 0, df["Renewal Fee"])
    
    category_columns = ["shopping", "travel", "dining", "movies", "fuel", "food", "bill payment", "stays", "business expenses"]
    
    df["Expenditure Match"] = sum(df[cat] * user_expenditure.get(cat, 0) for cat in category_columns)

    df["Score"] = (
        np.log(df[income_col] + 1) 
        - 0.001 * df["Joining Fee"] 
        - 0.002 * df["Adjusted Annual Fee"] 
        + df["welcome scores"]
        + df["Expenditure Match"]
    )

    return df.sort_values(by="Score", ascending=False)[
    ["Card Name", "Bank Name", "Joining Fee", "Renewal Fee", "Minimum Salaried Income", 
     "annual fee waiver", "Score"]
    ].reset_index(drop=True)  # Reset index to avoid JSON format issues


# Function to fetch financial data (income + expenditure) from Django
def fetch_financial_data(user_id, token):
    django_url = f"http://127.0.0.1:8000/api/transactions/user_financials/{user_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(django_url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("annual_income", 0), data.get("expenditure", {})
    except requests.exceptions.RequestException:
        pass
    
    return 0, {} 

# API route to get top 5 credit cards
@app.route('/top-cards', methods=['POST'])
def get_top_cards():
    data = request.json
    user_id = data.get("user_id")
    token = data.get("token")
    is_salaried = data.get("salaried", "true").lower() == "true"

    # Fetch user's annual income & expenditure data
    user_income, user_expenditure = fetch_financial_data(user_id, token)
    
    filtered_df = calculate_score(df, user_income, is_salaried, user_expenditure)
    
    return jsonify(filtered_df.head(5).to_dict(orient="records"))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
