import customtkinter as ctk
import numpy as np
import cv2
import tkinter as tk
from PIL import Image
import mylibrary as ml
import tkinter.messagebox
import time
import mediapipe as mp
from tkinter import filedialog
import os

screen_format = 16 / 9
frame_size = [640, 480]
widget_font = 'Consolas'
btn_config = [100, 0, 8, ('Consolas', 15, 'bold'), 10, 10]
title_config = ('Consolas', 36, 'bold')
lbl_config = [btn_config[2], (title_config[0], 12, title_config[2]), btn_config[4], btn_config[5]]
capR, capL = None, None
id_value = ['0', '0']
id_flag, pose_flag = False, False
try_flag_color, try_flag, start_flag, record_flag = False, False, False, False
change_flag = 0
fps_list = []
prev_time = 0
deep_list = []
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
detection_confidence = 0.5
detectorR = mp_pose.Pose(
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=detection_confidence,
    static_image_mode=False
)
detectorL = mp_pose.Pose(
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=detection_confidence,
    static_image_mode=False
)
depp = 0
coords_R = []
coords_L = []


def ImageBetweenFrames():
    if ctk.get_appearance_mode() == 'Dark':
        return np.ones((int(frame_size[1]), 25, 3), np.uint8) * 36
    else:
        return np.ones((int(frame_size[1]), 25, 3), np.uint8) * 235
def FrameConcat():
    return cv2.hconcat([
        cv2.imread('assets/Image_Green.png'),
        ImageBetweenFrames(),
        cv2.imread('assets/Image_Green.png')
    ])
def WindowGeometry(horizontalSize):
    text = f'{int(horizontalSize)}x{int(horizontalSize / screen_format)}'
    text = text + f'+{int((app_window.winfo_screenwidth() - horizontalSize) / 2)}'
    text = text + f'+{int((app_window.winfo_screenheight() - horizontalSize / screen_format) / 2)}'
    return text
def GetPoseBoundingBox(pose_landmarks, img_shape):
    x_min, y_min = float('inf'), float('inf')
    x_max, y_max = float('-inf'), float('-inf')
    if pose_landmarks:
        for landmark in pose_landmarks.landmark:
            x, y = landmark.x, landmark.y
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
        w, h = img_shape
        x_min, y_min = int(x_min * w), int(y_min * h)
        x_max, y_max = int(x_max * w), int(y_max * h)
        x_center = (x_min + x_max) // 2
        y_center = (y_min + y_max) // 2
        return (x_min, y_min), (x_max, y_max), (x_center, y_center)
    else: return None
def Triangulate(centerR, centerL):
    x_R = centerR[0]
    x_L = centerL[0]
    camera_distance = 50
    focal_length = 35
    if not (x_R == x_L):
        return focal_length*camera_distance/abs(x_R-x_L)
def DisableEvent(): pass
def HelpEvent():
    app_window.withdraw()
    help_window.deiconify()
def ReturnEvent():
    help_window.withdraw()
    app_window.deiconify()
def CloseEvent():
    global capR, capL
    if capR is not None: capR.release()
    if capL is not None: capL.release()
    help_window.destroy()
    app_window.destroy()
def RightValue(choice):
    global id_value, id_flag
    id_flag = False
    id_value[0] = choice
def LeftValue(choice):
    global id_value, id_flag
    id_flag = False
    id_value[1] = choice
