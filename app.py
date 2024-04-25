from flask import Flask, request, jsonify
from ASICROSCRAPPER import *
app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_data():
    data = request.json  # Obtén los datos JSON enviados en la petición
    url = data.get('url')  # Obtén la URL del JSON

    if not url:
        return jsonify({'error': 'Se requiere una URL válida en el JSON.'}), 400

    # Crear una instancia de ProductoMercadoLibre y extraer datos de la URL
    async def scrape_async():
        producto = ProductoMercadoLibre(url)
        return await producto.extraer_datos()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(scrape_async())

    return jsonify({'message': 'Datos obtenidos con éxito!', 'data': result})


# Endpoint raíz que devuelve un mensaje de bienvenida
@app.route('/', methods=['GET'])
def welcome():
    return "Bienvenido al servidor de prueba!"

# Endpoint que acepta datos en formato JSON y devuelve una confirmación
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json  # Obtiene los datos JSON enviados en la petición
    # Aquí puedes procesar los datos según sea necesario
    return jsonify({'message': 'Datos recibidos con éxito!', 'yourData': data})

# Endpoint que devuelve el estado del servidor
@app.route('/status', methods=['GET'])
def server_status():
    return jsonify({'status': 'Activo'})

if __name__ == '__main__':
    app.run(port=6000,debug=True)  # Inicia el servidor en modo de depuración
