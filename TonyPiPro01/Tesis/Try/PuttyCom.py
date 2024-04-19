import socket

listening_ip = "0.0.0.0"  # Escuchar en todas las interfaces de red
listening_port = 12345  # Cambia esto al puerto que estás usando en Unity

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((listening_ip, listening_port))

while True:
    data, addr = sock.recvfrom(1024)
    received_message = data.decode('utf-8')

    response_message = "Se recibió! "+received_message
    response_data = response_message.encode('utf-8')
    sock.sendto(response_data, addr)

