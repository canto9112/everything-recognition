import cv2

from config import CASCADES


def is_user_wants_quit():
    # При нажатии на клавишу 'q' произойдет выход из программы и скрипт оставновиться
    return cv2.waitKey(1) & 0xFF == ord('q')


def show_frame(frame):
    # Функция выводит рамку с названием 'Video'
    cv2.imshow('Video', frame)


def draw_sqare(frame, color):
    # функция рисует квадрат с указанным цветом
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def get_cascades():
    # Получаем обученные классификаторы из файла config.py
    cascades = [
        (cv2.CascadeClassifier(cascade['path']), cascade['color'])
        for title, cascade in CASCADES.items()
        if cascade['draw']
    ]
    return cascades


if __name__ == "__main__":
    cascades = get_cascades() # получаем только те каскады которые мы хотим чтоб были отрисованы (которые помечены как draw = True в файле config.py)

    video_capture = cv2.VideoCapture(0) # говорит о том что мы открываем веб-камеру для видеопотока
    while True:
        if not video_capture.isOpened(): # Если видеокамера недоступна то выведет Sorry
            print("Couldn't find your webcam... Sorry :c")
        _, webcam_frame = video_capture.read() # чтения видеофайлов или захвата данных в результате декодирования и
                                               # возврата только что захваченного кадра.

        gray_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2HSV)# Установка цветового пространства на серый
        for cascade, color in cascades:
            captures = [cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30)
            )]# Получаем картинку которую нам нужно распознать
            for capture in captures:
                for (x, y, w, h) in capture:
                    draw_sqare(webcam_frame, color)# отрисовываем квадрат на кадре видео потока
        show_frame(webcam_frame)# показываем видео с квадратами

        if is_user_wants_quit():# Если пользователь нажал q выходим из бесконечного цикла
            break
    video_capture.release()# прекращает захват видео с вебкамеры
    cv2.destroyAllWindows()# Выключает все окна с видео
