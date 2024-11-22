import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import joblib

class Training:
    def __init__(self, A_train, A_test, b_train, b_test, C_train, C_test, d_train, d_test, E_train, E_test, f_train, f_test, 
                 G_train, G_test, h_train, h_test, I_train, I_test, j_train, j_test, K_train, K_test, l_train, l_test, 
                 M_train, M_test, n_train, n_test, O_train, O_test, p_train, p_test, Q_train, Q_test, r_train, r_test):
        """
        Initialize the Training class with train and test data.
        """
        self.A_train = A_train
        self.A_test = A_test
        self.b_train = b_train
        self.b_test = b_test
        self.C_train = C_train
        self.C_test = C_test
        self.d_train = d_train
        self.d_test = d_test
        self.E_train = E_train
        self.E_test = E_test
        self.f_train = f_train
        self.f_test = f_test
        self.G_train = G_train
        self.G_test = G_test
        self.h_train = h_train
        self.h_test = h_test
        self.I_train = I_train
        self.I_test = I_test
        self.j_train = j_train
        self.j_test = j_test
        self.K_train = K_train
        self.K_test = K_test
        self.l_train = l_train
        self.l_test = l_test
        self.M_train = M_train
        self.M_test = M_test
        self.n_train = n_train
        self.n_test = n_test
        self.O_train = O_train
        self.O_test = O_test
        self.p_train = p_train
        self.p_test = p_test
        self.Q_train = Q_train
        self.Q_test = Q_test
        self.r_train = r_train
        self.r_test = r_test
        
        # Define separate scalers for each target
        self.feature_scaler = MinMaxScaler()
        self.target_scaler_b = MinMaxScaler()
        self.target_scaler_d = MinMaxScaler()
        self.target_scaler_f = MinMaxScaler()
        self.target_scaler_h = MinMaxScaler()
        self.target_scaler_j = MinMaxScaler()
        self.target_scaler_l = MinMaxScaler()
        self.target_scaler_n = MinMaxScaler()
        self.target_scaler_p = MinMaxScaler()
        self.target_scaler_r = MinMaxScaler()
        
        # Paths to save results and models
        self.results_path = Path.cwd() / 'results'
        self.model_path = Path.cwd() / 'ml_models' / 'models'
        
        # Create directories if they don't exist
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.model_path.mkdir(parents=True, exist_ok=True)

    def scale_data(self):
        """
        Scale the features and target variables using MinMaxScaler.
        """
        print("Scaling features and target variables...")
        # Scale the features
        self.A_train_scaled = self.feature_scaler.fit_transform(self.A_train)
        self.A_test_scaled = self.feature_scaler.transform(self.A_test)
        self.C_train_scaled = self.feature_scaler.fit_transform(self.C_train)
        self.C_test_scaled = self.feature_scaler.transform(self.C_test)
        self.E_train_scaled = self.feature_scaler.fit_transform(self.E_train)
        self.E_test_scaled = self.feature_scaler.transform(self.E_test)
        self.G_train_scaled = self.feature_scaler.fit_transform(self.G_train)
        self.G_test_scaled = self.feature_scaler.transform(self.G_test)
        self.I_train_scaled = self.feature_scaler.fit_transform(self.I_train)
        self.I_test_scaled = self.feature_scaler.transform(self.I_test)
        self.K_train_scaled = self.feature_scaler.fit_transform(self.K_train)
        self.K_test_scaled = self.feature_scaler.transform(self.K_test)
        self.M_train_scaled = self.feature_scaler.fit_transform(self.M_train)
        self.M_test_scaled = self.feature_scaler.transform(self.M_test)
        self.O_train_scaled = self.feature_scaler.fit_transform(self.O_train)
        self.O_test_scaled = self.feature_scaler.transform(self.O_test)
        self.Q_train_scaled = self.feature_scaler.fit_transform(self.Q_train)
        self.Q_test_scaled = self.feature_scaler.transform(self.Q_test)

        # Convert target variables to numpy arrays
        self.b_train = self.b_train.values if isinstance(self.b_train, pd.Series) else self.b_train
        self.b_test = self.b_test.values if isinstance(self.b_test, pd.Series) else self.b_test
        self.d_train = self.d_train.values if isinstance(self.d_train, pd.Series) else self.d_train
        self.d_test = self.d_test.values if isinstance(self.d_test, pd.Series) else self.d_test
        self.f_train = self.f_train.values if isinstance(self.f_train, pd.Series) else self.f_train
        self.f_test = self.f_test.values if isinstance(self.f_test, pd.Series) else self.f_test
        self.h_train = self.h_train.values if isinstance(self.h_train, pd.Series) else self.h_train
        self.h_test = self.h_test.values if isinstance(self.h_test, pd.Series) else self.h_test
        self.j_train = self.j_train.values if isinstance(self.j_train, pd.Series) else self.j_train
        self.j_test = self.j_test.values if isinstance(self.j_test, pd.Series) else self.j_test
        self.l_train = self.l_train.values if isinstance(self.l_train, pd.Series) else self.l_train
        self.l_test = self.l_test.values if isinstance(self.l_test, pd.Series) else self.l_test
        self.n_train = self.n_train.values if isinstance(self.n_train, pd.Series) else self.n_train
        self.n_test = self.n_test.values if isinstance(self.n_test, pd.Series) else self.n_test
        self.p_train = self.p_train.values if isinstance(self.p_train, pd.Series) else self.p_train
        self.p_test = self.p_test.values if isinstance(self.p_test, pd.Series) else self.p_test
        self.r_train = self.r_train.values if isinstance(self.r_train, pd.Series) else self.r_train
        self.r_test = self.r_test.values if isinstance(self.r_test, pd.Series) else self.r_test

        # Scale the target values with separate scalers
        self.b_train_scaled = self.target_scaler_b.fit_transform(self.b_train.reshape(-1, 1)).flatten()
        self.b_test_scaled = self.target_scaler_b.transform(self.b_test.reshape(-1, 1)).flatten()
        self.d_train_scaled = self.target_scaler_d.fit_transform(self.d_train.reshape(-1, 1)).flatten()
        self.d_test_scaled = self.target_scaler_d.transform(self.d_test.reshape(-1, 1)).flatten()
        self.f_train_scaled = self.target_scaler_f.fit_transform(self.f_train.reshape(-1, 1)).flatten()
        self.f_test_scaled = self.target_scaler_f.transform(self.f_test.reshape(-1, 1)).flatten()
        self.h_train_scaled = self.target_scaler_h.fit_transform(self.h_train.reshape(-1, 1)).flatten()
        self.h_test_scaled = self.target_scaler_h.transform(self.h_test.reshape(-1, 1)).flatten()
        self.j_train_scaled = self.target_scaler_j.fit_transform(self.j_train.reshape(-1, 1)).flatten()
        self.j_test_scaled = self.target_scaler_j.transform(self.j_test.reshape(-1, 1)).flatten()
        self.l_train_scaled = self.target_scaler_l.fit_transform(self.l_train.reshape(-1, 1)).flatten()
        self.l_test_scaled = self.target_scaler_l.transform(self.l_test.reshape(-1, 1)).flatten()
        self.n_train_scaled = self.target_scaler_n.fit_transform(self.n_train.reshape(-1, 1)).flatten()
        self.n_test_scaled = self.target_scaler_n.transform(self.n_test.reshape(-1, 1)).flatten()
        self.p_train_scaled = self.target_scaler_p.fit_transform(self.p_train.reshape(-1, 1)).flatten()
        self.p_test_scaled = self.target_scaler_p.transform(self.p_test.reshape(-1, 1)).flatten()
        self.r_train_scaled = self.target_scaler_r.fit_transform(self.r_train.reshape(-1, 1)).flatten()
        self.r_test_scaled = self.target_scaler_r.transform(self.r_test.reshape(-1, 1)).flatten()
        print("Scaling completed.")

    def train_model(self):
        """
        Train the XGBoost models.
        """
        print("Training XGBoost models...")
        self.model_A = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_C = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_E = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_G = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_I = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_K = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_M = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_O = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)
        self.model_Q = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.5, max_depth=15, subsample=0.9, colsample_bytree=0.8, random_state=42)

        # Train models
        self.model_A.fit(self.A_train_scaled, self.b_train_scaled)
        self.model_C.fit(self.C_train_scaled, self.d_train_scaled)
        self.model_E.fit(self.E_train_scaled, self.f_train_scaled)
        self.model_G.fit(self.G_train_scaled, self.h_train_scaled)
        self.model_I.fit(self.I_train_scaled, self.j_train_scaled)
        self.model_K.fit(self.K_train_scaled, self.l_train_scaled)
        self.model_M.fit(self.M_train_scaled, self.n_train_scaled)
        self.model_O.fit(self.O_train_scaled, self.p_train_scaled)
        self.model_Q.fit(self.Q_train_scaled, self.r_train_scaled)
        print("Model training completed.")

    def predict(self):
        """
        Make predictions on the test set and inverse transform.
        """
        print("Making predictions...")
        bhat_scaled = self.model_A.predict(self.A_test_scaled)
        self.inv_bhat = self.target_scaler_b.inverse_transform(bhat_scaled.reshape(-1, 1)).flatten()
        self.inv_b = self.target_scaler_b.inverse_transform(self.b_test_scaled.reshape(-1, 1)).flatten()

        dhat_scaled = self.model_C.predict(self.C_test_scaled)
        self.inv_dhat = self.target_scaler_d.inverse_transform(dhat_scaled.reshape(-1, 1)).flatten()
        self.inv_d = self.target_scaler_d.inverse_transform(self.d_test_scaled.reshape(-1, 1)).flatten()

        fhat_scaled = self.model_E.predict(self.E_test_scaled)
        self.inv_fhat = self.target_scaler_f.inverse_transform(fhat_scaled.reshape(-1, 1)).flatten()
        self.inv_f = self.target_scaler_f.inverse_transform(self.f_test_scaled.reshape(-1, 1)).flatten()

        hhat_scaled = self.model_G.predict(self.G_test_scaled)
        self.inv_hhat = self.target_scaler_h.inverse_transform(hhat_scaled.reshape(-1, 1)).flatten()
        self.inv_h = self.target_scaler_h.inverse_transform(self.h_test_scaled.reshape(-1, 1)).flatten()

        jhat_scaled = self.model_I.predict(self.I_test_scaled)
        self.inv_jhat = self.target_scaler_j.inverse_transform(jhat_scaled.reshape(-1, 1)).flatten()
        self.inv_j = self.target_scaler_j.inverse_transform(self.j_test_scaled.reshape(-1, 1)).flatten()

        lhat_scaled = self.model_K.predict(self.K_test_scaled)
        self.inv_lhat = self.target_scaler_l.inverse_transform(lhat_scaled.reshape(-1, 1)).flatten()
        self.inv_l = self.target_scaler_l.inverse_transform(self.l_test_scaled.reshape(-1, 1)).flatten()

        nhat_scaled = self.model_M.predict(self.M_test_scaled)
        self.inv_nhat = self.target_scaler_n.inverse_transform(nhat_scaled.reshape(-1, 1)).flatten()
        self.inv_n = self.target_scaler_n.inverse_transform(self.n_test_scaled.reshape(-1, 1)).flatten()

        phat_scaled = self.model_O.predict(self.O_test_scaled)
        self.inv_phat = self.target_scaler_p.inverse_transform(phat_scaled.reshape(-1, 1)).flatten()
        self.inv_p = self.target_scaler_p.inverse_transform(self.p_test_scaled.reshape(-1, 1)).flatten()

        rhat_scaled = self.model_Q.predict(self.Q_test_scaled)
        self.inv_rhat = self.target_scaler_r.inverse_transform(rhat_scaled.reshape(-1, 1)).flatten()
        self.inv_r = self.target_scaler_r.inverse_transform(self.r_test_scaled.reshape(-1, 1)).flatten()
        print("Predictions completed.")

    def evaluate_model(self):
        """
        Evaluate and plot results.
        """
        print("Evaluating model...")
        rmse1 = np.sqrt(mean_squared_error(self.inv_b, self.inv_bhat))
        print(f'RMSE Aluminum Purity (%): {rmse1:.3f}')

        rmse2 = np.sqrt(mean_squared_error(self.inv_d, self.inv_dhat))
        print(f'RMSE Casting Temperature (°C): {rmse2:.3f}')

        rmse3 = np.sqrt(mean_squared_error(self.inv_f, self.inv_fhat))
        print(f'RMSE Cooling Water Temperature (°C): {rmse3:.3f}')

        rmse4 = np.sqrt(mean_squared_error(self.inv_h, self.inv_hhat))
        print(f'RMSE Casting Speed (m/min): {rmse4:.3f}')

        rmse5 = np.sqrt(mean_squared_error(self.inv_j, self.inv_jhat))
        print(f'RMSE Cast Bar Entry Temperature at Rolling Mill (°C): {rmse5:.3f}')

        rmse6 = np.sqrt(mean_squared_error(self.inv_l, self.inv_lhat))
        print(f'RMSE Emulsion Temperature at Rolling Mill (°C): {rmse6:.3f}')

        rmse7 = np.sqrt(mean_squared_error(self.inv_n, self.inv_nhat))
        print(f'RMSE Emulsion Pressure at Rolling Mill (bar): {rmse7:.3f}')

        rmse8 = np.sqrt(mean_squared_error(self.inv_p, self.inv_phat))
        print(f'RMSE Emulsion Concentration (%): {rmse8:.3f}')

        rmse9 = np.sqrt(mean_squared_error(self.inv_r, self.inv_rhat))
        print(f'RMSE Rod Quench Water Pressure (bar): {rmse9:.3f}')

        results_df_1 = pd.DataFrame({
            'Actual': self.inv_b,
            'Predicted': self.inv_bhat
        })
        results_file_1 = self.results_path / 'test_results_xgboost_Aluminum Purity (%).csv'
        results_df_1.to_csv(results_file_1, index=False)
        print(f"Results saved to '{results_file_1}'")

        results_df_2 = pd.DataFrame({
            'Actual': self.inv_d,
            'Predicted': self.inv_dhat
        })
        results_file_2 = self.results_path / 'test_results_Casting Temperature (°C).csv'
        results_df_2.to_csv(results_file_2, index=False)
        print(f"Results saved to '{results_file_2}'")

        results_df_3 = pd.DataFrame({
            'Actual': self.inv_f,
            'Predicted': self.inv_fhat
        })
        results_file_3 = self.results_path / 'test_results_xgboost_Cooling Water Temperature (°C).csv'
        results_df_3.to_csv(results_file_3, index=False)
        print(f"Results saved to '{results_file_3}'")

        results_df_4 = pd.DataFrame({
            'Actual': self.inv_h,
            'Predicted': self.inv_hhat
        })
        results_file_4 = self.results_path / 'test_results_xgboost_Casting Speed.csv'
        results_df_4.to_csv(results_file_4, index=False)
        print(f"Results saved to '{results_file_4}'")

        results_df_5 = pd.DataFrame({
            'Actual': self.inv_j,
            'Predicted': self.inv_jhat
        })
        results_file_5 = self.results_path / 'test_results_xgboost_Cast Bar Entry Temperature at Rolling Mill (°C).csv'
        results_df_5.to_csv(results_file_5, index=False)
        print(f"Results saved to '{results_file_5}'")

        results_df_6 = pd.DataFrame({
            'Actual': self.inv_l,
            'Predicted': self.inv_lhat
        })
        results_file_6 = self.results_path / 'test_results_xgboost_Emulsion Temperature at Rolling Mill (°C).csv'
        results_df_6.to_csv(results_file_6, index=False)
        print(f"Results saved to '{results_file_6}'")

        results_df_7 = pd.DataFrame({
            'Actual': self.inv_n,
            'Predicted': self.inv_nhat
        })
        results_file_7 = self.results_path / 'test_results_xgboost_Emulsion Pressure at Rolling Mill (bar).csv'
        results_df_7.to_csv(results_file_7, index=False)
        print(f"Results saved to '{results_file_7}'")

        results_df_8 = pd.DataFrame({
            'Actual': self.inv_p,
            'Predicted': self.inv_phat
        })
        results_file_8 = self.results_path / 'test_results_xgboost_Emulsion Concentration (%).csv'
        results_df_8.to_csv(results_file_8, index=False)
        print(f"Results saved to '{results_file_8}'")

        results_df_9 = pd.DataFrame({
            'Actual': self.inv_r,
            'Predicted': self.inv_rhat
        })
        results_file_9 = self.results_path / 'test_results_xgboost_Rod Quench Water Pressure (bar).csv'
        results_df_9.to_csv(results_file_9, index=False)
        print(f"Results saved to '{results_file_9}'")

    def save_model(self):
        """
        Save the trained model to the specified directory.
        """
        print("Saving the model...")
        model_file_1 = self.model_path / 'xgboost_model_Aluminum Purity (%).joblib'
        joblib.dump(self.model_A, model_file_1)
        print(f"Model saved to '{model_file_1}'")

        model_file_2 = self.model_path / 'xgboost_model_Casting Temperature (°C).joblib'
        joblib.dump(self.model_C, model_file_2)
        print(f"Model saved to '{model_file_2}'")

        model_file_3 = self.model_path / 'xgboost_model_Cooling Water Temperature (°C).joblib'
        joblib.dump(self.model_E, model_file_3)
        print(f"Model saved to '{model_file_3}'")

        model_file_4 = self.model_path / 'xgboost_model_Casting Speed.joblib'
        joblib.dump(self.model_G, model_file_4)
        print(f"Model saved to '{model_file_4}'")

        model_file_5 = self.model_path / 'xgboost_model_Cast Bar Entry Temperature at Rolling Mill (°C).joblib'
        joblib.dump(self.model_I, model_file_5)
        print(f"Model saved to '{model_file_5}'")

        model_file_6 = self.model_path / 'xgboost_model_Emulsion Temperature at Rolling Mill (°C).joblib'
        joblib.dump(self.model_K, model_file_6)
        print(f"Model saved to '{model_file_6}'")

        model_file_7 = self.model_path / 'xgboost_model_Emulsion Pressure at Rolling Mill (bar).joblib'
        joblib.dump(self.model_M, model_file_7)
        print(f"Model saved to '{model_file_7}'")

        model_file_8 = self.model_path / 'xgboost_model_Emulsion Concentration (%).joblib'
        joblib.dump(self.model_O, model_file_8)
        print(f"Model saved to '{model_file_8}'")

        model_file_9 = self.model_path / 'xgboost_model_Rod Quench Water Pressure (bar).joblib'
        joblib.dump(self.model_Q, model_file_9)
        print(f"Model saved to '{model_file_9}'")

        # Save scalers
        scaler_file_b = self.model_path / 'target_scaler_bn.joblib'
        joblib.dump(self.target_scaler_b, scaler_file_b)
        print(f"Target scaler for Elongation saved to '{scaler_file_b}'")

        scaler_file_d = self.model_path / 'target_scaler_dn.joblib'
        joblib.dump(self.target_scaler_d, scaler_file_d)
        print(f"Target scaler for UTS saved to '{scaler_file_d}'")

        scaler_file_f = self.model_path / 'target_scaler_fn.joblib'
        joblib.dump(self.target_scaler_f, scaler_file_f)
        print(f"Target scaler for Conductivity saved to '{scaler_file_f}'")

        scaler_file_h = self.model_path / 'target_scaler_hn.joblib'
        joblib.dump(self.target_scaler_h, scaler_file_h)
        print(f"Target scaler for Elongation saved to '{scaler_file_h}'")

        scaler_file_j = self.model_path / 'target_scaler_jn.joblib'
        joblib.dump(self.target_scaler_j, scaler_file_j)
        print(f"Target scaler for UTS saved to '{scaler_file_j}'")

        scaler_file_l = self.model_path / 'target_scaler_ln.joblib'
        joblib.dump(self.target_scaler_l, scaler_file_l)
        print(f"Target scaler for Conductivity saved to '{scaler_file_l}'")

        scaler_file_n = self.model_path / 'target_scaler_nn.joblib'
        joblib.dump(self.target_scaler_n, scaler_file_n)
        print(f"Target scaler for Elongation saved to '{scaler_file_n}'")

        scaler_file_p = self.model_path / 'target_scaler_pn.joblib'
        joblib.dump(self.target_scaler_p, scaler_file_p)
        print(f"Target scaler for UTS saved to '{scaler_file_p}'")

        scaler_file_r = self.model_path / 'target_scaler_rn.joblib'
        joblib.dump(self.target_scaler_r, scaler_file_r)
        print(f"Target scaler for Conductivity saved to '{scaler_file_r}'")
        
        
    def run_training(self):
        """
        Complete pipeline.
        """
        self.scale_data()
        self.train_model()
        self.predict()
        self.evaluate_model()
        self.save_model()

