from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import sqlite3
from ml_models.training.model_eval import Predict as ModelEvalPredict
from ml_models.training.model_eval_mini import Predict as ModelEvalMiniPredict

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
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle CSV upload and run the first prediction pipeline.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save uploaded CSV
        input_csv_path = 'data/processed/uploaded_files/input_features.csv'
        file.save(input_csv_path)

        # Run predictions with model_eval.py
        model_eval = ModelEvalPredict(feature_csv=input_csv_path)
        elongation, uts, conductivity = model_eval.run_prediction()

        # Convert predictions to native Python types
        elongation = float(elongation)
        uts = float(uts)
        conductivity = float(conductivity)

        # Render manual input form with predicted values pre-filled
        return render_template('manual_input.html', elongation=elongation, uts=uts, conductivity=conductivity)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_features', methods=['POST'])
def save_features():
    """
    Save manually entered intermediate features to the database.
    """
    try:
        elongation = float(request.form['elongation'])
        uts = float(request.form['uts'])
        conductivity = float(request.form['conductivity'])

        # Save to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO features (elongation, uts, conductivity) VALUES (?, ?, ?)',
                       (elongation, uts, conductivity))
        conn.commit()
        conn.close()

        # Redirect to the final prediction step
        return redirect(url_for('final_prediction', elongation=elongation, uts=uts, conductivity=conductivity))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/final_prediction')
def final_prediction():
    try:
        elongation = float(request.args['elongation'])
        uts = float(request.args['uts'])
        conductivity = float(request.args['conductivity'])
        app.logger.info(f"Inputs received: elongation={elongation}, uts={uts}, conductivity={conductivity}")

        # Save intermediate features
        output_data = {
            "Elongation": [elongation],
            "UTS": [uts],
            "Conductivity": [conductivity]
        }
        intermediate_csv_path = 'data/processed/uploaded_files/intermediate_features.csv'
        pd.DataFrame(output_data).to_csv(intermediate_csv_path, index=False)
        app.logger.info(f"Intermediate features saved to {intermediate_csv_path}")

        # Model prediction
        try:
            model_eval_mini = ModelEvalMiniPredict(feature_csv=intermediate_csv_path)
            predictions = model_eval_mini.run_prediction()
        except Exception as e:
            app.logger.error(f"Error during model evaluation: {str(e)}")
            return jsonify({"error": "Model evaluation failed"}), 500

        # Original values
        try:
            original = pd.read_csv('data/processed/uploaded_files/input_features.csv').iloc[-1:]
            app.logger.info(f"Original values: {original}")
        except Exception as e:
            app.logger.error(f"Error reading input features: {str(e)}")
            return jsonify({"error": "Failed to read input features"}), 500
        
        predictions = [float(pred) for pred in predictions]

        print("Original values:\n", original[0])
        print("Predicted values:\n", predictions[0])


        # Calculate differences
        try:
            differences = {
            "Aluminum Purity": original[0] - predictions[0],
            "Casting Temperature":  original[1] - predictions[1],
            "Cooling Water Temperature": original[2] - predictions[2],
            "Casting Speed": original[3] - predictions[3],
            "Cast Bar Entry Temperature": original[4] - predictions[4],
            "Emulsion Temperature": original[5] - predictions[5],
            "Emulsion Pressure": original[6] - predictions[6],
            "Emulsion Concentration": original[7] - predictions[7],
            "Rod Quench Water Pressure": original[8] - predictions[8]
        }
        except Exception as e:
            app.logger.error(f"Error calculating differences: {str(e)}")
            return jsonify({"error": "Failed to calculate differences"}), 500

        # Render results
        return render_template('results.html', original_values=output_data, predictions=predictions, differences=differences)

    except Exception as e:
        app.logger.error(f"General error in final_prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
