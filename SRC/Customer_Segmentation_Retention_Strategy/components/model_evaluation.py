import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_auc_score, accuracy_score, precision_score, recall_score,f1_score
import joblib
import json
from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.entity.config_entity import ModelEvaluationConfig
from pathlib import Path
from datetime import datetime



class ModelEvaluation:
    def __init__(self, config):
        self.config = config
        self.predictions = None   
        self.actuals = None 

    def load_model_and_artifacts(self):
        
        if not os.path.exists(self.config.model_path):
            raise FileNotFoundError(f"Model file not found: {self.config.model_path}")
        
        model_artifacts = joblib.load(self.config.model_path)
        
        logger.info("Loaded model artifacts:")
        logger.info(f"  Model type: {model_artifacts.get('model_type', 'Unknown')}")
        logger.info(f"  Target column: {model_artifacts.get('target_column', 'Unknown')}")
        logger.info(f"  Timestamp: {model_artifacts.get('timestamp', 'Unknown')}")
        logger.info(f"  Features: {len(model_artifacts.get('feature_columns', []))}")
        
        return model_artifacts

    def load_test_data(self):
        columns_to_drop = ['Customer ID']
        if not os.path.exists(self.config.test_data_path):
            raise FileNotFoundError(f"Test data not found: {self.config.test_data_path}")
        
    
        if str(self.config.test_data_path).endswith('.csv'):
            test_data = pd.read_csv(self.config.test_data_path)
            logger.info(f"Loaded test data from CSV: {test_data.shape}")
        elif str(self.config.test_data_path).endswith('.joblib'):
            test_data = joblib.load(self.config.test_data_path)
            logger.info(f"Loaded test data from joblib: {type(test_data)}")
            
            
            if isinstance(test_data, dict):
                if 'X_test' in test_data and 'y_test' in test_data:
                    return test_data['X_test'], test_data['y_test']
                else:
                    raise ValueError("Joblib file doesn't contain 'X_test' and 'y_test' keys")
            elif isinstance(test_data, pd.DataFrame):

                if self.config.target_column in test_data.columns:
                    X_test = test_data.drop(columns=columns_to_drop + [self.config.target_column])
                    y_test = test_data[self.config.target_column]
                    return X_test, y_test
                else:
                    raise ValueError(f"Target column '{self.config.target_column}' not found in test data")
        else:
            raise ValueError(f"Unsupported file format: {self.config.test_data_path}")
        
   
        if self.config.target_column in test_data.columns:
            

            X_test = test_data.drop(columns=columns_to_drop + [self.config.target_column])
            y_test = test_data[self.config.target_column]
            logger.info(f"Split test data - X: {X_test.shape}, y: {y_test.shape}")
            return X_test, y_test
        else:
            raise ValueError(f"Target column '{self.config.target_column}' not found in test data")

    def validate_feature_compatibility(self, X_test, expected_features):
        
        current_features = set(X_test.columns)
        expected_features_set = set(expected_features)
        
        missing_features = expected_features_set - current_features
        extra_features = current_features - expected_features_set
        
        if missing_features:
            logger.warning(f"Missing features: {missing_features}")
            
        if extra_features:
            logger.warning(f"Extra features: {extra_features}")
        
        if missing_features or extra_features:
            logger.info("Reordering test features to match model expectations...")
            X_test = X_test.reindex(columns=expected_features, fill_value=0)
        
        logger.info(f"Feature compatibility check completed. Final shape: {X_test.shape}")
        return X_test



    def calculate_classification_metrics(self, y_true, y_pred, y_pred_proba=None):
        

        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

      
        if y_pred_proba is not None:
            roc_auc = roc_auc_score(y_true, y_pred_proba)
        else:
            roc_auc = None

   
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        confusion_dict = {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp)
        }

        metrics = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "roc_auc": float(roc_auc) if roc_auc is not None else None,
            "confusion_matrix": confusion_dict,
            "n_samples": int(len(y_true))
        }

        return metrics


    
    def save_detailed_results(self,metrics,model_info,y_test=None,y_pred=None,y_pred_proba=None):
        os.makedirs(self.config.root_dir, exist_ok=True)

        results = {
            "timestamp": datetime.now().isoformat(),
            "model_type": model_info.get("model_type", "Unknown"),
            "target_column": model_info.get("target_column", "Unknown"),
            "feature_count": len(model_info.get("feature_columns", [])),
            "metrics": metrics
        }

        results_path = os.path.join(self.config.root_dir, "evaluation_results.json")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=4)

        logger.info(f"Metrics saved to: {results_path}")

   
        if y_test is not None and y_pred is not None:
            df = pd.DataFrame({
                "actual": y_test.values if hasattr(y_test, "values") else y_test,
                "predicted": y_pred
            })

            if y_pred_proba is not None:
                df["predicted_proba"] = y_pred_proba

            predictions_path = os.path.join(self.config.root_dir, "predictions.csv")
            df.to_csv(predictions_path, index=False)
            logger.info(f"Predictions saved to: {predictions_path}")


    def evaluate(self):
        
        logger.info("Starting model evaluation...")
        
        try:
           
            model_artifacts = self.load_model_and_artifacts()
            xgb_model = model_artifacts['model']
            
            
            X_test, y_test = self.load_test_data()
            
            
            expected_features = model_artifacts.get('feature_columns', [])
            if expected_features:
                X_test = self.validate_feature_compatibility(X_test, expected_features)
            
            
            logger.info("Making predictions...")
            y_pred_xgb = xgb_model.predict(X_test)
            y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]
            logger.info(f"Predictions generated for {len(y_pred_xgb)} samples")

           
            self.predictions = y_pred_xgb
            self.actuals = y_test
            
            
            metrics = self.calculate_classification_metrics(y_test, y_pred_xgb,y_pred_proba)
            
        

            
            
            self.save_detailed_results(metrics, model_artifacts)
            
            logger.info("Model evaluation completed successfully!")
            
            return {
                'metrics': metrics,
                'model_info': model_artifacts,
                'evaluation_completed': True
            }
            
        except Exception as e:
            logger.error(f"Error in model evaluation: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            raise e
    