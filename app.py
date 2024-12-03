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
    ingest = DataIngestion(url='https://docs.google.com/spreadsheets/d/1i5SKBS7lr6nBPC2OTOF8Bj6sXiWAcKEj58Vg7ssdaKQ/export?format=csv', save_path='data/processed/uploaded_files/input_data.csv')
    ingest.ingest_data()

    preprocess = Preprocessing()
    preprocess.run_preprocessing()

    input_csv_path = 'data/processed/uploaded_files/scaled_data.csv'
    
    # Run predictions with model_eval.py
    model_eval = ModelEvalPredict(feature_csv=input_csv_path)
    elongation, uts, conductivity = model_eval.run_prediction()

    elongation = float(elongation[9])
    uts = float(uts[9])
    conductivity = float(conductivity[9])

    intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
    desired_csv_path = 'data/processed/uploaded_files/desired_values.csv'
    
    output_data = {
        "Elongation": [elongation],
        "UTS": [uts],
        "Conductivity": [conductivity]
    }
    pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)

    model_eval_mini = ModelEvalMiniPredict(feature_csv=desired_csv_path)
    results = model_eval_mini.run_pipeline()
    
    # Fetch original values
    original = pd.read_csv('data/processed/uploaded_files/input_data.csv').iloc[-1:]
    original_values = {
        "A": original['EMUL_OIL_L_TEMP_PV_VAL0'].values[0],
        "B": original['STAND_OIL_L_TEMP_PV_REAL_VAL0'].values[0],
        "C": original['GEAR_OIL_L_TEMP_PV_REAL_VAL0'].values[0],
        "D": original['EMUL_OIL_L_PR_VAL0'].values[0],
        "E": original['QUENCH_CW_FLOW_EXIT_VAL0'].values[0],
        "F": original['CAST_WHEEL_RPM_VAL0'].values[0],
        "G": original['BAR_TEMP_VAL0'].values[0],
        "H": original['QUENCH_CW_FLOW_ENTRY_VAL0'].values[0],
        "I": original['GEAR_OIL_L_PR_VAL0'].values[0],
        "J": original['STANDS_OIL_L_PR_VAL0'].values[0],
        "K": original['TUNDISH_TEMP_VAL0'].values[0],
        "L": original['BATH_TEMP_F7_VAL0'].values[0],
        "M": original['BATH_TEMP_F8_VAL0'].values[0],
        "N": original['RM_MOTOR_COOL_WATER__VAL0'].values[0],
        "O": original['ROLL_MILL_AMPS_VAL0'].values[0],
        "P": original['RM_COOL_WATER_FLOW_VAL0'].values[0],
        "Q": original['EMULSION_LEVEL_ANALO_VAL0'].values[0],
        "R": original['pctAL'].values[0]
    }
    
    # Calculate differences
    differences = {
        "A": original_values["A"] - results['EMUL_OIL_L_TEMP_PV_VAL0'],
        "B": original_values["B"] - results['STAND_OIL_L_TEMP_PV_REAL_VAL0'],
        "C": original_values["C"] - results['GEAR_OIL_L_TEMP_PV_REAL_VAL0'],
        "D": original_values["D"] - results['EMUL_OIL_L_PR_VAL0'],
        "E": original_values["E"] - results['QUENCH_CW_FLOW_EXIT_VAL0'],
        "F": original_values["F"] - results['CAST_WHEEL_RPM_VAL0'],
        "G": original_values["G"] - results['BAR_TEMP_VAL0'],
        "H": original_values["H"] - results['QUENCH_CW_FLOW_ENTRY_VAL0'],
        "I": original_values["I"] - results['GEAR_OIL_L_PR_VAL0'],
        "J": original_values["J"] - results['STANDS_OIL_L_PR_VAL0'],
        "K": original_values["K"] - results['TUNDISH_TEMP_VAL0'],
        "L": original_values["L"] - results['BATH_TEMP_F7_VAL0'],
        "M": original_values["M"] - results['BATH_TEMP_F8_VAL0'],
        "N": original_values["N"] - results['RM_MOTOR_COOL_WATER__VAL0'],
        "O": original_values["O"] - results['ROLL_MILL_AMPS_VAL0'],
        "P": original_values["P"] - results['RM_COOL_WATER_FLOW_VAL0'],
        "Q": original_values["Q"] - results['EMULSION_LEVEL_ANALO_VAL0'],
        "R": original_values["R"] - results['pctAL']
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
