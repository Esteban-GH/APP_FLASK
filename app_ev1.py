from flask import Flask, jsonify, request
from uuid import uuid4
import time
import json

app = Flask(__name__)


reminders = []

def validar_content(content):
    if not isinstance(content, str):
        return "Content debe ser un string"
    content = content.strip()
    if not content:
        return "Content no puede estar vacio"
    if len(content) > 120:
        return "Content no puede tener mas de 120 caracteres"

def validar_important(important):
    if not isinstance(important, bool):
        return "Important debe ser un booleano"

@app.route('/api/reminders', methods=['GET'])
def lista_reminders():
    return jsonify(sorted(reminders, key=lambda x: (-x['important'], x['createdAt']))), 200

@app.route('/api/reminders', methods=['POST'])
def crear_reminder():
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    datos = request.get_json()
    
    if 'content' not in datos:
        return jsonify({"error": "Content es requerido"}), 400
    
    if error := validar_content(datos['content']):
        return jsonify({"error": error}), 400

    important = datos.get('important', False)
    if error := validar_important(important):
        return jsonify({"error": error}), 400

    reminder = {
        'id': str(uuid4()),
        'content': datos['content'].strip(),
        'createdAt': int(time.time() * 1000),
        'important': important
    }

    reminders.append(reminder)
    return jsonify(reminder), 201

@app.route('/api/reminders/<id>', methods=['PATCH'])
def actualizar_reminder(id):

    reminder = next((r for r in reminders if r['id'] == id), None)
    if not reminder:
        return jsonify({"error": "Recordatorio no encontrado"}), 404

    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    datos = request.get_json()
    
    if 'content' in datos:
        if error := validar_content(datos['content']):
            return jsonify({"error": error}), 400
        reminder['content'] = datos['content'].strip()

    if 'important' in datos:
        if error := validar_important(datos['important']):
            return jsonify({"error": error}), 400
        reminder['important'] = datos['important']

    return jsonify(reminder), 200

@app.route('/api/reminders/<id>', methods=['DELETE'])
def eliminar_reminder(id):
    
    reminder = next((r for r in reminders if r['id'] == id), None)
    if not reminder:
        return jsonify({"error": "Recordatorio no encontrado"}), 404

    reminders.remove(reminder)
    return '', 204