def TryEvent():
    global try_flag, pose_flag, try_flag_color, capR, capL, id_flag
    if try_flag:
        try_flag = False
        btn_try.configure(text='Probar', text_color=ml.white, fg_color=ml.green)
        btn_start_grid()
        btn_start.configure(text='Comenzar', text_color=ml.white, fg_color=ml.green)
        lbl_fps.configure(text='FPS: ##', text_color=ml.gray)
        if capR is not None: capR.release()
        if capL is not None: capL.release()
        lbl_frames.configure(image=ctk.CTkImage(
            light_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
            dark_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
            size=(int(frame_size[0]*1.75), int(frame_size[1]*1.75/2))
        ))
        if id_flag: lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: Probar otra vez o Comenzar'), text_color=ml.orange)
        cmbbx_right.configure(state=tk.NORMAL)
        cmbbx_left.configure(state=tk.NORMAL)
    else:
        if id_value[0] == id_value[1]:
            lbl_error.configure(textvariable=tk.StringVar(value='Error: IDs escogidas deben ser diferentes'), text_color=ml.red)
            id_flag = False
        else:
            capR = cv2.VideoCapture(int(id_value[0]))
            if capR.isOpened():
                capL = cv2.VideoCapture(int(id_value[1]))
                if capL.isOpened():
                    try_flag_color = True
                    try_flag = True
                    btn_try.configure(text='Probando', text_color=ml.white, fg_color=ml.red)
                    btn_start.grid_forget()
                    lbl_fps.configure(textvariable=tk.StringVar(value='FPS: 0'), text_color=ml.green)
                    lbl_error.configure(textvariable=tk.StringVar(value='NA'), text_color=ml.gray)
                    pose_flag = False
                    cmbbx_right.configure(state=tk.DISABLED)
                    cmbbx_left.configure(state=tk.DISABLED)
                    Capture()
                else:
                    if capR is not None: capR.release()
                    if capL is not None: capL.release()
                    lbl_error.configure(textvariable=tk.StringVar(value='Error: ID izquierdo no permite captura'), text_color=ml.red)
                    id_flag = False
            else:
                if capR is not None: capR.release()
                if capL is not None: capL.release()
                lbl_error.configure(textvariable=tk.StringVar(value='Error: ID derecho no permite captura'), text_color=ml.red)
                id_flag = False
def StartEvent():
    global start_flag, id_flag, capR, capL, pose_flag
    if id_flag:
        if start_flag:
            start_flag = False
            btn_try_grid()
            btn_start.configure(text='Comenzar', text_color=ml.white, fg_color=ml.green)
            btn_change.grid_forget()
            btn_record.grid_forget()
            if record_flag: RecordEvent()
            lbl_fps.configure(textvariable=tk.StringVar(value='FPS: ##'), text_color=ml.gray)
            if capR is not None: capR.release()
            if capL is not None: capL.release()
            lbl_frames.configure(image=ctk.CTkImage(
                light_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                dark_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
            ))
            lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: Probar o Comenzar otra vez'), text_color=ml.orange)
        else:
            start_flag = True
            capR = cv2.VideoCapture(int(id_value[0]))
            if capR.isOpened():
                capL = cv2.VideoCapture(int(id_value[1]))
                if capL.isOpened():
                    btn_try.grid_forget()
                    btn_start.configure(text='Terminar', text_color=ml.white, fg_color=ml.red)
                    btn_change_grid()
                    btn_open_grid()
                    btn_record_grid()
                    lbl_fps.configure(textvariable=tk.StringVar(value='FPS: 0'), text_color=ml.green)
                    lbl_error.configure(textvariable=tk.StringVar(value='NA'), text_color=ml.gray)
                    pose_flag = True
                    cmbbx_right.configure(state=tk.DISABLED)
                    cmbbx_left.configure(state=tk.DISABLED)
                    Capture()
                else:
                    if capR is not None: capR.release()
                    if capL is not None: capL.release()
                    lbl_error.configure(textvariable=tk.StringVar(value='Error: ID izquierdo no permite captura'), text_color=ml.red)
                    id_flag = False
                    btn_try.configure(text='Probar', text_color=ml.black, fg_color=ml.orange)
                    btn_start.grid_forget()
                    start_flag = False
            else:
                if capR is not None: capR.release()
                if capL is not None: capL.release()
                lbl_error.configure(textvariable=tk.StringVar(value='Error: ID derecho no permite captura'), text_color=ml.red)
                id_flag = False
                btn_try.configure(text='Probar', text_color=ml.black, fg_color=ml.orange)
                btn_start.grid_forget()
                start_flag = False
    else:
        start_flag = False
        btn_try.configure(text='Probar', text_color=ml.black, fg_color=ml.orange)
        btn_start.grid_forget()
        lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: Probar el nuevo ID'), text_color=ml.orange)
