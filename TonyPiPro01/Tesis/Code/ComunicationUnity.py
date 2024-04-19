import socket
import time
import hiwonder.Board as Board
import hiwonder.ActionGroupControl as AGC
import MovesActions as moves

AGC.runActionGroup('edit_t_pose')

ip_address = "0.0.0.0"
port = 5042

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip_address, port))
server_socket.listen(1)
print(f'Comunicacion preparada...')

servo_mapping = [
    {'id': 6, 'servo_min': 0, 'servo_max': 1000, 'angle_min': -135, 'angle_max': 135}, #Codo I
    {'id': 17, 'servo_min': 0, 'servo_max': 1000, 'angle_min': 150, 'angle_max': 270}, #Hombro I
    {'id': 8, 'servo_min': 1000, 'servo_max': 0, 'angle_min': -60, 'angle_max': 180}, # Hombro Rotacional I
    {'id': 14, 'servo_min': 0, 'servo_max': 1000, 'angle_min': -135, 'angle_max': 135}, #Codo D
    {'id': 15, 'servo_min': 0, 'servo_max': 1000, 'angle_min': -120, 'angle_max': 120}, #Hombro D
    {'id': 16, 'servo_min': 1000, 'servo_max': 0, 'angle_min': -180, 'angle_max': 60} #Hombro Rotacional D
]

conn, addr = server_socket.accept()
print(f'Conectado con Unity')
while True:
    data = conn.recv(1024)
    if data:
        received_data = data.decode('utf-8')
        print(f'Trama recivida de Unity : [{received_data}]')
        data_list = received_data.split(',')
        if len(data_list) == 1:
            if 'Up' in received_data:
                moves.UpBody()
                AGC.runActionGroup('go_forward_one_step')
            elif 'Down' in received_data:
                moves.UpBody()
                AGC.runActionGroup('back_one_step')
            elif 'Left' in received_data:
                moves.UpBody()
                AGC.runActionGroup('left_move_30')
            elif 'Right' in received_data:
                moves.UpBody()
                AGC.runActionGroup('right_move_30')
            elif 'Start' in received_data:
                moves.UpBody()
                AGC.runActionGroup('edit_t_pose')
            elif 'Back' in received_data:
                moves.UpBody()
                AGC.runActionGroup('edit_t_pose')
            elif 'RT' in received_data:
                moves.DownBody()
            elif 'RB' in received_data:
                moves.UpBody()
            elif 'X' in received_data:
                moves.UpBody()
                AGC.runActionGroup('turn_left')
            elif 'B' in received_data:
                moves.UpBody()
                AGC.runActionGroup('turn_right')
            #elif 'Y' in received_data:
                #moves.UpBody()
                #AGC.runActionGroup('back_one_step')
        else:
            data_list.pop()
            data_int = [int(float(elemento)) for elemento in data_list]
            for i in range(0, len(data_int), 2):
                id = data_int[i]
                angle = data_int[i + 1]
                for map in servo_mapping:
                    if map['id'] == id:
                        servo = (angle - map['angle_max']) / (map['angle_min'] - map['angle_max'])
                        servo = servo * (map['servo_min'] - map['servo_max'])
                        servo = servo + map['servo_max']
                        servo_int = int(servo)
                        print(f'ID: {id} -> Angulo: {angle} -> Servo: {servo_int}')
                        Board.setBusServoPulse(id, servo_int, 1000)
        time.sleep(0.5)
conn.close()