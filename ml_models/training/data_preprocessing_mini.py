import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class Preprocessing:
    def __init__(self):
        # Set up paths
        self.current_dir = Path.cwd()
        self.raw_data_path = self.current_dir / 'data' / 'raw' / 'wire-rod-production'
        self.processed_data_path = self.current_dir / 'data' / 'processed' / 'backward'
        self.processed_data_path.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        """Load the CSV data."""
        try:
            self.df = pd.read_csv(self.raw_data_path)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"File not found at path: {self.raw_data_path}")
            raise

    def clean_data(self):
        """Handle missing values and remove outliers using Z-score."""
        # Check for missing values
        print("Checking for missing values...")
        missing_values = self.df.isnull().sum()
        print(missing_values)

        # Drop rows with missing values if any
        self.df.dropna(inplace=True)
        print("Missing values dropped (if any).")

        # Remove rows with Z-score > 3 for outlier removal
        print("Removing outliers...")
        self.df = self.df[(np.abs(zscore(self.df)) < 3).all(axis=1)]
        print("Outliers removed.")

    def scale_features(self):
        """Scale the features using StandardScaler."""
        print("Scaling features...")
        scaler = StandardScaler()

        # Separate the features and target column
        features = self.df[['Elongation (%)', 'Ultimate Tensile Strength (UTS) (MPa)', 'Conductivity (% IACS)']]
        target_column_1 = self.df['Aluminum Purity (%)']
        target_column_2 = self.df['Casting Temperature (°C)']
        target_column_3 = self.df['Cooling Water Temperature (°C)']
        target_column_4 = self.df['Casting Speed (m/min)']
        target_column_5 = self.df['Cast Bar Entry Temperature at Rolling Mill (°C)']
        target_column_6 = self.df['Emulsion Temperature at Rolling Mill (°C)']
        target_column_7 = self.df['Emulsion Pressure at Rolling Mill (bar)']
        target_column_8 = self.df['Emulsion Concentration (%)']
        target_column_9 = self.df['Rod Quench Water Pressure (bar)']

        # Scale features
        scaled_features = scaler.fit_transform(features)
        self.df_scaled = pd.DataFrame(scaled_features, columns=features.columns)

        # Add the target column back to the DataFrame
        self.df_scaled['Aluminum Purity (%)'] = target_column_1.values
        self.df_scaled['Casting Temperature (°C)'] = target_column_2.values
        self.df_scaled['Cooling Water Temperature (°C)'] = target_column_3.values
        self.df_scaled['Casting Speed (m/min)'] = target_column_4.values
        self.df_scaled['Cast Bar Entry Temperature at Rolling Mill (°C)'] = target_column_5.values
        self.df_scaled['Emulsion Temperature at Rolling Mill (°C)'] = target_column_6.values
        self.df_scaled['Emulsion Pressure at Rolling Mill (bar)'] = target_column_7.values
        self.df_scaled['Emulsion Concentration (%)'] = target_column_8.values
        self.df_scaled['Rod Quench Water Pressure (bar)'] = target_column_9.values
        print("Features scaled successfully.")

    def split_data(self):
        """Split the data into training and testing sets and save them."""
        print("Splitting data into training and testing sets...")
        A = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        b = self.df_scaled['Aluminum Purity (%)']
        C = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        d = self.df_scaled['Casting Temperature (°C)']
        E = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        f = self.df_scaled['Cooling Water Temperature (°C)']
        G = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        h = self.df_scaled['Casting Speed (m/min)']
        I = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        j = self.df_scaled['Cast Bar Entry Temperature at Rolling Mill (°C)']
        K = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        l = self.df_scaled['Emulsion Temperature at Rolling Mill (°C)']
        M = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        n = self.df_scaled['Emulsion Pressure at Rolling Mill (bar)']
        O = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        p = self.df_scaled['Emulsion Concentration (%)']
        Q = self.df_scaled.drop(columns=['Aluminum Purity (%)','Casting Temperature (°C)','Cooling Water Temperature (°C)','Casting Speed (m/min)','Cast Bar Entry Temperature at Rolling Mill (°C)'
                                         ,'Emulsion Temperature at Rolling Mill (°C)','Emulsion Pressure at Rolling Mill (bar)','Emulsion Concentration (%)','Rod Quench Water Pressure (bar)'])
        r = self.df_scaled['Rod Quench Water Pressure (bar)']

        A_train, A_test, b_train, b_test = train_test_split(A, b, test_size=0.2, random_state=42)
        C_train, C_test, d_train, d_test = train_test_split(C, d, test_size=0.2, random_state=42)
        E_train, E_test, f_train, f_test = train_test_split(E, f, test_size=0.2, random_state=42)
        G_train, G_test, h_train, h_test = train_test_split(G, h, test_size=0.2, random_state=42)
        I_train, I_test, j_train, j_test = train_test_split(I, j, test_size=0.2, random_state=42)
        K_train, K_test, l_train, l_test = train_test_split(K, l, test_size=0.2, random_state=42)
        M_train, M_test, n_train, n_test = train_test_split(M, n, test_size=0.2, random_state=42)
        O_train, O_test, p_train, p_test = train_test_split(O, p, test_size=0.2, random_state=42)
        Q_train, Q_test, r_train, r_test = train_test_split(Q, r, test_size=0.2, random_state=42)
        print("Data split completed.")

        # Save the splits
        pd.DataFrame(A_train).to_csv(self.processed_data_path / 'A_train.csv', index=False)
        pd.DataFrame(A_test).to_csv(self.processed_data_path / 'A_test.csv', index=False)
        pd.DataFrame(b_train).to_csv(self.processed_data_path / 'b_train.csv', index=False)
        pd.DataFrame(b_test).to_csv(self.processed_data_path / 'b_test.csv', index=False)
        pd.DataFrame(C_train).to_csv(self.processed_data_path / 'C_train.csv', index=False)
        pd.DataFrame(C_test).to_csv(self.processed_data_path / 'C_test.csv', index=False)
        pd.DataFrame(d_train).to_csv(self.processed_data_path / 'd_train.csv', index=False)
        pd.DataFrame(d_test).to_csv(self.processed_data_path / 'd_test.csv', index=False)
        pd.DataFrame(E_train).to_csv(self.processed_data_path / 'E_train.csv', index=False)
        pd.DataFrame(E_test).to_csv(self.processed_data_path / 'E_test.csv', index=False)
        pd.DataFrame(f_train).to_csv(self.processed_data_path / 'f_train.csv', index=False)
        pd.DataFrame(f_test).to_csv(self.processed_data_path / 'f_test.csv', index=False)
        pd.DataFrame(G_train).to_csv(self.processed_data_path / 'G_train.csv', index=False)
        pd.DataFrame(G_test).to_csv(self.processed_data_path / 'G_test.csv', index=False)
        pd.DataFrame(h_train).to_csv(self.processed_data_path / 'h_train.csv', index=False)
        pd.DataFrame(h_test).to_csv(self.processed_data_path / 'h_test.csv', index=False)
        pd.DataFrame(I_train).to_csv(self.processed_data_path / 'I_train.csv', index=False)
        pd.DataFrame(I_test).to_csv(self.processed_data_path / 'I_test.csv', index=False)
        pd.DataFrame(j_train).to_csv(self.processed_data_path / 'j_train.csv', index=False)
        pd.DataFrame(j_test).to_csv(self.processed_data_path / 'j_test.csv', index=False)
        pd.DataFrame(K_train).to_csv(self.processed_data_path / 'K_train.csv', index=False)
        pd.DataFrame(K_test).to_csv(self.processed_data_path / 'K_test.csv', index=False)
        pd.DataFrame(l_train).to_csv(self.processed_data_path / 'l_train.csv', index=False)
        pd.DataFrame(l_test).to_csv(self.processed_data_path / 'l_test.csv', index=False)
        pd.DataFrame(M_train).to_csv(self.processed_data_path / 'M_train.csv', index=False)
        pd.DataFrame(M_test).to_csv(self.processed_data_path / 'M_test.csv', index=False)
        pd.DataFrame(n_train).to_csv(self.processed_data_path / 'n_train.csv', index=False)
        pd.DataFrame(n_test).to_csv(self.processed_data_path / 'n_test.csv', index=False)
        pd.DataFrame(O_train).to_csv(self.processed_data_path / 'O_train.csv', index=False)
        pd.DataFrame(O_test).to_csv(self.processed_data_path / 'O_test.csv', index=False)
        pd.DataFrame(p_train).to_csv(self.processed_data_path / 'p_train.csv', index=False)
        pd.DataFrame(p_test).to_csv(self.processed_data_path / 'p_test.csv', index=False)
        pd.DataFrame(Q_train).to_csv(self.processed_data_path / 'Q_train.csv', index=False)
        pd.DataFrame(Q_test).to_csv(self.processed_data_path / 'Q_test.csv', index=False)
        pd.DataFrame(r_train).to_csv(self.processed_data_path / 'r_train.csv', index=False)
        pd.DataFrame(r_test).to_csv(self.processed_data_path / 'r_test.csv', index=False)
        print("Processed files saved to the 'data/processed/backward' directory.")

    def run_preprocessing(self):
        """Run all preprocessing steps."""
        self.load_data()
        self.clean_data()
        self.scale_features()
        self.split_data()

if __name__ == "__main__":
    # Instantiate and run the preprocessing pipeline
    preprocess = Preprocessing()
    preprocess.run_preprocessing()
