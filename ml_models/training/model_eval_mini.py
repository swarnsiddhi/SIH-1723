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
        self.model_A = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Aluminum Purity (%).joblib')
        self.model_C = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Casting Temperature (°C).joblib')
        self.model_E = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Cooling Water Temperature (°C).joblib')
        self.model_G = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Casting Speed.joblib')
        self.model_I = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Cast Bar Entry Temperature at Rolling Mill (°C).joblib')
        self.model_K = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Emulsion Temperature at Rolling Mill (°C).joblib')
        self.model_M = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Emulsion Pressure at Rolling Mill (bar).joblib')
        self.model_O = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Emulsion Concentration (%).joblib')
        self.model_Q = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'xgboost_model_Rod Quench Water Pressure (bar).joblib')
        
        # Load the scalers for each target variable
        self.target_scaler_b = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_bn.joblib')
        self.target_scaler_d = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_dn.joblib')
        self.target_scaler_f = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_fn.joblib')
        self.target_scaler_h = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_hn.joblib')
        self.target_scaler_j = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_jn.joblib')
        self.target_scaler_l = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_ln.joblib')
        self.target_scaler_n = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_nn.joblib')
        self.target_scaler_p = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_pn.joblib')
        self.target_scaler_r = joblib.load(Path.cwd() / 'ml_models' / 'models' / 'target_scaler_rn.joblib')
    
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
        bhat_scaled = self.model_A.predict(self.features_scaled)
        aluminium_purity = self.target_scaler_b.inverse_transform(bhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict UTS
        dhat_scaled = self.model_C.predict(self.features_scaled)
        casting_temperature = self.target_scaler_d.inverse_transform(dhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict Conductivity
        fhat_scaled = self.model_E.predict(self.features_scaled)
        cooling_water_temp = self.target_scaler_f.inverse_transform(fhat_scaled.reshape(-1, 1)).flatten()[0]

        hhat_scaled = self.model_G.predict(self.features_scaled)
        casting_speed = self.target_scaler_h.inverse_transform(hhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict UTS
        jhat_scaled = self.model_I.predict(self.features_scaled)
        rolling_mill_temp = self.target_scaler_j.inverse_transform(jhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict Conductivity
        lhat_scaled = self.model_K.predict(self.features_scaled)
        emulsion_temp = self.target_scaler_l.inverse_transform(lhat_scaled.reshape(-1, 1)).flatten()[0]

        nhat_scaled = self.model_M.predict(self.features_scaled)
        emulsion_pressure = self.target_scaler_n.inverse_transform(nhat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict UTS
        phat_scaled = self.model_O.predict(self.features_scaled)
        emulsion_conc = self.target_scaler_p.inverse_transform(phat_scaled.reshape(-1, 1)).flatten()[0]
        
        # Predict Conductivity
        rhat_scaled = self.model_Q.predict(self.features_scaled)
        rod_quench_temp = self.target_scaler_r.inverse_transform(rhat_scaled.reshape(-1, 1)).flatten()[0]
        
        print("Predictions completed.")
        return aluminium_purity, casting_temperature, cooling_water_temp, casting_speed, rolling_mill_temp, emulsion_temp, emulsion_pressure, emulsion_conc, rod_quench_temp

    def run_prediction(self):
        """
        Run the complete prediction pipeline.
        """
        self.load_features()
        self.scale_features()
        A, B, C , D, E, F, G, H, I= self.make_predictions()
        print(f"Predicted aluminium_purity: {A:.3f}")
        print(f"Predicted casting_temperature: {B:.3f}")
        print(f"Predicted cooling_water_temp: {C:.3f}")
        print(f"Predicted casting_speed: {D:.3f}")
        print(f"Predicted rolling_mill_temp: {E:.3f}")
        print(f"Predicted emulsion_temp: {F:.3f}")
        print(f"Predicted emulsion_pressure: {G:.3f}")
        print(f"Predicted emulsion_conc: {H:.3f}")
        print(f"Predicted rod_quench_temp: {I:.3f}")
        return A,B,C,D,E,F,G,H,I

if __name__ == "__main__":
    # Path to the feature CSV file
    feature_csv_path = '/home/nitin/Downloads/SIH-1723/data/processed/uploaded_files/intermediate_features.csv'
    
    # Create an instance of the Predict class
    predictor = Predict(feature_csv=feature_csv_path)
    
    # Run the prediction
    A,B,C,D,E,F,G,H,I = predictor.run_prediction()
