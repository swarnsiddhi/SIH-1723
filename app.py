from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import sqlite3
from ml_models.training.model_eval import Predict as ModelEvalPredict
from ml_models.training.model_eval_mini import Predict as ModelEvalMiniPredict
from scripts.ingest_data import DataIngestion
from scripts.preprocess_data import Preprocessing
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

DATABASE = 'features.db'

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

@app.route('/api/save_features', methods=['POST'])
def save_features():
    try:
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

        output_data = {
            "Elongation": [elongation_d],
            "UTS": [uts_d],
            "Conductivity": [conductivity_d]
        }
        pd.DataFrame(output_data).to_csv('data/processed/uploaded_files/desired_values.csv', index=False)

        return jsonify({"message": "Features saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/final_prediction', methods=['GET'])
def final_prediction():
    ingest = DataIngestion(url='https://docs.google.com/spreadsheets/d/1eqNiMixvg9GqAOzCBoQPNG7fpYb9pE9chQuNxl9-8Sk/export?format=csv', save_path='data/processed/uploaded_files/input_data.csv')
    ingest.ingest_data()

    preprocess = Preprocessing()
    preprocess.run_preprocessing()

    input_csv_path = 'data/processed/uploaded_files/scaled_data.csv'
    
    # Run predictions with model_eval.py
    model_eval = ModelEvalPredict(feature_csv=input_csv_path)
    elongation, uts, conductivity = model_eval.run_prediction()

    elongation = float(elongation)
    uts = float(uts)
    conductivity = float(conductivity)

    intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
    desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
    
    output_data = {
        "Elongation": [elongation],
        "UTS": [uts],
        "Conductivity": [conductivity]
    }
    pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)

    model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
    A,B,C,D,E,F,G,H,I = model_eval_mini.run_prediction()
    
    # Fetch original values
    original = pd.read_csv('data/processed/uploaded_files/input_data.csv').iloc[-1:]
    original_values = {
        "A": original['Aluminum Purity (%)'].values[0],
        "B": original['Casting Temperature (°C)'].values[0],
        "C": original['Cooling Water Temperature (°C)'].values[0],
        "D": original['Casting Speed (m/min)'].values[0],
        "E": original['Cast Bar Entry Temperature at Rolling Mill (°C)'].values[0],
        "F": original['Emulsion Temperature at Rolling Mill (°C)'].values[0],
        "G": original['Emulsion Pressure at Rolling Mill (bar)'].values[0],
        "H": original['Emulsion Concentration (%)'].values[0],
        "I": original['Rod Quench Water Pressure (bar)'].values[0]
    }
    
    # Calculate differences
    differences = {
        "A": original_values["A"] - A,
        "B": original_values["B"] - B,
        "C": original_values["C"] - C,
        "D": original_values["D"] - D,
        "E": original_values["E"] - E,
        "F": original_values["F"] - F,
        "G": original_values["G"] - G,
        "H": original_values["H"] - H,
        "I": original_values["I"] - I
    }
    
    response = {
        "predictions": {
            "elongation": elongation,
            "uts": uts,
            "conductivity": conductivity
        },
        "differences": differences
    }

    try:
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
