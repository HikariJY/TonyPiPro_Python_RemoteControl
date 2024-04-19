import socket
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print(f"Esperando una conexión en {SERVER_IP}:{SERVER_PORT}")
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida desde {client_address}")

x1_data = deque()
x2_data = deque()
y1_data = deque()
y2_data = deque()
z1_data = deque()
z2_data = deque()
time_data = deque()

try:
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        coordinates = [float(coord) for coord in data.split(',')]
        timestamp = datetime.now()
        x1_data.append(coordinates[0])
        x2_data.append(coordinates[3])
        y1_data.append(coordinates[1])
        y2_data.append(coordinates[4])
        z1_data.append(coordinates[2])
        z2_data.append(coordinates[5])
        time_data.append(timestamp)
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    client_socket.close()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    ax1.plot(time_data, x1_data, label='Persona', color='red')
    ax1.plot(time_data, x2_data, label='Robot', color='green', linestyle='dashed')
    ax2.set_xlabel('Tiempo')
    ax1.set_ylabel('Coordenadas X')
    ax1.legend()

    ax2.plot(time_data, y1_data, label='Persona', color='red')
    ax2.plot(time_data, y2_data, label='Robot', color='green', linestyle='dashed')
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('Coordenadas Y')
    ax2.legend()

    ax3.plot(time_data, z1_data, label='Persona', color='red')
    ax3.plot(time_data, z2_data, label='Robot', color='green', linestyle='dashed')
    ax3.set_xlabel('Tiempo')
    ax3.set_ylabel('Coordenadas Z')
    ax3.legend()

    plt.tight_layout()
    plt.show()