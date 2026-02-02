import os
from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.utils.common import get_size
from Customer_Segmentation_Retention_Strategy.entity.config_entity import ModelTrainerConfig
from pathlib import Path
import numpy as np 
import pandas as pd 
import xgboost as xgb
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib
from datetime import datetime

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config
        self.features_columns = None 


    def  prepare_features(self, train_data, test_data): 

        logger.info(f"Feature preparation started:")

        X_train = train_data.drop(columns=[self.config.target_column], errors="ignore")
        X_test = test_data.drop(columns=[self.config.target_column], errors="ignore")
        y_train = train_data[self.config.target_column]
        y_test = test_data[self.config.target_column]


        logger.info(f"Feature preparation completed:")
        logger.info(f"  Training features shape: {X_train.shape}")
        logger.info(f"  Test features shape: {X_test.shape}")

        return X_train, X_test, y_train, y_test


    
    def evaluate(self, model, X_test, y_test):

        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        logger.info("=== Model Evaluation Metrics ===")
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"ROC-AUC: {roc_auc:.4f}")


        predictions_df = pd.DataFrame({
            "y_true": y_test.values,
            "y_pred": y_pred,
            "y_pred_proba": y_pred_proba
        })

        predictions_path = os.path.join(
            self.config.root_dir,
            "predictions.csv"
        )

        predictions_df.to_csv(predictions_path, index=False)
        
        logger.info(f"Predictions saved at: {predictions_path}")

        return {
            "accuracy": accuracy,
            "roc_auc": roc_auc,
            "predictions_path": predictions_path
        }

            


    def save_model_artifacts(self, model,X_train):
        os.makedirs(self.config.root_dir, exist_ok=True)
        
        model_artifacts = {
                    "model": model,
                    "model_type": "XGBClassifier",
                    "target_column": self.config.target_column,
                    "feature_columns": list(X_train.columns),
                    "timestamp": datetime.now().isoformat()
                }
        
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(model_artifacts, model_path)
        logger.info(f"Model artifacts saved at: {model_path}")

    def train(self):
        logger.info("Starting model training pipeline")

        try: 

            logger.info("Loading training and test data...")
            train_data = pd.read_csv(self.config.train_data_path)
            test_data = pd.read_csv(self.config.test_data_path)

            X_train, X_test, y_train, y_test = self.prepare_features(train_data, test_data)

            xgb_params = {
                    'objective': self.config.objective, 
                    'n_estimators': self.config.n_estimators, 
                    'learning_rate': self.config.learning_rate,
                    'max_depth': self.config.max_depth,
                    'subsample': self.config.subsample,
                    'colsample_bytree': self.config.colsample_bytree, 
                    'min_child_weight': self.config.min_child_weight, 
                    'random_state': self.config.random_state
                    }



            xgb_model = xgb.XGBClassifier(
                                **xgb_params,
                                eval_metric=self.config.eval_metric
                            )
            xgb_model.fit(X_train, y_train)

            metrics = self.evaluate(model=xgb_model,X_test=X_test,y_test=y_test)
            
            self.save_model_artifacts(xgb_model,X_train)




            logger.info("Model training completed successfully!")

            return {"model": xgb_model,"metrics": metrics}


        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise e