import json
from datetime import datetime
from pathlib import Path

from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.utils.logger import logger


class ModelMaintenance:
    def __init__(self, monitoring_config=None, maintenance_config=None):
        config_manager = ConfigurationManager()
        
        self.monitoring_config = monitoring_config or config_manager.get_model_monitoring_config()
        self.maintenance_config = maintenance_config or config_manager.get_model_maintenance_config()

    def load_drift_report(self) -> dict:
        with open(self.monitoring_config.drift_report_path, "r") as f:
            return json.load(f)

    def retrain_decision(self) -> dict:
        logger.info("Loaded the drift report")
        drift_report = self.load_drift_report()
        features_with_drift = [
            feature
            for feature, details in drift_report["drift_report"].items()
            if details["drift_detected"]
        ]
        logger.info("Extracting the drifted features")
        decision = {
            "mode": self.maintenance_config.retrain_mode,
            "timestamp": datetime.utcnow().isoformat(),
            "retrain_required": False,
            "reason": "No significant drift detected"
        }
        logger.info("Retrain decision made")
        if features_with_drift and self.maintenance_config.retrain_on_drift:
            decision.update({
                "retrain_required": True,
                "reason": "Feature drift detected",
                "drifted_features": features_with_drift
            })
        
        self._update_model_registry(decision)
        logger.info("Saves decision to model registry")
        return decision

    def _update_model_registry(self, decision: dict):

        registry_path = Path(self.maintenance_config.model_registry_path)
        registry_path.parent.mkdir(parents=True, exist_ok=True)

        if registry_path.exists():
            with open(registry_path, "r") as f:
                registry = json.load(f)
        else:
            registry = {"history": []}

        registry["history"].append(decision)

        with open(registry_path, "w") as f:
            json.dump(registry, f, indent=4)
