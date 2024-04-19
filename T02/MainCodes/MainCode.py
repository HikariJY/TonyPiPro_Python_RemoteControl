
###  Importación Interna

import Colors
import Functions

###      Importación Externa

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog #
import cv2
from PIL import Image
import time
from cvzone.PoseModule import PoseDetector
import os
from datetime import datetime
import socket
import threading

###      Constantes y Variables

window_flag = id_flag = try_flag = start_flag = record_flag = False
change_flag = 0

cap_right = cap_left = None
id_values = ['0', '0']
fps_list, prev_time = [], 0

confidence = 0.85
detector_right = PoseDetector(detectionCon=confidence, trackCon=confidence)
detector_left = PoseDetector(detectionCon=confidence, trackCon=confidence)
depp_list, depp = [], 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addres_port = ('127.0.0.1', 5052)
list_data, data_increment, prev_data = [], [15, 15, 60], []
folder_path = ''

###      Funciones

def Open_Window_Event():
    global window_flag
    if window_flag:
        app_window.geometry(help_window.geometry())
        app_window.deiconify()
        help_window.withdraw()
    else:
        help_window.geometry(app_window.geometry())
        help_window.deiconify()
        app_window.withdraw()
    window_flag = not window_flag
def Release_Capture():
    cap_right.release() if cap_right is not None else None
    cap_left.release() if cap_left is not None else None
def Close_Event():
    Release_Capture()
    help_window.destroy()
    app_window.destroy()
def Right_Value(choice):
    global id_values, id_flag
    id_flag = True
    id_values[0] = choice
def Left_Value(choice):
    global id_values, id_flag
    id_flag = True
    id_values[1] = choice
def Change_Event():
    global change_flag
    if start_flag: change_flag = (change_flag + 1) % 3
def Try_Event():
    global try_flag, id_flag, cap_right, cap_left
    if not try_flag:
        cap_right = cv2.VideoCapture(int(id_values[0]))
        if cap_right.isOpened():
            cap_left = cap_right
            if cap_left.isOpened():
                btn_try.configure(text='Probando', text_color=Colors.white, fg_color=Colors.red)
                btn_start.grid_forget()
                lbl_fps.configure(textvariable=tk.StringVar(value='FPS: 0'), text_color=Colors.green)
                lbl_error.configure(textvariable=tk.StringVar(value='NA'), text_color=Colors.gray)
                cmbbx_right.configure(state=tk.DISABLED)
                cmbbx_left.configure(state=tk.DISABLED)
                try_flag = True
                TryCapture()
            else:
                Release_Capture()
                lbl_error.configure(textvariable=tk.StringVar(value='Error: ID izquierdo no permite captura'),
                                    text_color=Colors.red)
                id_flag = False
        else:
            Release_Capture()
            lbl_error.configure(textvariable=tk.StringVar(value='Error: ID derecho no permite captura'),
                                text_color=Colors.red)
            id_flag = False
    else:
        btn_try.configure(text='Probar', text_color=Colors.white, fg_color=Colors.green)
        Grid_Button_Start()
        btn_start.configure(text='Comenzar', text_color=Colors.white, fg_color=Colors.green)
        lbl_fps.configure(text='FPS: ##', text_color=Colors.gray)
        Release_Capture()
        lbl_frames.configure(image=ctk.CTkImage(
            light_image=Image.fromarray(cv2.cvtColor(Functions.FramesConcat(), cv2.COLOR_BGR2RGB)),
            dark_image=Image.fromarray(cv2.cvtColor(Functions.FramesConcat(), cv2.COLOR_BGR2RGB)),
            size=(int(Functions.default_values['frame_size'][0] * 1.75), int(Functions.default_values['frame_size'][1] * 1.75 / 2))
        ))
        lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: Probar otra vez o Comenzar'), text_color=Colors.orange)
        cmbbx_right.configure(state=tk.NORMAL)
        cmbbx_left.configure(state=tk.NORMAL)
        try_flag = False
