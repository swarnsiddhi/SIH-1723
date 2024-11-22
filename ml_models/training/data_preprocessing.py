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
        self.processed_data_path = self.current_dir / 'data' / 'processed' / 'forward'
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
        features = self.df.drop(columns=['Elongation (%)', 'Ultimate Tensile Strength (UTS) (MPa)', 'Conductivity (% IACS)'])
        target_column_1 = self.df['Elongation (%)']
        target_column_2 = self.df['Ultimate Tensile Strength (UTS) (MPa)']
        target_column_3 = self.df['Conductivity (% IACS)']

        # Scale features
        scaled_features = scaler.fit_transform(features)
        self.df_scaled = pd.DataFrame(scaled_features, columns=features.columns)

        # Add the target column back to the DataFrame
        self.df_scaled['Elongation (%)'] = target_column_1.values
        self.df_scaled['Ultimate Tensile Strength (UTS) (MPa)'] = target_column_2.values
        self.df_scaled['Conductivity (% IACS)'] = target_column_3.values
        print("Features scaled successfully.")

    def split_data(self):
        """Split the data into training and testing sets and save them."""
        print("Splitting data into training and testing sets...")
        X = self.df_scaled.drop(columns=['Elongation (%)','Ultimate Tensile Strength (UTS) (MPa)','Conductivity (% IACS)'])
        y = self.df_scaled['Elongation (%)']
        A = self.df_scaled.drop(columns=['Elongation (%)','Ultimate Tensile Strength (UTS) (MPa)','Conductivity (% IACS)'])
        b = self.df_scaled['Ultimate Tensile Strength (UTS) (MPa)']
        R = self.df_scaled.drop(columns=['Elongation (%)','Ultimate Tensile Strength (UTS) (MPa)','Conductivity (% IACS)'])
        s = self.df_scaled['Conductivity (% IACS)']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        A_train, A_test, b_train, b_test = train_test_split(A, b, test_size=0.2, random_state=42)
        R_train, R_test, s_train, s_test = train_test_split(R, s, test_size=0.2, random_state=42)
        print("Data split completed.")

        # Save the splits
        pd.DataFrame(X_train).to_csv(self.processed_data_path / 'X_train_E.csv', index=False)
        pd.DataFrame(X_test).to_csv(self.processed_data_path / 'X_test_E.csv', index=False)
        pd.DataFrame(y_train).to_csv(self.processed_data_path / 'y_train_E.csv', index=False)
        pd.DataFrame(y_test).to_csv(self.processed_data_path / 'y_test_E.csv', index=False)
        pd.DataFrame(A_train).to_csv(self.processed_data_path / 'A_train_UTS.csv', index=False)
        pd.DataFrame(A_test).to_csv(self.processed_data_path / 'A_test_UTS.csv', index=False)
        pd.DataFrame(b_train).to_csv(self.processed_data_path / 'b_train_UTS.csv', index=False)
        pd.DataFrame(b_test).to_csv(self.processed_data_path / 'b_test_UTS.csv', index=False)
        pd.DataFrame(R_train).to_csv(self.processed_data_path / 'R_train_C.csv', index=False)
        pd.DataFrame(R_test).to_csv(self.processed_data_path / 'R_test_C.csv', index=False)
        pd.DataFrame(s_train).to_csv(self.processed_data_path / 's_train_C.csv', index=False)
        pd.DataFrame(s_test).to_csv(self.processed_data_path / 's_test_C.csv', index=False)
        print("Processed files saved to the 'data/processed' directory.")

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
