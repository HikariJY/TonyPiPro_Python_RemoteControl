import Colors

import customtkinter as ctk
import tkinter as tk
import numpy as np
import cv2
import math

file_name = 'Assets/CameraIDs.txt'
default_values = {
    'frame_size': [640, 480],
    'screen_theme': 'green', #green, blue, dark-blue
    'screen_format': 16/9,
    'screen_width': 1280,
    'general_arguments': [10, 10],
    'button_arguments': [100, 0, 8, ('Consolas', 15, 'bold')],
    'title_arguments': [8, ('Consolas', 34, 'bold')],
    'label_arguments': [8, ('Consolas', 12, 'bold')],
    'error_arguments': [8, ('Consolas', 24, 'bold')],
    'credits_arguments': [8, ('Consolas', 9, 'italic')],
    'combobox_arguments': [8, ('Consolas', 14, 'bold')],
}

def WriteIDs():
    array = []
    index = 0
    print('Actualizando dispositivos de cámara...')
    while True:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            array.append(index)
            cap.release()
            index += 1
        else:
            cap.release()
            break
    print(f'Se encontraron {index} cámaras.')
    text = ' '.join(str(ID) for ID in array)
    with open(file_name, 'w') as my_file:
        my_file.write(text)
def ReadIDs():
    with open(file_name) as my_file:
        return [line.rstrip().split(' ') for line in my_file.readlines()]
def WindowGeometry(app, width = default_values['screen_width'], format = default_values['screen_format']):
    return f'{int(width)}x{int(width / format)}+{int((app.winfo_screenwidth() - width) / 2)}+{int((app.winfo_screenheight() - width / format) / 2)}'
def ImageSize(image, factor):
    width = int(factor)
    height = int(image.size[1] * factor / image.size[0])
    return (width, height)
def GetDefaultImage(theme):
    image_paths = {
        'blue': 'Assets/ThemeImages/Image_Blue.png',
        'dark-blue': 'Assets/ThemeImages/Image_DarkBlue.png',
        'green': 'Assets/ThemeImages/Image_Green.png'
    }
    return cv2.imread(image_paths[theme])
def ThirdImage(appearance, size):
    color = Colors.light_appearance if appearance == 'Light' else Colors.dark_appearance
    return np.ones((int(size), 25, 3), np.uint8) * color
def FramesConcat():
    return cv2.hconcat([
        GetDefaultImage(default_values['screen_theme']),
        ThirdImage(ctk.get_appearance_mode(), default_values['frame_size'][1]),
        GetDefaultImage(default_values['screen_theme'])
    ])
def GetFrameRL(frame_R, frame_L):
    return cv2.hconcat([
        frame_L,
        ThirdImage(ctk.get_appearance_mode(), default_values['frame_size'][1]),
        frame_R
    ])
def Triangulate(centerR, centerL):
    camera_distance = 63
    focal_length = 12

    if centerR[0] != centerL[0] and centerR[1] != centerL[1]:
        X_m = centerR[0] - centerL[0]
        Y_m = centerR[1] - centerL[1]
        d = math.sqrt(X_m ** 2 + Y_m ** 2)
        print(f'Profundidad: {106.0}')
        return (camera_distance * d / focal_length) / 1.875
    else:
        return focal_length
def CreateButton(master, text, command):
    return ctk.CTkButton(
        master=master,
        width=default_values['button_arguments'][0],
        border_width=default_values['button_arguments'][1],
        corner_radius=default_values['button_arguments'][2],
        font=default_values['button_arguments'][3],
        text=text,
        command=command
    )
def CreateLabelImg(master, img, factor):
    return ctk.CTkLabel(
        master=master,
        textvariable=tk.StringVar(value=''),
        image=ctk.CTkImage(light_image=img, dark_image=img, size=ImageSize(img, factor))
    )
def CreateLabel(master, text, key):
    return ctk.CTkLabel(
        master=master,
        textvariable=tk.StringVar(value=text),
        corner_radius=default_values[key][0],
        font=default_values[key][1]
    )
def GridGadget(gadget, row, column, rowspan=1, columnspan=1, sticky=''):
    gadget.grid(
        row=row,
        column=column,
        rowspan=rowspan,
        columnspan=columnspan,
        padx=default_values['general_arguments'][0],
        pady=default_values['general_arguments'][1],
        sticky=sticky
    )