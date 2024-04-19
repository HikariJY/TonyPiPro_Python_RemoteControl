import time
import hiwonder.Board as Board
import socket

HOST = ''  # Escucha en todas las interfaces
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('Esperando conexion...')
    client_socket, client_addres = server_socket.accept()
    print(f'Conexion establecida desde: {client_addres}')
    while True:
        data = client_socket.recv(1024)
        received_data = data.decode()
        print(f'Datos recibidos: {received_data}')
        if received_data.strip() == 'close':
            break
        else:
            data_substrings = received_data.split(',')
            values = [int(numero) for numero in data_substrings if numero.strip()]
            print(f'Datos convertidos: {values}')
            for i in range(int(len(values)/2)):
                Board.setBusServoPulse(values[i*2], values[i*2+1], 500)  # ID Servo #Pulso Servo #Tiempo ms
                #time.sleep(0.5)
    print('Cerrando conexion...')
    client_socket.close()