import cv2

# Захват видео из файла
cap = cv2.VideoCapture('open_cv/images/Rick Roll.mp4')

# Проверка, что видео успешно открыто
if not cap.isOpened():
    print("Ошибка открытия видеофайла.")
else:
    while True:
        # Чтение кадра из видео
        ret, frame = cap.read()
        
        # Проверка, что кадр был успешно прочитан
        if not ret:
            print("Завершение видео или ошибка чтения кадра.")
            break
        
        # Отображение кадра
        cv2.imshow('Video Frame', frame)
        
        # Ожидание 25 мс между кадрами и возможность завершения по нажатию клавиши 'q'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# Освобождение ресурсов после завершения работы с видео
cap.release()
cv2.destroyAllWindows()