import pandas as pd

if __name__ == "__main__":
    A_train = pd.read_csv('data/processed/backward/A_train.csv')
    A_test = pd.read_csv('data/processed/backward/A_test.csv')
    b_train = pd.read_csv('data/processed/backward/b_train.csv').squeeze()
    b_test = pd.read_csv('data/processed/backward/b_test.csv').squeeze()
    C_train = pd.read_csv('data/processed/backward/C_train.csv')
    C_test = pd.read_csv('data/processed/backward/C_test.csv')
    d_train = pd.read_csv('data/processed/backward/d_train.csv').squeeze()
    d_test = pd.read_csv('data/processed/backward/d_test.csv').squeeze()
    E_train = pd.read_csv('data/processed/backward/E_train.csv')
    E_test = pd.read_csv('data/processed/backward/E_test.csv')
    f_train = pd.read_csv('data/processed/backward/f_train.csv').squeeze()
    f_test = pd.read_csv('data/processed/backward/f_test.csv').squeeze()
    G_train = pd.read_csv('data/processed/backward/G_train.csv')
    G_test = pd.read_csv('data/processed/backward/G_test.csv')
    h_train = pd.read_csv('data/processed/backward/h_train.csv').squeeze()
    h_test = pd.read_csv('data/processed/backward/h_test.csv').squeeze()
    I_train = pd.read_csv('data/processed/backward/I_train.csv')
    I_test = pd.read_csv('data/processed/backward/I_test.csv')
    j_train = pd.read_csv('data/processed/backward/j_train.csv').squeeze()
    j_test = pd.read_csv('data/processed/backward/j_test.csv').squeeze()
    K_train = pd.read_csv('data/processed/backward/K_train.csv')
    K_test = pd.read_csv('data/processed/backward/K_test.csv')
    l_train = pd.read_csv('data/processed/backward/l_train.csv').squeeze()
    l_test = pd.read_csv('data/processed/backward/l_test.csv').squeeze()
    M_train = pd.read_csv('data/processed/backward/M_train.csv')
    M_test = pd.read_csv('data/processed/backward/M_test.csv')
    n_train = pd.read_csv('data/processed/backward/n_train.csv').squeeze()
    n_test = pd.read_csv('data/processed/backward/n_test.csv').squeeze()
    O_train = pd.read_csv('data/processed/backward/O_train.csv')
    O_test = pd.read_csv('data/processed/backward/O_test.csv')
    p_train = pd.read_csv('data/processed/backward/p_train.csv').squeeze()
    p_test = pd.read_csv('data/processed/backward/p_test.csv').squeeze()
    Q_train = pd.read_csv('data/processed/backward/Q_train.csv')
    Q_test = pd.read_csv('data/processed/backward/Q_test.csv')
    r_train = pd.read_csv('data/processed/backward/r_train.csv').squeeze()
    r_test = pd.read_csv('data/processed/backward/r_test.csv').squeeze()

    # Initialize and run training
    training = Training(
        A_train, A_test, b_train, b_test, C_train, C_test, d_train, d_test, 
        E_train, E_test, f_train, f_test, G_train, G_test, h_train, h_test, 
        I_train, I_test, j_train, j_test, K_train, K_test, l_train, l_test, 
        M_train, M_test, n_train, n_test, O_train, O_test, p_train, p_test, 
        Q_train, Q_test, r_train, r_test
    )
    training.run_training()

