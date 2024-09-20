from flask import Flask, jsonify, request
import requests
import datetime

# Inicialización de la aplicación Flask
app = Flask(__name__)

# URL base de la API externa
base_url = "https://66eb02c955ad32cda47b5560.mockapi.io/IoTCarStatus"


# Ruta para obtener todos los registros (GET)
@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        # Realizamos una solicitud GET a la API externa
        response = requests.get(base_url)
        response.raise_for_status()  # Verifica que la respuesta sea exitosa
        cars = response.json()  # Parseamos la respuesta en formato JSON
        return jsonify(cars), 200  # Devolvemos la lista de autos
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ruta para obtener un solo registro por ID (GET)
@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    try:
        response = requests.get(f"{base_url}/{id}")
        response.raise_for_status()
        car = response.json()
        return jsonify(car), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ruta para crear un nuevo registro (POST)
@app.route('/cars', methods=['POST'])
def create_car():
    try:
        new_car = request.json  # Obtenemos el contenido del cuerpo de la solicitud en formato JSON

        # Validamos y creamos un objeto con los datos esperados
        car_data = {
            'status': new_car.get('status', 'Unknown'),
            'date': new_car.get('date', str(datetime.datetime.now().date())),  # Fecha actual si no se proporciona
            'ipClient': new_car.get('ipClient', '0.0.0.0'),  # Dirección IP por defecto
            'name': new_car.get('name', 'Anonymous')  # Nombre por defecto si no se proporciona
        }

        response = requests.post(base_url, json=car_data)
        response.raise_for_status()
        created_car = response.json()
        return jsonify(created_car), 201  # Devolvemos el auto creado con el código 201 (creado)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ruta para actualizar un registro existente por ID (PUT)
@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    try:
        updated_data = request.json  # Obtenemos los nuevos datos del auto

        # Validamos y actualizamos solo los campos proporcionados
        car_data = {
            'status': updated_data.get('status'),
            'date': updated_data.get('date', str(datetime.datetime.now().date())),
            'ipClient': updated_data.get('ipClient'),
            'name': updated_data.get('name')
        }

        response = requests.put(f"{base_url}/{id}", json=car_data)
        response.raise_for_status()
        updated_car = response.json()
        return jsonify(updated_car), 200  # Devolvemos el auto actualizado
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ruta para eliminar un registro por ID (DELETE)
@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    try:
        response = requests.delete(f"{base_url}/{id}")
        response.raise_for_status()
        return jsonify({'message': f'Car with ID {id} deleted successfully'}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True)