from flask import Flask, jsonify, request, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')

DATA_DIR = '../data'
os.makedirs(DATA_DIR, exist_ok=True)
ESTUDIANTES_FILE = os.path.join(DATA_DIR, 'estudiantes.json')
ASISTENCIAS_FILE = os.path.join(DATA_DIR, 'asistencias.json')

# Inicializa archivos JSON si no existen
if not os.path.exists(ESTUDIANTES_FILE):
    with open(ESTUDIANTES_FILE, 'w') as f:
        json.dump([], f)
if not os.path.exists(ASISTENCIAS_FILE):
    with open(ASISTENCIAS_FILE, 'w') as f:
        json.dump([], f)

# Ruta para servir páginas HTML
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/registro')
def registro():
    return send_from_directory('../frontend', 'registro.html')

@app.route('/asistencia')
def asistencia():
    return send_from_directory('../frontend', 'asistencia.html')

@app.route('/reportes')
def reportes():
    return send_from_directory('../frontend', 'reportes.html')

# API: Obtener estudiantes
@app.route('/api/estudiantes', methods=['GET'])
def get_estudiantes():
    with open(ESTUDIANTES_FILE, 'r') as f:
        return jsonify(json.load(f))

# API: Agregar estudiante
@app.route('/api/estudiantes', methods=['POST'])
def add_estudiante():
    data = request.json
    with open(ESTUDIANTES_FILE, 'r+') as f:
        estudiantes = json.load(f)
        nuevo_id = max([e['id'] for e in estudiantes] + [0]) + 1
        data['id'] = nuevo_id
        estudiantes.append(data)
        f.seek(0)
        json.dump(estudiantes, f, indent=4)
    return jsonify({'success': True, 'id': nuevo_id})

# API: Eliminar estudiante
@app.route('/api/estudiantes/<int:est_id>', methods=['DELETE'])
def delete_estudiante(est_id):
    with open(ESTUDIANTES_FILE, 'r+') as f:
        estudiantes = json.load(f)
        estudiantes = [e for e in estudiantes if e['id'] != est_id]
        f.seek(0)
        f.truncate()
        json.dump(estudiantes, f, indent=4)
    return jsonify({'success': True})

# API: Obtener asistencias
@app.route('/api/asistencias', methods=['GET'])
def get_asistencias():
    with open(ASISTENCIAS_FILE, 'r') as f:
        return jsonify(json.load(f))

# API: Agregar asistencia
@app.route('/api/asistencias', methods=['POST'])
def add_asistencia():
    data = request.json
    data['fecha'] = datetime.now().strftime('%Y-%m-%d')  # Fecha automática
    with open(ASISTENCIAS_FILE, 'r+') as f:
        asistencias = json.load(f)
        asistencias.append(data)
        f.seek(0)
        json.dump(asistencias, f, indent=4)
    return jsonify({'success': True})

# API: Invocar Java para estadísticas (por estudiante ID)
@app.route('/api/estadisticas/<int:est_id>', methods=['GET'])
def get_estadisticas(est_id):
    # Llama a Java via subprocess
    import subprocess
    result = subprocess.run(['java', '-cp', '../java', 'Estadisticas', str(est_id)], 
                            capture_output=True, text=True)
    if result.returncode == 0:
        return jsonify({'porcentaje': result.stdout.strip()})
    return jsonify({'error': 'Fallo en cálculo'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)