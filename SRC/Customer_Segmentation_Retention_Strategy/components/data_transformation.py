import os
import shutil
from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.utils.common import get_size
from Customer_Segmentation_Retention_Strategy.entity.config_entity import DataTransformationConfig
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import linregress
from datetime import timedelta



class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config = config




    def load_preprocess_data(self):
        logger.info("Loading and preprocessing data...")
        excel_path = self.config.source_file_path
        

        sheets = pd.read_excel(excel_path, sheet_name=None)
        df = pd.concat(sheets.values(), ignore_index=True)
        logger.info(f"Loaded data shape: {df.shape}")


        # Handling the missing values
        df["Description"] = df["Description"].fillna("Unknown")
        df = df.dropna(subset=['Customer ID'])
        df.drop_duplicates(inplace=True)
        


        # Removing the anomalous stock codes
        unique_stock_codes = df['StockCode'].unique()
        anomalous_stock_codes  = [ code for code in unique_stock_codes if sum(c.isdigit() for c in str(code))<=4]
        df = df[~df['StockCode'].isin(anomalous_stock_codes)]

        # Filtering out service related descriptions
        service_related_descriptions = ['Next Day Carriage', 'High Resolution Image']

        df = df[~df['Description'].isin(service_related_descriptions)]

        df['Description'] = df['Description'].str.upper()

        # Removing entries with non-positive prices
        df = df[df['Price']>0]

        df.reset_index(drop=True, inplace=True)

        logger.info(f"Preprocessed data shape: {df.shape}")

        logger.info("Loading and preprocessing data completed...")

        return df
    

    

    def feature_engineering(self, df):
        logger.info("Feature engineering...")

        df = df.copy()
        
        # Convert 'InvoiceDate' to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        # Calculate 'Total_Spend'
        df['Total_Spend'] = df['Quantity'] * df['Price']

        df['Transaction_Status'] = np.where(df['Invoice'].astype(str).str.startswith('C'), 'Cancelled', 'Completed')

        max_date = df['InvoiceDate'].max()
        snapshot_date = max_date - timedelta(days=180)
        churn_window_end = snapshot_date + timedelta(days=90)

        df = df[df['InvoiceDate'] <= snapshot_date]

        last_purchase = df.groupby('Customer ID')['InvoiceDate'].max().reset_index()
        last_purchase['Churn'] = ((snapshot_date - last_purchase['InvoiceDate']).dt.days > 90).astype(int)

        rfm = df.groupby('Customer ID').agg(Frequency=('Invoice', 'nunique'),
                                            Monetary=('Total_Spend', 'sum'),
                                            Total_Products_Purchased=('Quantity', 'sum'),
                                            Unique_Products_Purchased=('StockCode', 'nunique')).reset_index()
        

        rfm['Avg_Transaction_Value'] = rfm['Monetary'] / rfm['Frequency']

        product_features = df.groupby('Customer ID').agg(Top_Product_Concentration=('StockCode', lambda x: x.value_counts().iloc[0] / len(x)),Category_Diversity=('Description', 'nunique')).reset_index()
        
        df['Quarter'] = df['InvoiceDate'].dt.to_period('Q')
        quarterly = df.groupby(['Customer ID', 'Quarter'])['Total_Spend'].sum().reset_index()
        quarterly_growth = quarterly.groupby('Customer ID').apply(lambda x: linregress(np.arange(len(x)), x['Total_Spend'].values).slope if len(x) > 1 else 0).reset_index(name='Quarterly_Spending_Trend')


        tenure = df.groupby('Customer ID')['InvoiceDate'].min().reset_index(name='First_Purchase')
        tenure['Customer_Tenure_Days'] = (snapshot_date - tenure['First_Purchase']).dt.days
        rfm = rfm.merge(tenure[['Customer ID', 'Customer_Tenure_Days']], on='Customer ID', how='left')
        
        purchase_gaps = df.sort_values(['Customer ID', 'InvoiceDate']).groupby('Customer ID')['InvoiceDate'].diff().dt.days
        gap_stats = purchase_gaps.groupby(df['Customer ID']).agg( Avg_Days_Between_Purchases='mean',Std_Days_Between_Purchases='std' ).reset_index()
        gap_stats['Std_Days_Between_Purchases'] = gap_stats['Std_Days_Between_Purchases'].fillna(0)
        

        gap_stats['Purchase_Regularity'] = (gap_stats['Avg_Days_Between_Purchases'] / (gap_stats['Std_Days_Between_Purchases'] + 1)).fillna(0)



        monthly = df.assign(YearMonth=df['InvoiceDate'].dt.to_period('M')).groupby(['Customer ID', 'YearMonth'])['Total_Spend'].sum().reset_index()
        

        def calc_slope(s):
            return 0 if len(s) <= 1 else linregress(np.arange(len(s)), s.values).slope
        
        trend = monthly.groupby('Customer ID')['Total_Spend'].apply(calc_slope).reset_index(name='Spending_Trend')
        

        rfm['Revenue_Per_Product'] = (rfm['Monetary'] / rfm['Unique_Products_Purchased']).fillna(0)
        

        total_tx = df.groupby('Customer ID')['Invoice'].nunique().reset_index(name='Total_Transactions')
        cancelled = df[df['Transaction_Status']=='Cancelled'].groupby('Customer ID')['Invoice'].nunique().reset_index(name='Cancelled_Transactions')
        cancel_features = total_tx.merge(cancelled, on='Customer ID', how='left')
        cancel_features['Cancelled_Transactions'] = cancel_features['Cancelled_Transactions'].fillna(0)
        cancel_features['Cancellation_Rate'] = cancel_features['Cancelled_Transactions'] / cancel_features['Total_Transactions']

        price_behavior = df.groupby('Customer ID').agg(Price_Sensitivity=('Price', 'std')).reset_index()
        
        country_mode = df.groupby(['Customer ID','Country']).size().reset_index(name='Count').sort_values('Count', ascending=False).drop_duplicates('Customer ID')
        country_mode['Is_UK'] = (country_mode['Country'] == 'United Kingdom').astype(int)

        repeat_customers = df.groupby('Customer ID')['Invoice'].nunique().reset_index(name='Invoice_Count')
        repeat_customers['Is_Repeat_Customer'] = (repeat_customers['Invoice_Count'] >= 2).astype(int)
        
    
        customer_data = rfm.merge(gap_stats[['Customer ID','Avg_Days_Between_Purchases','Purchase_Regularity']], on='Customer ID', how='left')
        customer_data = customer_data.merge(product_features, on='Customer ID', how='left')
        customer_data = customer_data.merge(quarterly_growth, on='Customer ID', how='left')
        customer_data = customer_data.merge(price_behavior, on='Customer ID', how='left')   
        customer_data = customer_data.merge(trend, on='Customer ID', how='left')
        customer_data = customer_data.merge(cancel_features[['Customer ID','Cancellation_Rate']], on='Customer ID', how='left')
        customer_data = customer_data.merge(country_mode[['Customer ID','Is_UK']], on='Customer ID', how='left')
        customer_data = customer_data.merge(last_purchase[['Customer ID','Churn']], on='Customer ID', how='left')

        
        numeric_cols = customer_data.select_dtypes(include=['number']).columns
        customer_data[numeric_cols] = customer_data[numeric_cols].fillna(0)
        customer_data = customer_data[customer_data['Monetary'] >= 0].copy()
        df = customer_data

        logger.info("Feature engineering completed.")

        return df


    def data_transformation(self):

        logger.info("Starting data transformation pipeline...")
        df = self.load_preprocess_data()
        df = self.feature_engineering(df)
        

        os.makedirs(self.config.root_dir, exist_ok=True)
        df.to_csv(self.config.root_dir / "customer_data.csv", index=False)


        logger.info("Performing train-test split...")
        

        split_ratio = getattr(self.config, 'train_split_ratio', 0.80)
        split_index = int(len(df) * split_ratio)

        
        train = df.iloc[:split_index].copy()
        test = df.iloc[split_index:].copy()

        
        
        train.to_csv(self.config.root_dir / "train.csv", index=False)
        test.to_csv(self.config.root_dir / "test.csv", index=False)

        logger.info("=== Train-Test Split Summary ===")
        logger.info(f"Total samples: {len(df):,}")
        logger.info(f"Training samples: {len(train):,} ({len(train)/len(df)*100:.1f}%)")
        logger.info(f"Test samples: {len(test):,} ({len(test)/len(df)*100:.1f}%)")

               
       
        logger.info("Data transformation pipeline completed successfully!")

        return train, test