def Capture():
    global try_flag, start_flag, try_flag_color, capR, capL, id_flag, prev_time, fps_list, deep_list, deep, coords_R, coords_L
    bbx_R = None
    bbx_L = None
    if try_flag or start_flag:
        ret_R, frame_R = capR.read()
        if ret_R:
            ret_L, frame_L = capL.read()
            if ret_L:
                id_flag = True
                lbl_fps.configure(textvariable=tk.StringVar(value='FPS: 0'), text_color=ml.gray)
                frame_R = cv2.resize(frame_R, frame_size, interpolation=cv2.INTER_LINEAR)
                frame_L = cv2.resize(frame_L, frame_size, interpolation=cv2.INTER_LINEAR)
                if pose_flag:
                    results_R = detectorR.process(cv2.cvtColor(frame_R, cv2.COLOR_BGR2RGB))
                    results_L = detectorL.process(cv2.cvtColor(frame_L, cv2.COLOR_BGR2RGB))
                    bbx_R = GetPoseBoundingBox(results_R.pose_landmarks, frame_size)
                    bbx_L = GetPoseBoundingBox(results_L.pose_landmarks, frame_size)
                    if record_flag:
                        #### COdigo para guardar
                        print('agh')
                    if bbx_R is not None and bbx_L is not None:
                        deep_list.append(Triangulate(bbx_R[2], bbx_L[2]))
                        if len(deep_list) > 20: deep_list.pop(0)
                        deep = sum(deep_list)/len(deep_list)
                    if not results_R.pose_landmarks or not results_L.pose_landmarks:
                        lbl_error.configure(textvariable=tk.StringVar(value='Advertencia: La persona no está en el campo de análisis'), text_color=ml.orange)
                    else: lbl_error.configure(textvariable=tk.StringVar(value='NA'), text_color=ml.gray)
                    if change_flag == 0:
                        if results_R.pose_landmarks: mp_drawing.draw_landmarks(frame_R, results_R.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        if results_L.pose_landmarks: mp_drawing.draw_landmarks(frame_L, results_L.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        frame_RL = cv2.hconcat([frame_R, ImageBetweenFrames(), frame_L])
                        lbl_frames.configure(image=ctk.CTkImage(
                            light_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            dark_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
                        ))
                    elif change_flag == 1:
                        frame_R = cv2.cvtColor(cv2.threshold(cv2.cvtColor(frame_R, cv2.COLOR_BGR2GRAY), 0, 0, cv2.THRESH_BINARY)[1], cv2.COLOR_GRAY2BGR)
                        frame_L = cv2.cvtColor(cv2.threshold(cv2.cvtColor(frame_L, cv2.COLOR_BGR2GRAY), 0, 0, cv2.THRESH_BINARY)[1],cv2.COLOR_GRAY2BGR)
                        if results_R.pose_landmarks: mp_drawing.draw_landmarks(frame_R, results_R.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        if results_L.pose_landmarks: mp_drawing.draw_landmarks(frame_L, results_L.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        frame_RL = cv2.hconcat([frame_R, ImageBetweenFrames(), frame_L])
                        lbl_frames.configure(image=ctk.CTkImage(
                            light_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            dark_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
                        ))
                    elif change_flag == 2:
                        if results_R.pose_landmarks:
                            cv2.rectangle(frame_R, bbx_R[0], bbx_R[1], (0, 255, 0), 2)
                            cv2.circle(frame_R, bbx_R[2], 5, (0, 0, 255), -1)
                        if results_L.pose_landmarks:
                            cv2.rectangle(frame_L, bbx_L[0], bbx_L[1], (0, 255, 0), 2)
                            cv2.circle(frame_L, bbx_L[2], 5, (0, 0, 255), -1)
                        frame_RL = cv2.hconcat([frame_R, ImageBetweenFrames(), frame_L])
                        lbl_frames.configure(image=ctk.CTkImage(
                            light_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            dark_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                            size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
                        ))
                else:
                    frame_RL = cv2.hconcat([frame_R, ImageBetweenFrames(), frame_L])
                    lbl_frames.configure(image=ctk.CTkImage(
                        light_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                        dark_image=Image.fromarray(cv2.cvtColor(frame_RL, cv2.COLOR_BGR2RGB)),
                        size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
                    ))
                fps = 1 / (time.time() - prev_time)
                prev_time = time.time()
                fps_list.append(fps)
                if len(fps_list) > 20: fps_list.pop(0)
                fps = sum(fps_list) / len(fps_list)
                lbl_fps.configure(textvariable=tk.StringVar(value=f'FPS: {int(fps)}'), text_color=ml.green)
                lbl_frames.after(10, Capture)
            else:
                try_flag = False
                start_flag = False
                if pose_flag: try_flag_color = False
                btn_try.configure(text='Probar', text_color=ml.white, fg_color=ml.orange)
                btn_start.grid_forget()
                lbl_fps.configure(textvariable=tk.StringVar(value='FPS: ##'), text_color=ml.gray)
                if capR is not None: capR.release()
                if capL is not None: capL.release()
                lbl_frames.configure(image=ctk.CTkImage(
                    light_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                    dark_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                    size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
                ))
                lbl_error.configure(textvariable=tk.StringVar(value='Error: Cámara izquierda sin imagen'), text_color=ml.red)
                id_flag = False
                cmbbx_right.configure(state=tk.NORMAL)
                cmbbx_left.configure(state=tk.NORMAL)
        else:
            try_flag = False
            start_flag = False
            if pose_flag: try_flag_color = False
            btn_try.configure(text='Probar', text_color=ml.white, fg_color=ml.orange)
            btn_start.grid_forget()
            lbl_fps.configure(textvariable=tk.StringVar(value='FPS: ##'), text_color=ml.gray)
            if capR is not None: capR.release()
            if capL is not None: capL.release()
            lbl_frames.configure(image=ctk.CTkImage(
                light_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                dark_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
                size=(int(frame_size[0] * 1.75), int(frame_size[1] * 1.75 / 2))
            ))
            lbl_error.configure(textvariable=tk.StringVar(value='Error: Cámara derecha sin imagen'), text_color=ml.red)
            id_flag = False
            cmbbx_right.configure(state=tk.NORMAL)
            cmbbx_left.configure(state=tk.NORMAL)
def ChangeEvent():
    global change_flag
    if start_flag:
        match change_flag:
            case 0:
                change_flag = 1
            case 1:
                change_flag = 2
            case 2:
                change_flag = 0
def OpenEvent():
    local_path = str(os.path.abspath('')).replace('\\', '/')
    result = ml.OpenFile_Movement(str(filedialog.askopenfilename(initialdir=f'{local_path}/assets/Files_Records')))
    print(result)
def RecordEvent():
    global record_flag
    if record_flag:
        record_flag = False
        if start_flag: btn_start.configure(text_color=ml.white, fg_color=ml.red)
        btn_record.configure(text='Grabar', text_color=ml.white, fg_color=ml.green)
        btn_open_grid()
    else:
        record_flag = True
        btn_start.configure(text_color=ml.black, fg_color=ml.orange)
        btn_record.configure(text='Grabando', text_color=ml.white, fg_color=ml.red)
        btn_open.grid_forget()

res = tkinter.messagebox.askquestion('ID CÁMARAS', '¿Desea actualizar la lista de cámaras detectables?')
if res == 'yes': ml.CameraList()
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('green')
app_window = ctk.CTk()
help_window = ctk.CTkToplevel()
help_window.withdraw()

####################################################################################################

app_window.title('POSECAM: VENTANA PRINCIPAL')
app_window.geometry(WindowGeometry(frame_size[0]*2))
app_window.resizable(False, False)
app_window.protocol('WM_DELETE_WINDOW', DisableEvent)
app_window.grid_rowconfigure((1, 2, 3, 4, 5, 6, 8), weight=1)
app_window.grid_rowconfigure(7, weight=2)
app_window.grid_rowconfigure(0, weight=3)
app_window.grid_columnconfigure((0, 1, 3, 4, 5, 7, 8), weight=1)
app_window.grid_columnconfigure((2, 6, 9), weight=2)

btn_help = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Ayuda',
    command=HelpEvent
)
btn_help.grid(row=0, column=9, padx=btn_config[4], pady=btn_config[5])
def btn_try_grid(): btn_try.grid(row=2, column=9, padx=btn_config[4], pady=btn_config[5])
btn_try = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Probar',
    command=TryEvent,
    fg_color=ml.orange,
    text_color=ml.black
)
btn_try_grid()
def btn_start_grid(): btn_start.grid(row=3, column=9, padx=btn_config[4], pady=btn_config[5])
btn_start = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Comenzar',
    command=StartEvent
)
btn_start_grid()
btn_start.grid_forget()
def btn_change_grid(): btn_change.grid(row=4, column=9, padx=btn_config[4], pady=btn_config[5])
btn_change = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Cambiar',
    command=ChangeEvent
)
btn_change_grid()
btn_change.grid_forget()
def btn_open_grid(): btn_open.grid(row=5, column=9, padx=btn_config[4], pady=btn_config[5])
btn_open = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Abrir',
    command=OpenEvent
)
btn_open_grid()
def btn_record_grid(): btn_record.grid(row=6, column=9, padx=btn_config[4], pady=btn_config[5])
btn_record = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Grabar',
    command=RecordEvent
)
btn_record_grid()
btn_record.grid_forget()
btn_close = ctk.CTkButton(
    master=app_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Cerrar',
    command=CloseEvent
)
btn_close.grid(row=7, column=9, rowspan=2, padx=btn_config[4], pady=btn_config[5])
lbl_ESPEL = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.open('assets/Image_ESPEL.png'),
        dark_image=Image.open('assets/Image_ESPEL.png'),
        size=(int(100), int(Image.open('assets/Image_ESPEL.png').size[1]*100/Image.open('assets/Image_ESPEL.png').size[0]))
    )
)
lbl_ESPEL.grid(row=0, column=0, rowspan=2, columnspan=2, padx=lbl_config[2], pady=lbl_config[3])
lbl_title = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='CONFIGURA LAS CÁMARAS Y\nVISUALIZA TU POSE'),
    corner_radius=lbl_config[0],
    font=title_config
)
lbl_title.grid(row=0, column=2, columnspan=5, padx=lbl_config[2], pady=lbl_config[3], sticky="ew")
lbl_logo = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.open('assets/Image_ESPEL.png'),
        dark_image=Image.open('assets/Image_ESPEL.png'),
        size=(int(100), int(Image.open('assets/Image_ESPEL.png').size[1]*100/Image.open('assets/Image_ESPEL.png').size[0]))
    )
)
lbl_logo.grid(row=0, column=7, rowspan=2, columnspan=2, padx=lbl_config[2], pady=lbl_config[3])
def lbl_fps_grid(): lbl_fps.grid(row=1, column=4, padx=lbl_config[2], pady=lbl_config[3], sticky="ew")
lbl_fps = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='FPS: ##'),
    text_color=(ml.gray, ml.gray),
    corner_radius=lbl_config[0],
    font=lbl_config[1]
)
lbl_fps_grid()
lbl_right = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='ID derecho: '),
    corner_radius=lbl_config[0],
    font=lbl_config[1]
)
lbl_right.grid(row=2, column=0, padx=lbl_config[2], pady=lbl_config[3])
lbl_left = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='ID izquierdo: '),
    corner_radius=lbl_config[0],
    font=lbl_config[1]
)
lbl_left.grid(row=2, column=5, padx=lbl_config[2], pady=lbl_config[3])
def lbl_frames_grid(): lbl_frames.grid(row=3, column=0, rowspan=4, columnspan=9, padx=lbl_config[2], pady=lbl_config[3])
lbl_frames = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
        dark_image=Image.fromarray(cv2.cvtColor(FrameConcat(), cv2.COLOR_BGR2RGB)),
        size=(int(frame_size[0]*1.75), int(frame_size[1]*1.75/2))
    )
)
lbl_frames_grid()
def lbl_error_grid(): lbl_error.grid(row=7, column=0, columnspan=9, padx=lbl_config[2]+10, pady=lbl_config[3])
lbl_error = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='Advertencia: Probar los dispositivos'),
    text_color=(ml.orange, ml.orange),
    corner_radius=lbl_config[0],
    font=(title_config[0], 24, title_config[2]),
)
lbl_error_grid()
lbl_credits = ctk.CTkLabel(
    master=app_window,
    textvariable=tk.StringVar(value='Catagua Cobos Josseph Yaakob © 2023'),
    corner_radius=lbl_config[0],
    font=(title_config[0], 9, 'italic'),
    text_color=(ml.gray, ml.gray)
)
lbl_credits.grid(row=8, column=0,columnspan=2, padx=lbl_config[2], pady=lbl_config[3], sticky="ew")
def cmbbx_right_grid(): cmbbx_right.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
cmbbx_right = ctk.CTkComboBox(
    master=app_window,
    values=ml.ReadDocument_ID(ml.GetFileName())[0],
    corner_radius=lbl_config[0],
    font=(title_config[0], 14, title_config[2]),
    command=RightValue
)
cmbbx_right_grid()
def cmbbx_left_grid(): cmbbx_left.grid(row=2, column=6, columnspan=2, padx=10, pady=10, sticky="ew")
cmbbx_left = ctk.CTkComboBox(
    master=app_window,
    values=ml.ReadDocument_ID(ml.GetFileName())[0],
    corner_radius=lbl_config[0],
    font=(title_config[0], 14, title_config[2]),
    command=LeftValue
)
cmbbx_left_grid()

