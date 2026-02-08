![Image](assets/Customer%20Churn%20Prediction.jpg)

![Python version](https://img.shields.io/badge/Python%20version-3.11-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/samithcsachi/Customer-Segmentation-Retention-Strategy)
![GitHub repo size](https://img.shields.io/github/repo-size/samithcsachi/Customer-Segmentation-Retention-Strategy)
![License](https://img.shields.io/badge/License-MIT-green)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

Badge [source](https://shields.io/)

# Customer Segmentation & Retention Strategy using Transactional Data

This is an End-to-end customer segmentation and retention strategy built on transactional data, combining RFM-based analytics, churn modeling, deployment, and monitoring to support data-driven retention decisions. From the insights from the data analysis few actionable business decisions was made and developed a Customer Churn Prediction App. The application provides a web interface for users to input the values for features and a check whether the customer will be churn or not.

Hugging Face Spaces Streamlit App link : [https://huggingface.co/spaces/samithcs/Customer_Churn_Prediction_App](https://huggingface.co/spaces/samithcs/Customer_Churn_Prediction_App)

Docker Hub Link: - [https://hub.docker.com/r/samithc/customer-segmentation-app](https://hub.docker.com/r/samithc/customer-segmentation-app)

Articles - 
-  Medium :
  -- Analysis: - [https://medium.com/towards-artificial-intelligence/customer-segmentation-and-retention-strategy-using-transactional-data-9b74e0d27e35](https://medium.com/towards-artificial-intelligence/customer-segmentation-and-retention-strategy-using-transactional-data-9b74e0d27e35)   

## Authors

- [Samith Chimminiyan](https://www.github.com/samithcsachi)

## Table of Contents

- [Authors](#Authors)
- [Table of Contents](#table-of-contents)
- [Problem Statement](#problem-statement)
- [Tech Stack](#tech-stack)
- [Data source](#data-source)
- [Quick glance at the results](#quick-glance-at-the-results)
- [Limitation and what can be improved](#limitation-and-what-can-be-improved)
- [Lessons Learned and Recommendations](#lessons-learned-and-recommendations)
- [Run Locally](#run-locally)
- [Explore the notebook](#explore-the-notebook)
- [Contribution](#contribution)
- [License](#license)

## Problem Statement

Retailers are continuously competing to grow their businesses by better understanding customer behavior and predicting customer churn. Often retailers have a large quantity of transactional data collected from their customers, but, if they don't know how to analyze that data, they have no way to differentiate between their customers and develop retention strategies for their customers.

The purpose of the proposed project will be to analyze transactional data to group the customer into various groups based on the purchasing patterns and spending patterns and identify the customers at the highest risk of churning and develop a retention strategy for each customer segment. As part of the retention strategy develop an app to predict the customer churn in advance so that necessary steps can be initiated.

## Tech Stack

- Python
- Streamlit
- Fastapi
- Sklearn
- Docker

## Data Source

This Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers.

Dataset Source : - [https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii](https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii)

The dataset contains 1067371 entries and has 8 columns. This is a short description of the columns:

- Invoice : Invoice number. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.
- StockCode : Product (item) code. A 5-digit integral number uniquely assigned to each distinct product.
- Description : Product (item) name.
- Quantity : The quantities of each product (item) per transaction.
- InvoiceDate : Invoice date and time. The day and time when a transaction was generated.
- Price : Unit price. Product price per unit in sterling (£).
- CustomerID : Customer number. A 5-digit integral number uniquely assigned to each customer.
- Country : Country name. The name of the country where a customer resides.

## Quick glance at the results

![Demo](assets/Customer%20Churn%20Prediction.jpg)

Recency Distribution and Customer Segments

![Recency Distribution](assets/Recency%20Distribution%20and%20Segments.png)

Customer Behavior by Spending Tier

![Customer Behavior by Spending Tier](assets/Customer%20Behavior%20by%20Spending%20Tier.png)

RFM Heatmap Recency vs Frequency Score Counts
![RFM Heatmap Recency vs Frequency Score Counts](assets/RFM%20Heatmap%20Recency%20vs%20Frequency%20Score%20Counts.png)

RFM Segment Analysis
![RFM Segment Analysis](assets/RFM%20Segment%20Analysis.png)

Spending Trends by RFM Segment (Positive Growth Only)
![Spending Trends by RFM Segment (Positive Growth Only)](<assets/Spending%20Trends%20by%20RFM%20Segment%20(Positive%20Growth%20Only).png>)

Churn Rate vs Avg Monetary Value by RFM Segment Bubble Plot
![Churn Rate vs Avg Monetary Value by RFM Segment Bubble Plot](assets/Churn%20Rate%20vs%20Avg%20Monetary%20Value%20by%20RFM%20Segment%20Bubble%20Plot.png)

Analysis :

As per the analysis, it was understood that there over-reliance on the top 10 %, and if the top 10% churn, then the 50% of the revenue is gone. But there lies an opportunity to understand what makes the top 10% different and replicate their characteristics in the 80–90% segment. Also to be noted that 59.2% of customers are at-risk or lost, and Only 40.8% are actively engaged. Different visuals confirmed how important was the top 10% customers but in that also some are in-active. The champion customer are regular buyers and active, it is difficult to predict the exact timing of purchase. Champions are amazing customers, but cannot manage them blindly because they can't predict their behavior. Finally it can be concluded that there is a conversation threshold, not a retention problem. The champion customer are buying high value items and controlling the revenue loss. As per the analysis the customer was segregated to different segments and different strategy need to be applied
to retain the heavy lifters and also regain some of the customers which was lost and few other strategies for the remaining. Suggested strategies are as below.

| RFM Segment            | Customers | Revenue (£) | Strategy                                         |
| ---------------------- | --------- | ----------- | ------------------------------------------------ |
| Champions              | 1,463     | 11,502,549  | VIP treatment, loyalty rewards, exclusive offers |
| Best Customers         | 511       | 1,641,089   | Premium support, early access to new products    |
| Can’t Lose Them        | 376       | 988,690     | High-value focus, personalized service           |
| Lost Customers         | 1,815     | 663,549     | Upsell opportunities, cross-selling              |
| Loyal Customers        | 434       | 451,983     | Win-back campaigns, special incentives           |
| Lost – Big Spenders    | 157       | 349,662     | Immediate re-engagement, special offers          |
| Good Customers         | 275       | 324,155     | Aggressive win-back campaign                     |
| Hibernating            | 385       | 195,030     | Low priority, automated campaigns only           |
| Low-Value Customers    | 335       | 94,326      | Budget-friendly reactivation offers              |
| Potential              | 95        | 76,450      | Convert to higher-value segment                  |
| At Risk – Big Spenders | 29        | 69,920      | Cross-sell and upsell strategies                 |

Churn Prediction Model :

It was noticed in the analysis how important it is to predict the customer churn as early as possible. The goal of the churn model is not just prediction accuracy, but to identify high-value customers who are at risk early enough for intervention. Churn for model prediction is defined as no purchase within 90 days after a fixed snapshot date, where the snapshot date is set 180 days before the maximum date in the dataset.This separation ensures no data leakage and reflects real-world deployment conditions.

Notebook :

| Model (Notebook)            | ROC-AUC | Accuracy |
| --------------------------- | ------- | -------- |
| Logistic Regression         | 87.45 % | 80.60 %  |
| XGBoost                     | 97.47 % | 91.91 %  |
| Neural Network (TensorFlow) | 97.39 % | 92.12 %  |

Logistic Regression:
The Model achieves 80.60 % accuracy with an ROC-AUC of 87.45 %, indicating good discriminative ability between classes. Confusion matrix indicated it misclassifies 78 negative cases as positive (false positives) and 114 positive cases as negative (false negatives).

XGBoost :

The Model achieves 91.91% accuracy with an ROC-AUC of 97.47 %. Confusion matrix indicated it misclassifies 30 negative cases as positive (false positives) and 50 positive cases as negative (false negatives).

Neural Network (TensorFlow):
The Model achieves 92.12 % accuracy with an ROC-AUC of 97.39 %. Confusion matrix indicated it misclassifies 55 negative cases as positive (false positives) and 23 positive cases as negative (false negatives).

Although the Neural Network achieved the slightly better, XGBoost achieved comparable performance with better interpretability and operational simplicity.

MLOps Pipeline :

| Model (MLOps Pipeline) | ROC-AUC | Accuracy |
| ---------------------- | ------- | -------- |
| XGBoost                | 85.45 % | 94.95 %  |

In the MLOps pipeline train test was split as csv files unlike the sklean train-test split.

The key reasons for the difference is as below:

- Data distribution shift
- Class imbalance impact on Accuracy

This shows that the model is generalizing well and is considered as positive signal.

Conclusion :

Although accuracy decreased in the MLOps pipeline, the ROC-AUC remains high. This indicates that the model continues to rank churn and non-churn customers effectively. The drop in accuracy is expected due to stricter train–test separation and real-world data distribution differences. ROC-AUC is therefore a more reliable metric for evaluating churn models in production. For churn prediction, ROC-AUC is preferred over accuracy because churn prevention is a prioritization problem.

How Model Monitoring & Maintenance (Simulation) was implemented :

Since the dataset is historical (2009–2011), model monitoring and maintenance are implemented in simulation mode. Data from 2009–2010 is treated as baseline training data, while 2011 data simulates production traffic. Feature drift is detected using PSI, and retraining logic is demonstrated conditionally to reflect real-world MLOps workflows.

## Limitation and what can be improved

- Limitations:
  - Dataset Diversity: The current dataset contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011. The Dataset is old and it is based on 2 years data. Few years data will provide more diversity and the model can relate to the real world customer churn.

- What Can Be Improved
  - Expand Dataset: Current dataset seems like biased as the dataset is concentrated on one country and will be able get better results if the dataset is expanded.

  - Real World Dataset : Best option to demonstrate Customer Churn Prediction system was to get the Real World dataset with API. Unfortunately the API's are not currently available or its expensive.

  - Monitoring and Maintenance: Currently Monitoring and Maintenance are implemented based on stimulation data. It is not based on real time drift. It simulates model monitoring using historical data to demonstrate production-grade ML workflows.

## Lessons Learned and Recommendations

- Lessons Learned
  - Using UV : Have learn how to use UV instead of PIP for an end to end MLOps project. UV was used to create the dockerfile locally and in HuggingFace space.

  - Monitoring and Maintenance: Implemented continuous monitoring for data and cluster drift using PSI. When drift exceeds thresholds, an automated maintenance pipeline retrains, validates, versions, and redeploys the model.

- Recommendations
  - Broader Dataset Acquisition: Invest in collecting a more comprehensive dataset which can be connected more the real world customers.

  - Continuous Monitoring and Retraining: Set up feedback loops to capture new data and edge cases, enabling periodic retraining for improved accuracy and adaptability.

  - Integration Workflow: Develop user-friendly interfaces (web, mobile), possibly leveraging frameworks like PowerBi or Tableau, for visualization.

## Run Locally

Initialize git

```bash
git init
```

Clone the project

```bash
git clone https://github.com/samithcsachi/Customer-Segmentation-Retention-Strategy.git
```

Change the Directory

```bash
cd E:/Customer-Segmentation-Retention-Strategy

```

Initialize UV

```bash
uv init
```

Only if you need to try the tensorflow code in notebook

- Change the python verions in the pyproject.toml and .python-version to 3.11

```bash
uv sync
```

```bash
uv pip install tensorflow-cpu
```

install the requirements

```bash
uv add ensure fastapi joblib matplotlib numpy openpyxl pandas protobuf pydantic python pyyaml scikit-learn seaborn streamlit uvicorn xgboost

```

Run the main file

```bash
uv pip install -e .
```

```bash
uv run python main.py
```

Run the app

```bash
.venv\Scripts\activate
```

```bash
python -m streamlit run app.py
```

Run the FAST API

```bash
.venv\Scripts\activate
```

```bash
cd F:Customer-Segmentation-Retention-Strategy\SRC\Customer_Segmentation_Retention_Strategy\api
```

```bash
uvicorn main:app --reload
```

For Dockerization

```bash
docker build -t customer-segmentation-app .
```

```bash
docker login
```

```bash
docker tag customer-segmentation-app:latest samithc/customer-segmentation-app:latest
```

```bash
docker push samithc/customer-segmentation-app:latest
```

## Explore the notebook

GitHub : [https://github.com/samithcsachi/Customer-Segmentation-Retention-Strategy](https://github.com/samithcsachi/Customer-Segmentation-Retention-Strategy)

## Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change or contribute.

## License

MIT License

Copyright (c) 2025 Samith Chimminiyan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Learn more about [MIT](https://choosealicense.com/licenses/mit/) license

## Contact

If you have any questions, suggestions, or collaborations in data science, feel free to reach out:

- 📧 Email: [samith.sachi@gmail.com](mailto:samith.sachi@gmail.com)
- 🔗 LinkedIn: [www.linkedin.com/in/samithchimminiyan](https://www.linkedin.com/in/samithchimminiyan)
- 🌐 Website: [https://samithcsachi.github.io/](https://samithcsachi.github.io/)