def Start_Event():
    global start_flag, id_flag, cap_right, cap_left
    if id_flag:
        if start_flag:
            Grid_Button_Try()
            btn_start.configure(text='Comenzar', text_color=Colors.white, fg_color=Colors.green)
            btn_change.grid_forget()
            btn_record.grid_forget()
            if record_flag: Record_Event()
            lbl_fps.configure(textvariable=tk.StringVar(value='FPS: ##'), text_color=Colors.gray)
            Release_Capture()
            lbl_frames.configure(image=ctk.CTkImage(
                light_image=Image.fromarray(cv2.cvtColor(Functions.FramesConcat(), cv2.COLOR_BGR2RGB)),
                dark_image=Image.fromarray(cv2.cvtColor(Functions.FramesConcat(), cv2.COLOR_BGR2RGB)),
                size=(int(Functions.default_values['frame_size'][0] * 1.75), int(Functions.default_values['frame_size'][1] * 1.75 / 2))
            ))
            lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: Probar o Comenzar otra vez'), text_color=Colors.orange)
            cmbbx_right.configure(state=tk.NORMAL)
            cmbbx_left.configure(state=tk.NORMAL)
            start_flag = False
        else:
            cap_right = cv2.VideoCapture(int(id_values[0]))
            if cap_right.isOpened():
                cap_left = cv2.VideoCapture(int(id_values[1]))
                if cap_left.isOpened():
                    btn_try.grid_forget()
                    btn_start.configure(text='Terminar', text_color=Colors.white, fg_color=Colors.red)
                    Grid_Button_Change()
                    Grid_Button_Record()
                    lbl_fps.configure(textvariable=tk.StringVar(value='FPS: 0'), text_color=Colors.green)
                    lbl_error.configure(textvariable=tk.StringVar(value='NA'), text_color=Colors.gray)
                    cmbbx_right.configure(state=tk.DISABLED)
                    cmbbx_left.configure(state=tk.DISABLED)
                    start_flag = True
                    TryCapture()
                else:
                    Release_Capture()
                    lbl_error.configure(textvariable=tk.StringVar(value='Error: ID izquierdo no permite captura'), text_color=Colors.red)
                    id_flag = False
                    btn_try.configure(text='Probar', text_color=Colors.black, fg_color=Colors.orange)
                    btn_start.grid_forget()
            else:
                Release_Capture()
                lbl_error.configure(textvariable=tk.StringVar(value='Error: ID derecho no permite captura'), text_color=Colors.red)
                id_flag = False
                btn_try.configure(text='Probar', text_color=Colors.black, fg_color=Colors.orange)
                btn_start.grid_forget()
