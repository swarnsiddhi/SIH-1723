from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
import pandas as pd
import sqlite3
from flask_cors import CORS
from ml_models.training.model_eval import Predict as ModelEvalPredict
from ml_models.training.model_eval_mini import Predict as ModelEvalMiniPredict
from scripts.ingest_data import DataIngestion
from scripts.preprocess_data import Preprocessing
from flask_apscheduler import APScheduler
import os

app = Flask(__name__, static_folder="frontend/dist", static_url_path="/")
CORS(app)
scheduler = APScheduler()

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
def serve_frontend():
    """
    Serve the frontend application.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/predict', methods=['GET'])
def predict():
    """
    Run the prediction pipeline using a continuously refreshing CSV file.
    """
    ingest = DataIngestion(
        url='https://docs.google.com/spreadsheets/d/1eqNiMixvg9GqAOzCBoQPNG7fpYb9pE9chQuNxl9-8Sk/export?format=csv',
        save_path='data/processed/uploaded_files/input_data.csv'
    )
    ingest.ingest_data()

    preprocess = Preprocessing()
    preprocess.run_preprocessing()

    try:
        input_csv_path = 'data/processed/uploaded_files/scaled_data.csv'
        model_eval = ModelEvalPredict(feature_csv=input_csv_path)
        elongation, uts, conductivity = model_eval.run_prediction()

        elongation = float(elongation)
        uts = float(uts)
        conductivity = float(conductivity)

        return jsonify({
            "elongation": elongation,
            "uts": uts,
            "conductivity": conductivity
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save_features', methods=['POST'])
def save_features():
    """
    Save manually entered intermediate features to the database
    and generate the final prediction.
    """
    try:
        # Save features to the database
        data = request.json
        elongation_d = float(data['elongation'])
        uts_d = float(data['uts'])
        conductivity_d = float(data['conductivity'])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO features (elongation, uts, conductivity) VALUES (?, ?, ?)',
                       (elongation_d, uts_d, conductivity_d))
        conn.commit()
        conn.close()

        # Save features to the desired CSV file
        output_data = {
            "Elongation": [elongation_d],
            "UTS": [uts_d],
            "Conductivity": [conductivity_d]
        }
        desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
        pd.DataFrame(output_data).to_csv(desired_csv_path, index=False)

        # Generate final prediction
        model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
        predictions = model_eval_mini.run_prediction()

        return jsonify({
            "message": "Features saved successfully!",
            "original_values": output_data,
            "predictions": predictions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/final_prediction', methods=['POST'])
def final_prediction():
    """
    Generate the final prediction and return results to the frontend.
    """
    try:
        input_data = request.json
        elongation = float(input_data.get('elongation', 0))
        uts = float(input_data.get('uts', 0))
        conductivity = float(input_data.get('conductivity', 0))

        intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
        desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
        output_data = {
            "Elongation": [elongation],
            "UTS": [uts],
            "Conductivity": [conductivity]
        }
        pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)

        model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
        predictions = model_eval_mini.run_prediction()

        return jsonify({
            "original_values": output_data,
            "predictions": predictions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_predictions():
    """
    Automatically run predict and final_prediction logic.
    """
    try:
        ingest = DataIngestion(
            url='https://docs.google.com/spreadsheets/d/1eqNiMixvg9GqAOzCBoQPNG7fpYb9pE9chQuNxl9-8Sk/export?format=csv',
            save_path='data/processed/uploaded_files/input_data.csv'
        )
        ingest.ingest_data()

        preprocess = Preprocessing()
        preprocess.run_preprocessing()

        input_csv_path = 'data/processed/uploaded_files/scaled_data.csv'
        desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
        model_eval = ModelEvalPredict(feature_csv=input_csv_path)
        elongation, uts, conductivity = model_eval.run_prediction()

        output_data = {
            "Elongation": [float(elongation)],
            "UTS": [float(uts)],
            "Conductivity": [float(conductivity)]
        }
        intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
        pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)

        model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
        predictions = model_eval_mini.run_prediction()

    except Exception as e:
        app.logger.error(f"Error in run_predictions: {str(e)}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
