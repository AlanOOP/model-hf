from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar el modelo y el scaler
model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos del request
        data = request.get_json(force=True)
        print("Datos recibidos:", data)
        
        # Convertir los datos en un DataFrame
        df = pd.DataFrame([data])
        print("DataFrame creado:", df)
        
        # Preprocesamiento: Convertir a numéricos
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
        df['height'] = pd.to_numeric(df['height'], errors='coerce')
        
        # Verificación de datos
        print("DataFrame después del preprocesamiento:", df)
        
        # Seleccionar las características (debe coincidir con las características seleccionadas en el modelo)
        selected_columns = ['time', 'distance', 'weight', 'height']
        X = df[selected_columns]
        print("Características seleccionadas:", X)
        
        # Escalar las características
        X_scaled = scaler.transform(X)
        print("Características escaladas:", X_scaled)
        
        # Realizar la predicción
        prediction = model.predict(X_scaled)
        print("Predicción:", prediction)
        
        # Devolver la predicción
        return jsonify({"level": prediction[0]})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
