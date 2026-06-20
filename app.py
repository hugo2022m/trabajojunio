from flask import Flask, render_template
import socket

app = Flask(__name__)
HOST = "172.20.10.2"	## IP del servidor
PORT = 12345			## Puerto del servidor

def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)  
            s.connect((HOST, PORT))
            data = s.recv(1024).decode().strip()
            print("RECIBIDO:", data)
            
            ejeX, ejeY = data.split(',')
            ejeX = float(ejeX.replace('X:', ''))
            ejeY = float(ejeY.replace('Y:', ''))
            return ejeX, ejeY

    except Exception as e:
        print("ERROR:", e)
        return 0.0, 0.0

def calcular_posicion_matriz(valor, min_val=-90, max_val=90):
    """Mapea el ángulo del sensor a un índice de matriz 4x4 (0 a 3)"""
    if valor < min_val: valor = min_val
    if valor > max_val: valor = max_val
    rango = max_val - min_val
    proporcion = (valor - min_val) / rango
    return int(proporcion * 3)


@app.route('/')
def index():
    ejeX, ejeY = leer_sensor()  
    matriz_x = calcular_posicion_matriz(ejeX)
    matriz_y = calcular_posicion_matriz(ejeY)
    
    return render_template(
        'index.html',
        ejeX=ejeX,
        ejeY=ejeY,
        mx=matriz_x,
        my=matriz_y
    )

## Pestaña 2: Integración Vista Compañero 1 
@app.route('/vista2')
def vista2():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'vista2.html', 
        ejeX=ejeX, 
        ejeY=ejeY
    )

## Pestaña 3: Integración Vista Compañero 2 
@app.route('/vista3')
def vista3():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'vista3.html', 
        ejeX=ejeX, 
        ejeY=ejeY
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
