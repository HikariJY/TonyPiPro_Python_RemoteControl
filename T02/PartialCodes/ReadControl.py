import cv2
import pygame

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No se encontraron controles inalámbricos.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick detectado:", joystick.get_name())

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Muestra el frame en una ventana de OpenCV
        cv2.imshow("Frame", frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.JOYAXISMOTION:
                print("Eje {} valor: {}".format(event.axis, joystick.get_axis(event.axis)))
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Botón {} presionado".format(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                print("Botón {} liberado".format(event.button))

        # Espera 1 milisegundo para que cv2.waitKey() funcione correctamente
        if cv2.waitKey(1) & 0xFF == ord('q'): break

if __name__ == "__main__":
    main()