def TryCapture():
    global id_flag, cap_right, cap_left, prev_time, fps_list, depp_list, depp , prev_data
    if try_flag or start_flag:
        ret_R, frame_R = cap_right.read()
        if ret_R:
            ret_L, frame_L = ret_R, frame_R
            if ret_L:
                id_flag = True
                if start_flag:
                    lmList_R, bboxInfo_R = detector_right.findPosition(
                        detector_right.findPose(
                            frame_R,
                            draw=False
                        ),
                        draw=False,
                        bboxWithHands=False
                    )
                    lmList_L, bboxInfo_L = detector_left.findPosition(
                        detector_left.findPose(
                            frame_L,
                            draw=False
                        ),
                        draw=False,
                        bboxWithHands=False
                    )
                    if change_flag == 0 or change_flag == 2:
                        frame_R = detector_right.findPose(frame_R, draw=True)
                        frame_L = detector_left.findPose(frame_L, draw=True)
                    if change_flag == 1 or change_flag == 2:
                        if bboxInfo_R:
                            bbox = bboxInfo_R['bbox']
                            cv2.rectangle(frame_R, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 2)
                            center = bboxInfo_R["center"]
                            cv2.circle(frame_R, center, 5, (0, 0, 255), cv2.FILLED)
                        if bboxInfo_L:
                            bbox = bboxInfo_L['bbox']
                            cv2.rectangle(frame_L, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 2)
                            center = bboxInfo_L["center"]
                            cv2.circle(frame_L, center, 5, (0, 0, 255), cv2.FILLED)
                    if bboxInfo_L and bboxInfo_R: #or bboxInfo_R:
                        lmList = lmList_L
                        depp_list.append(Functions.Triangulate(bboxInfo_R["center"], bboxInfo_L["center"]))
                        if len(depp_list) > 40:
                            depp_list.pop(0)
                        depp = sum(depp_list) / len(depp_list)
                        # CENTRO DEL CUERRPO
                        center = [0, 0, 0]
                        for i in (11, 12, 23, 24):
                            center[0] += lmList[i][1]
                            center[1] += lmList[i][2]
                            center[2] += lmList[i][3]
                        center = [x // 4 for x in center]
                        # PUNTOS
                        data = []
                        for lm in lmList:
                            if lm[0] in (11, 12, 23, 24, 13, 15, 14, 16):
                                data.extend([lm[0], lm[1] - center[0], - lm[2] + center[1], lm[3] - center[2]])
                        list_data.append(data)
                        if len(list_data) > 20:
                            list_data.pop(0)
                        filter_data = [0] * len(data)
                        for value in list_data:
                            filter_data = [x + y for x, y in zip(value, filter_data)]
                        filter_data = [x // len(list_data) for x in filter_data]
                        if len(prev_data) == 0:
                            prev_data = filter_data
                        else:
                            for i, value in enumerate(data):
                                if i % 4 == 1:
                                    if value >= prev_data[i] + data_increment[0] or value <= prev_data[i] - \
                                            data_increment[0]:
                                        prev_data[i] = value
                                elif i % 4 == 2:
                                    if value >= prev_data[i] + data_increment[1] or value <= prev_data[i] - \
                                            data_increment[1]:
                                        prev_data[i] = value
                                elif i % 4 == 3:
                                    if value >= prev_data[i] + data_increment[2] or value <= prev_data[i] - \
                                            data_increment[2]:
                                        prev_data[i] = value
                        if prev_data:
                            # GRABAR
                            if record_flag:
                                str_data = ', '.join(str(value) for value in prev_data)
                                with open(folder_path, 'r') as file:
                                    content = file.read()
                                if len(content.strip()) == 0:
                                    with open(folder_path, 'w') as file:
                                        file.write(str_data + '\n')
                                else:
                                    with open(folder_path, 'a') as file:
                                        file.write(str_data + '\n')
                                print(f'Guardando....')
                            else:
                                print(f'Filtrado: {prev_data}')
                                sock.sendto(str.encode(str(prev_data)), server_addres_port)
                                print(f'Enviando....')
                frame_R = cv2.resize(frame_R, Functions.default_values['frame_size'])
                frame_L = cv2.resize(frame_L, Functions.default_values['frame_size'])
                lbl_frames.configure(image=ctk.CTkImage(
                    light_image=Image.fromarray(cv2.cvtColor(Functions.GetFrameRL(frame_R, frame_L), cv2.COLOR_BGR2RGB)),
                    dark_image=Image.fromarray(cv2.cvtColor(Functions.GetFrameRL(frame_R, frame_L), cv2.COLOR_BGR2RGB)),
                    size=(int(Functions.default_values['frame_size'][0] * 1.75), int(Functions.default_values['frame_size'][1] * 1.75 / 2))
                ))
                # FPS
                fps = 1 / (time.time() - prev_time)
                prev_time = time.time()
                fps_list.append(fps)
                if len(fps_list) > 20: fps_list.pop(0)
                fps = sum(fps_list) / len(fps_list)
                lbl_fps.configure(textvariable=tk.StringVar(value=f'FPS: {int(fps)}'), text_color=Colors.green)
                lbl_frames.after(10, TryCapture)
            else:
                if try_flag: Try_Event()
                elif start_flag: Start_Event()
                lbl_error.configure(textvariable=tk.StringVar(value='Error: Cámara izquierda sin imagen'), text_color=Colors.red)
                id_flag = False
        else:
            if try_flag: Try_Event()
            elif start_flag: Start_Event()
            lbl_error.configure(textvariable=tk.StringVar(value='Error: Cámara derecha sin imagen'), text_color=Colors.red)
            id_flag = False
def Record_Event():
    global record_flag, folder_path
    if not record_flag:
        current_directory = os.getcwd() + '/Assets/PoseFiles'
        if not os.path.exists(current_directory): os.makedirs(current_directory)
        selected_directory = filedialog.askdirectory(initialdir=current_directory, title='Seleccionar carpeta')
        if selected_directory:
            current_datetime = datetime.now()
            default_file_name = current_datetime.strftime("PoseRecord_%Y_%m_%d_%H_%M_%S")
            folder_path = selected_directory + f'/{default_file_name}.txt'
            with open(folder_path, 'w') as file: pass
            btn_record.configure(text='Grabando', fg_color=Colors.red)
            record_flag = True
        else:
            btn_record.configure(text='Grabar', fg_color=Colors.green)
            record_flag = False
    else:
        btn_record.configure(text='Grabar', fg_color=Colors.green)
        record_flag = False
def Open_Event():
    if not record_flag:
        current_directory = os.getcwd() + '/Assets/PoseFiles'
        file_path = filedialog.askopenfilename(initialdir=current_directory, title="Seleccionar archivo")
        if file_path:
            enviar_hilo = threading.Thread(target=Open_Event2, args=(file_path,))
            enviar_hilo.start()
def Open_Event2(file_path):
    with open(file_path, 'r') as archivo:
        lineas_totales = sum(1 for _ in archivo)
        archivo.seek(0)
        i = 0
        for linea in archivo:
            i += 1
            linea = linea.strip()
            if linea:
                # EMNVIAR DATOS
                print(f'Grabado {i}/{lineas_totales}: {linea}')
                sock.sendto(str.encode(str(linea)), server_addres_port)
                print(f'Enviando....')
                #time.sleep(1)
        archivo.close()

####################################################################################################

if messagebox.askquestion('VENTANA DE MENSAJE', '¿Desea actualizar la lista de cámaras detectables?') == 'yes': Functions.WriteIDs()
ctk.set_appearance_mode('System')
ctk.set_default_color_theme(Functions.default_values['screen_theme'])
app_window = ctk.CTk()
help_window = ctk.CTkToplevel()
help_window.withdraw()

####################################################################################################

###     Configuración de la ventana principal

app_window.title('VENTANA PRINCIPAL')
app_window.geometry(Functions.WindowGeometry(app=app_window))
app_window.resizable(False, False)
app_window.protocol('WM_DELETE_WINDOW', Close_Event)
for row in range(9):
    weight = 1 if row in [1, 8] else 2 if row in [2, 7] else 3 if row in [3, 4, 5, 6] else 4
    app_window.grid_rowconfigure(row, weight=weight)
for col in range(9):
    weight = 1 if col in [0, 3, 4, 7] else 2 if col in [1, 5] else 3 if col == 8 else 4
    app_window.grid_columnconfigure(col, weight=weight)

##       Botones

def Grid_Button_Help(): Functions.GridGadget(gadget=btn_help, row=0, column=8)
btn_help = Functions.CreateButton(master=app_window, text='Ayuda', command=Open_Window_Event)
Grid_Button_Help()
def Grid_Button_Try(): Functions.GridGadget(gadget=btn_try, row=1, column=8, rowspan=2)
btn_try = Functions.CreateButton(master=app_window, text='Probar', command=Try_Event)
Grid_Button_Try()
btn_try.configure(fg_color=Colors.orange, text_color=Colors.black)
def Grid_Button_Start(): Functions.GridGadget(gadget=btn_start, row=3, column=8)
btn_start = Functions.CreateButton(master=app_window, text='Comenzar', command=Start_Event)
Grid_Button_Start()
def Grid_Button_Change(): Functions.GridGadget(gadget=btn_change, row=4, column=8)
btn_change = Functions.CreateButton(master=app_window, text='Cambiar', command=Change_Event)
def Grid_Button_Record(): Functions.GridGadget(gadget=btn_record, row=5, column=8)
btn_record = Functions.CreateButton(master=app_window, text='Grabar', command=Record_Event)
def Grid_Button_Open(): Functions.GridGadget(gadget=btn_open, row=6, column=8)
btn_open = Functions.CreateButton(master=app_window, text='Abrir', command=Open_Event)
Grid_Button_Open()
def Grid_Button_Close(): Functions.GridGadget(gadget=btn_close, row=7, column=8, rowspan=2)
btn_close = Functions.CreateButton(master=app_window, text='Cerrar', command=Close_Event)
Grid_Button_Close()

##      Labels

lbl_ESPEL_1 = Functions.CreateLabelImg(master=app_window, img=Image.open('Assets/ImageESPEL.png'), factor=100)
Functions.GridGadget(gadget=lbl_ESPEL_1, row=0, column=0)
lbl_logo_1 = Functions.CreateLabelImg(master=app_window, img=Image.open('Assets/ImageESPEL.png'), factor=100)
Functions.GridGadget(gadget=lbl_logo_1, row=0, column=7)
lbl_title_1 = Functions.CreateLabel(master=app_window, text='CONFIGURA LAS CÁMARAS Y VISUALIZA TU POSE',
                                    key='title_arguments')
Functions.GridGadget(gadget=lbl_title_1, row=0, column=1, columnspan=6, sticky='ew')
lbl_fps = Functions.CreateLabel(master=app_window, text='FPS: ##', key='label_arguments')
lbl_fps.configure(text_color=Colors.gray)
Functions.GridGadget(gadget=lbl_fps, row=1, column=1, columnspan=6, sticky='ew')
lbl_left = Functions.CreateLabel(master=app_window, text='ID izquierdo:', key='label_arguments')
Functions.GridGadget(gadget=lbl_left, row=2, column=1, sticky='e')
lbl_right = Functions.CreateLabel(master=app_window, text='ID derecho:', key='label_arguments')
Functions.GridGadget(gadget=lbl_right, row=2, column=5, sticky='e')
lbl_frames = Functions.CreateLabelImg(master=app_window,
                                      img=Image.fromarray(cv2.cvtColor(Functions.FramesConcat(), cv2.COLOR_BGR2RGB)),
                                      factor=Functions.default_values['frame_size'][0] * 1.75)
Functions.GridGadget(gadget=lbl_frames, row=3, column=0, rowspan=4, columnspan=8)
lbl_error = Functions.CreateLabel(master=app_window, text='Advertencia: Probar los dispositivos', key='error_arguments')
Functions.GridGadget(gadget=lbl_error, row=7, column=1, columnspan=6, sticky='ew')
lbl_error.configure(text_color=Colors.orange)
lbl_credits_1 = Functions.CreateLabel(master=app_window, text='Catagua Cobos Josseph Yaakob © 2023',
                                      key='credits_arguments')
Functions.GridGadget(gadget=lbl_credits_1, row=8, column=0, columnspan=4, sticky='w')
lbl_credits_1.configure(text_color=Colors.gray)

##      Combobox

cmbbx_left = ctk.CTkComboBox(master=app_window, values=Functions.ReadIDs()[0], corner_radius=Functions.default_values['combobox_arguments'][0], font=Functions.default_values['combobox_arguments'][1], command=Left_Value)
Functions.GridGadget(gadget=cmbbx_left, row=2, column=2, sticky='ew')
cmbbx_right = ctk.CTkComboBox(master=app_window, values=Functions.ReadIDs()[0], corner_radius=Functions.default_values['combobox_arguments'][0], font=Functions.default_values['combobox_arguments'][1], command=Right_Value)
Functions.GridGadget(gadget=cmbbx_right, row=2, column=6, sticky='ew')

####################################################################################################

###     Configuración de la ventana de ayuda

help_window.title('POSECAM: VENTANA DE AYUDA')
help_window.geometry(Functions.WindowGeometry(app=help_window))
help_window.resizable(False, False)
help_window.protocol('WM_DELETE_WINDOW', Close_Event)
help_window.grid_rowconfigure(2, weight=1)
help_window.grid_rowconfigure(0, weight=2)
help_window.grid_rowconfigure(1, weight=3)
help_window.grid_columnconfigure((0, 2), weight=1)
help_window.grid_columnconfigure(3, weight=2)
help_window.grid_columnconfigure(1, weight=3)

##      Botones

btn_return = Functions.CreateButton(master=help_window, text='Regresar', command=Open_Window_Event)
Functions.GridGadget(gadget=btn_return, row=0, column=3)
btn_close_2 = Functions.CreateButton(master=help_window, text='Cerrar', command=Close_Event)
Functions.GridGadget(gadget=btn_close_2, row=1, column=3, sticky='s')

##      Labels

lbl_ESPEL_2 = Functions.CreateLabelImg(master=help_window, img=Image.open('Assets/ImageESPEL.png'), factor=100)
Functions.GridGadget(gadget=lbl_ESPEL_2, row=0, column=0)
lbl_logo_2 = Functions.CreateLabelImg(master=help_window, img=Image.open('Assets/ImageESPEL.png'), factor=100)
Functions.GridGadget(gadget=lbl_logo_2, row=0, column=2)
lbl_title_2 = Functions.CreateLabel(master=help_window, text='\nAYUDA\n', key='title_arguments')
Functions.GridGadget(gadget=lbl_title_2, row=0, column=1, sticky='ew')
lbl_help = ctk.CTkLabel(master=help_window, textvariable=tk.StringVar(value=''), image=ctk.CTkImage(
        light_image=Image.open('Assets/HelpPP/Diapositiva2.PNG'),
        dark_image=Image.open('Assets/HelpPP/Diapositiva1.PNG'),
        size=(int(Functions.default_values['frame_size'][0] * 1.5), int(Functions.default_values['frame_size'][1] * 1.25))
    )
)
Functions.GridGadget(gadget=lbl_help, row=1, column=0, columnspan=3)
lbl_credits_2 = Functions.CreateLabel(master=help_window, text='Catagua Cobos Josseph Yaakob © 2023',
                                      key='credits_arguments')
Functions.GridGadget(gadget=lbl_credits_2, row=2, column=0, columnspan=2, sticky='w')
lbl_credits_2.configure(text_color=Colors.gray)

####################################################################################################

app_window.mainloop()