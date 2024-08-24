import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('путь_к_изображению')

# Проверка, что изображение успешно загружено
if image is None:
    print("Ошибка загрузки изображения.")
else:
    # Создание сепия фильтра
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    
    # Применение фильтра к изображению
    sepia_image = cv2.transform(image, sepia_filter)

    # Ограничение значений от 0 до 255
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
    
    # Сохранение и отображение изображения
    cv2.imwrite('output_sepia.jpg', sepia_image)
    cv2.imshow('Sepia Image', sepia_image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()