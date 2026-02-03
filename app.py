import streamlit as st
import joblib
import pandas as pd






def load_model():
    model_path = "artifacts/model_trainer/model.joblib"
    model_dict = joblib.load(model_path)
    return model_dict['model']  

def main():
    st.set_page_config(page_title="Customer Churn Prediction App",layout="wide")

    st.title(" Customer Churn Prediction")
    st.write("Predict whether a customer is likely to **churn or stay**, "
        "based on behavioral and transaction-level features."
        )
    st.header("Input Customer Features")

    Frequency = st.number_input("Frequency", min_value=0.0, value=10.0)
    Monetary = st.number_input("Monetary", min_value=0.0, value=10000.0)
    Total_Products_Purchased = st.number_input("Total Products Purchased", min_value=0, value=20)
    Unique_Products_Purchased = st.number_input("Unique Products Purchased", min_value=0, value=10)
    Avg_Transaction_Value = st.number_input("Average Transaction Value", min_value=0.0, value=50.0)
    Customer_Tenure_Days = st.number_input("Customer Tenure (Days)", min_value=0, value=365)
    Revenue_Per_Product = st.number_input("Revenue Per Product", min_value=0.0, value=25.0)
    Avg_Days_Between_Purchases = st.number_input("Avg Days Between Purchases", min_value=0.0, value=15.0)
    Purchase_Regularity = st.number_input("Purchase Regularity", min_value=0.0, value=0.5)
    Top_Product_Concentration = st.number_input("Top Product Concentration", min_value=0.0, max_value=1.0, value=0.4)
    Category_Diversity = st.number_input("Category Diversity", min_value=0.0, value=3.0)
    Quarterly_Spending_Trend = st.number_input("Quarterly Spending Trend", value=0.1)
    Price_Sensitivity = st.number_input("Price Sensitivity", min_value=0.0, value=0.3)
    Spending_Trend = st.number_input("Spending Trend", value=0.05)
    Cancellation_Rate = st.number_input("Cancellation Rate", min_value=0.0, max_value=1.0, value=0.1)
    Is_UK = st.selectbox("Is UK Customer?", [0, 1])

    input_data = pd.DataFrame(
        [{
            "Frequency": Frequency,
            "Monetary": Monetary,
            "Total_Products_Purchased": Total_Products_Purchased,
            "Unique_Products_Purchased": Unique_Products_Purchased,
            "Avg_Transaction_Value": Avg_Transaction_Value,
            "Customer_Tenure_Days": Customer_Tenure_Days,
            "Revenue_Per_Product": Revenue_Per_Product,
            "Avg_Days_Between_Purchases": Avg_Days_Between_Purchases,
            "Purchase_Regularity": Purchase_Regularity,
            "Top_Product_Concentration": Top_Product_Concentration,
            "Category_Diversity": Category_Diversity,
            "Quarterly_Spending_Trend": Quarterly_Spending_Trend,
            "Price_Sensitivity": Price_Sensitivity,
            "Spending_Trend": Spending_Trend,
            "Cancellation_Rate": Cancellation_Rate,
            "Is_UK": Is_UK
        }]
    )


    if st.button("Predict Churn"):
        model = load_model()

        prediction = model.predict(input_data)[0]

        churn_label = "Churn" if prediction == 1 else "Not Churn"

        st.subheader("Prediction Result")
        st.success(f"**Customer Status:** {churn_label}")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(input_data)[0][1]
            st.info(f"Churn Probability: **{prob:.2%}**")

    else:
        st.info("Enter feature values and click **Predict Churn**")

if __name__ == "__main__":
    main()
