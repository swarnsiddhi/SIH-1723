from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import sqlite3
from ml_models.training.model_eval import Predict as ModelEvalPredict
from ml_models.training.model_eval_mini import Predict as ModelEvalMiniPredict
from scripts.ingest_data import DataIngestion
from scripts.preprocess_data import Preprocessing

app = Flask(__name__)

# SQLite database setup
DATABASE = 'intermediate_features.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elongation REAL,
            uts REAL,
            conductivity REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """
    Render the homepage with a form to upload the CSV file.
    """
    return render_template('manual_input.html')

@app.route('/predict', methods=['GET'])
def predict():
    """
    Run the prediction pipeline using a continuously refreshing CSV file.
    """

    ingest = DataIngestion(url='https://docs.google.com/spreadsheets/d/1eqNiMixvg9GqAOzCBoQPNG7fpYb9pE9chQuNxl9-8Sk/export?format=csv',save_path='data/processed/uploaded_files/input_data.csv')
    ingest.ingest_data()

    preprocess = Preprocessing()
    preprocess.run_preprocessing()

    try:
        # Define the path for the refreshing CSV file
        input_csv_path = 'data/processed/uploaded_files/scaled_data.csv'
        
        # Run predictions with model_eval.py
        model_eval = ModelEvalPredict(feature_csv=input_csv_path)
        elongation, uts, conductivity = model_eval.run_prediction()

        # Convert predictions to native Python types
        elongation = float(elongation)
        uts = float(uts)
        conductivity = float(conductivity)

        # Render manual input form with predicted values pre-filled
        return redirect(url_for('final_prediction', elongation=elongation, uts=uts, conductivity=conductivity))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/save_features', methods=['POST'])
def save_features():
    """
    Save manually entered intermediate features to the database.
    """
    try:
        elongation_d = float(request.form['elongation'])
        uts_d = float(request.form['uts'])
        conductivity_d = float(request.form['conductivity'])

        # Save to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO features (elongation, uts, conductivity) VALUES (?, ?, ?)',
                       (elongation_d, uts_d, conductivity_d))
        conn.commit()
        conn.close()

        output_data = {
            "Elongation": [elongation_d],
            "UTS": [uts_d],
            "Conductivity": [conductivity_d]
        }
        pd.DataFrame(output_data).to_csv('data/processed/uploaded_files/desired_values.csv', index=False)

        # Redirect to the final prediction step
        return redirect(url_for('predict'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/final_prediction')
def final_prediction():
    try:
        elongation = float(request.args.get('elongation', 0))
        uts = float(request.args.get('uts', 0))
        conductivity = float(request.args.get('conductivity', 0))
        app.logger.info(f"Inputs: elongation={elongation}, uts={uts}, conductivity={conductivity}")

        intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
        desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
        output_data = {
            "Elongation": [elongation],
            "UTS": [uts],
            "Conductivity": [conductivity]
        }
        pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)
        app.logger.info(f"Intermediate features saved: {output_data}")

        model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
        predictions = model_eval_mini.run_prediction()

        app.logger.info(f"Predictions: {predictions}")

        # Assuming original data fetching works
        original = pd.read_csv('data/processed/uploaded_files/input_data.csv').iloc[-1:]
        differences = {f"Feature_{i}": original.iloc[0, i] - predictions[i] for i in range(len(predictions))}

        return render_template('results.html', original_values=output_data, predictions=predictions, differences=differences)
    except Exception as e:
        app.logger.error(f"Error in final_prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
