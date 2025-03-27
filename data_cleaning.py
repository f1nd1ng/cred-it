import pandas as pd
import numpy as np

df = pd.read_csv("final.csv")

df.head()

df = df.drop(columns=["Unnamed: 0"])

df.to_csv("final.csv", index=False)

df = pd.read_csv("final.csv")

df.head()

print(df.info())  

print(df.describe())  

print(df.isnull().sum()) 

df = df.dropna(subset=[col for col in df.columns if col != "Welcome Benefits"])

print(df.isnull().sum()) 

checker = df[(df["Renewal Fee"] == 0) & (df["annual fee waiver"] != 0)]
print(checker)

df.loc[df["Renewal Fee"] == 0, "annual fee waiver"] = 0

checker = df[(df["Renewal Fee"] == 0) & (df["annual fee waiver"] != 0)]
print(checker)

print(df.duplicated().sum())

print(df[df.duplicated(keep=False)])

df = df.drop_duplicates(keep="first")

print(df[df.duplicated(keep=False)])

df.head(15)

df = df.reset_index(drop=True)

df.head(10)

df.tail()

df.dtypes

df['Minimum Salaried Income'].value_counts()

df['Minimum ITR for Self Employed'].value_counts()

import google.generativeai as genai 

genai.configure(api_key="AIzaSyCOUJOesMbTUQZqN-************")

models = genai.list_models()
for m in models:
    print(m.name)

benefits_list = df["Welcome Benefits"].dropna().tolist()

print(len(benefits_list))
print(benefits_list[:202]) 

def get_monetary_values(benefits):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
    "Estimate the total monetary value (in INR) of the following credit card welcome benefits. "
    "If multiple benefits are present, sum their values. Follow these rules:"
    "  if Cashback or direct statement credit → Use the exact amount."
    " if Reward points → Convert using 1 point ≈ 0.25 INR."
    "if Vouchers (e.g., Amazon, Flipkart, Taj, etc.) → Approximate their market value using online references for similar vouchers."
    " if Complimentary services (hotel stays, lounge access, memberships, etc.) → Estimate their value based on typical market prices."
    " If a benefit has no clear monetary value then try estimating its value from online sources.\n\n"
    "For each card, return the total estimated value in INR and assign a score from 1 to 10 based on its overall worth:"
    "- **1** = Minimal value (~0-500 INR)\n"
    "- **5** = Moderate value (~2000-5000 INR)\n"
    "- **10** = Extremely high value (~20,000+ INR)\n\n"
    "If multiple benefits are included in one card, add their values accordingly. Format your response strictly as:"
    "`Estimated Value: <total_amount>, Score: <score>`\n\n"
    "Benefits List:\n" + "\n".join([f"{i+1}. {b}" for i, b in enumerate(benefits)])
)

    print("Sending prompt to API...")
    response = model.generate_content(prompt)

    if response is None:
        print("No response from API")
        return []

    print("RAW API RESPONSE:", response.text)  

    values = response.text.split("\n")
    print("Extracted Values:", values)  

    return values

monetary_values = get_monetary_values(benefits_list)
print("Length of monetary_values:", len(monetary_values))

monetary_values[-1]

monetary_values = monetary_values[:-1]

len(monetary_values)

print(monetary_values)

import re

scores = [int(re.search(r"Score: (\d+)", entry).group(1)) for entry in monetary_values]
print(scores)

len(scores)

from collections import Counter
freq = Counter(scores)
print(freq)

df.loc[df["Welcome Benefits"].notna(), "welcome scores"] = scores
df["welcome scores"] = df["welcome scores"].fillna(0).astype(int)

df.head()

df.tail()

df.drop(columns=['welcome value'], inplace=True)

df.head()

df['business expenses'].value_counts()

df['movies'].value_counts()

print(df.loc[df['business expenses'] != 0])

df = df.dropna(subset=['Best Suited For'])

df = df.reset_index(drop=True)

df.shape

df.to_csv('final.csv')

def calculate_score(df, user_income, is_salaried, user_expenditure):
    df = df.copy()
    income_col = "Minimum Salaried Income" if is_salaried else "Minimum ITR for Self Employed"
    df = df[df[income_col] <= user_income]
    total_expenditure = sum(user_expenditure.values())
    df["Adjusted Annual Fee"] = np.where(df["annual fee waiver"] <= total_expenditure, 0, df["Renewal Fee"])
    category_columns = ["shopping", "travel", "dining", "movies", "fuel", "food", "bill payment", "stays", "business expenses"]
    df["Expenditure Match"] = sum(df[cat] * user_expenditure.get(cat, 0) for cat in category_columns)
    df["Score"] = (
        np.log(df[income_col] + 100000) 
        -  df["Joining Fee"] 
        - df["Adjusted Annual Fee"] 
        + df["welcome scores"]
        + df["Expenditure Match"]
    )
    return df[["Card Name", "Score"]].sort_values(by="Score", ascending=False)

user_income = 300000
is_salaried = True
user_expenditure = {'shopping': 200000, 'travel': 320000, 'dining': 70000}

filtered_df = calculate_score(df, user_income, is_salaried, user_expenditure)
print(filtered_df[:5])