####################################################################################################

help_window.title('POSECAM: VENTANA DE AYUDA')
help_window.geometry(WindowGeometry(frame_size[0]*2))
help_window.resizable(False, False)
help_window.protocol('WM_DELETE_WINDOW', DisableEvent)
help_window.grid_rowconfigure((0, 1, 3, 4), weight=1)
help_window.grid_rowconfigure(2, weight=2)
help_window.grid_columnconfigure((1, 3, 4), weight=1)
help_window.grid_columnconfigure(0, weight=2)
help_window.grid_columnconfigure(2, weight=3)

btn_return = ctk.CTkButton(
    master=help_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Regresar',
    command=ReturnEvent
)
btn_return.grid(row=0, column=4, padx=btn_config[4], pady=btn_config[5])
btn_close = ctk.CTkButton(
    master=help_window,
    width=btn_config[0],
    border_width=btn_config[1],
    corner_radius=btn_config[2],
    font=btn_config[3],
    text='Cerrar',
    command=CloseEvent
)
btn_close.grid(row=3, column=4, rowspan=2, padx=btn_config[4], pady=btn_config[5])
lbl_ESPEL = ctk.CTkLabel(
    master=help_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.open('assets/Image_ESPEL.png'),
        dark_image=Image.open('assets/Image_ESPEL.png'),
        size=(int(100), int(Image.open('assets/Image_ESPEL.png').size[1]*100/Image.open('assets/Image_ESPEL.png').size[0]))
    )
)
lbl_ESPEL.grid(row=0, column=0, padx=lbl_config[2], pady=lbl_config[3])
lbl_title = ctk.CTkLabel(
    master=help_window,
    textvariable=tk.StringVar(value='\nAYUDA\n'),
    corner_radius=lbl_config[0],
    font=title_config
)
lbl_title.grid(row=0, column=1, columnspan=2, padx=lbl_config[2], pady=lbl_config[3], sticky="ew")
lbl_logo = ctk.CTkLabel(
    master=help_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.open('assets/Image_ESPEL.png'),
        dark_image=Image.open('assets/Image_ESPEL.png'),
        size=(int(100), int(Image.open('assets/Image_ESPEL.png').size[1]*100/Image.open('assets/Image_ESPEL.png').size[0]))
    )
)
lbl_logo.grid(row=0, column=3, padx=lbl_config[2], pady=lbl_config[3])
lbl_help = ctk.CTkLabel(
    master=help_window,
    textvariable=tk.StringVar(value=''),
    image=ctk.CTkImage(
        light_image=Image.open('assets/Help_PP/Diapositiva1.PNG'),
        dark_image=Image.open('assets/Help_PP/Diapositiva1.PNG'),
        size=(int(frame_size[0]*1.25), int(frame_size[1]*1.25))
    )
)
lbl_help.grid(row=1, column=0, rowspan=3, columnspan=4, padx=lbl_config[2], pady=lbl_config[3])
lbl_credits = ctk.CTkLabel(
    master=help_window,
    textvariable=tk.StringVar(value='Catagua Cobos Josseph Yaakob © 2023'),
    corner_radius=lbl_config[0],
    font=(title_config[0], 9, 'italic'),
    text_color=('gray', 'gray')
)
lbl_credits.grid(row=4, column=0,columnspan=2, padx=lbl_config[2], pady=lbl_config[3], sticky="ew")

####################################################################################################

app_window.mainloop()
