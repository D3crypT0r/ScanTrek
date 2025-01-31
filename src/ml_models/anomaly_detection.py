import numpy as np
from sklearn.ensemble import IsolationForest

class FileAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.01,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def train(self, file_metadata):
        features = self.extract_features(file_metadata)
        scaled = self.scaler.fit_transform(features)
        self.model.fit(scaled)

    def predict(self, file_metadata):
        features = self.extract_features(file_metadata)
        scaled = self.scaler.transform([features])
        return self.model.decision_function(scaled)

    def extract_features(self, metadata):
        return [
            metadata['entropy'],
            metadata['file_size'],
            len(metadata['embedded_files']),
            metadata['header_complexity'],
            metadata['compression_ratio']
        ]
