import cv2

file_name = 'assets/Camera_ID_List.txt'
white = '#ffffff'
black = '#000000'
green = '#2fa572'
orange = '#ff8c40'
blue = '#1f6aa5'
red = '#cc0000'
gray = '#808080'

def GetFileName():
    return file_name
def CameraList():
    global file_name
    array_ids = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            array_ids.append(index)
            cap.release()
            index += 1
        else:
            cap.release()
            break
    WriteDocument_ID(array_ids, file_name)
def WriteDocument_ID(stringLiteral, fileName):
    plain_text = ''
    for sub_string in stringLiteral: plain_text = plain_text + f'{sub_string} '
    my_file = open(fileName, 'w')
    my_file.write(plain_text)
    my_file.close()
def ReadDocument_ID(fileName):
    with open(fileName) as my_file:
        file_lines = my_file.readlines()
        file_lines = [file_line.rstrip() for file_line in file_lines]
        file_array = [file_line.split(' ') for file_line in file_lines]
        return file_array
def OpenFile_Movement(fileName):
    try:
        lines = []
        with open(fileName, 'r') as my_file:
            lines = [line.strip().split() for line in my_file.readlines() if len(line.strip()) > 0]
        if lines:
            return lines
        else:
            return []
    except FileNotFoundError:
        return []

def WriteFile_Movement(fileName):
    print('WriteFile')