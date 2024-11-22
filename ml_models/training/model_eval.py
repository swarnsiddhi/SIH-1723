import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
from pathlib import Path

class Predict:
    def __init__(self, feature_csv):
        """
        Initialize the Predict class and load pre-trained models.
        """
        self.feature_csv = feature_csv
        self.feature_scaler = MinMaxScaler()
        
        # Load the pre-trained models
        self.model_E = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Elongation.joblib')
        self.model_UTS = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_UTS.joblib')
        self.model_C = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Conductivity.joblib')
        
        # Load the scalers for each target variable
        self.target_scaler_y = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_y.joblib')
        self.target_scaler_b = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_b.joblib')
        self.target_scaler_s = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_s.joblib')
    
    def load_features(self):
        """
        Load the features from the CSV file and extract the last row.
        """
        df_features = pd.read_csv(self.feature_csv)
        # Get the last row as the input features for prediction
        self.features = df_features.iloc[-1:].values
        return self.features

    def scale_features(self):
        """
        Scale the input features using the feature scaler.
        """
        self.features_scaled = self.feature_scaler.fit_transform(self.features)
    
    def make_predictions(self):
        """
        Make predictions using the pre-trained models.
        """
        print("Making predictions...")
        
        # Predict Elongation
        yhat_scaled = self.model_E.predict(self.features_scaled)
        elongation_prediction = self.target_scaler_y.inverse_transform(yhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict UTS
        bhat_scaled = self.model_UTS.predict(self.features_scaled)
        uts_prediction = self.target_scaler_b.inverse_transform(bhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict Conductivity
        shat_scaled = self.model_C.predict(self.features_scaled)
        conductivity_prediction = self.target_scaler_s.inverse_transform(shat_scaled.reshape(-1, 1)).flatten()[0]
        
        print("Predictions completed.")
        return elongation_prediction, uts_prediction, conductivity_prediction

    def run_prediction(self):
        """
        Run the complete prediction pipeline.
        """
        self.load_features()
        self.scale_features()
        elongation, uts, conductivity = self.make_predictions()
        print(f"Predicted Elongation: {elongation:.3f}")
        print(f"Predicted UTS: {uts:.3f}")
        print(f"Predicted Conductivity: {conductivity:.3f}")
        return elongation, uts, conductivity

if __name__ == "__main__":
    # Path to the feature CSV file
    feature_csv_path = 'data/processed/forward/A_test_UTS.csv'
    
    # Create an instance of the Predict class
    predictor = Predict(feature_csv=feature_csv_path)
    
    # Run the prediction
    elongation, uts, conductivity = predictor.run_prediction()
