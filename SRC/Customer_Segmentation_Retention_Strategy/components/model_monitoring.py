import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.utils.logger import logger

class ModelMonitoring:
    def __init__(self,config):
        config_manager = ConfigurationManager()
        self.config = config_manager.get_model_monitoring_config()

    @staticmethod
    def calculate_psi(expected: pd.Series, actual: pd.Series, buckets: int = 10) -> float:
    

        breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
        psi_value = 0.0

        for i in range(len(breakpoints) - 1):
            expected_ratio = np.mean(
                (expected >= breakpoints[i]) & (expected < breakpoints[i + 1])
            )
            actual_ratio = np.mean(
                (actual >= breakpoints[i]) & (actual < breakpoints[i + 1])
            )

            if expected_ratio == 0 or actual_ratio == 0:
                continue

            psi_value += (expected_ratio - actual_ratio) * np.log(
                expected_ratio / actual_ratio
            )

        return round(psi_value, 4)

    def run_monitoring(self):

        logger.info("Loaded the data.")
        baseline_df = pd.read_csv(self.config.baseline_data_path)
        production_df = pd.read_csv(self.config.production_data_path)

        drift_report = {}

        common_columns = baseline_df.columns.intersection(production_df.columns)

        for col in common_columns:
            if baseline_df[col].dtype in ["int64", "float64"]:
                logger.info("Calculating the psi")
                psi = self.calculate_psi(
                    baseline_df[col].dropna(),
                    production_df[col].dropna()
                )
                logger.info("Detecting the drifts")
                drift_detected = bool(psi > self.config.psi_threshold)  
                drift_report[col] = {
                    "psi": psi,
                    "drift_detected": drift_detected  
                }

        report = {
            "mode": "simulation",
            "timestamp": datetime.utcnow().isoformat(),
            "psi_threshold": self.config.psi_threshold,
            "drift_report": drift_report
        }

        self._save_report(report)
        logger.info("Saves the results to JSON report")
        return report

    def _save_report(self, report: dict):
        Path(self.config.root_dir).mkdir(parents=True, exist_ok=True)

        with open(self.config.drift_report_path, "w") as f:
            json.dump(report, f, indent=4)
