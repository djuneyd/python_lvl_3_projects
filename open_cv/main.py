import cv2

# Загрузка изображений
background = cv2.imread('open_cv/images/scenery.png')  # Основное изображение
overlay = cv2.imread('open_cv/images/abstractionizm.png')        # Изображение, которое будет наложено

# Проверка успешной загрузки изображений
if background is None or overlay is None:
    print("Ошибка загрузки изображений.")
else:
    # Определение размера overlay
    h, w = overlay.shape[:2]

    # Определение позиции для наложения (верхний левый угол)
    x, y = 50, 50  # Позиция верхнего левого угла overlay на background

    # Проверка, что overlay помещается на background
    if x + w <= background.shape[1] and y + h <= background.shape[0]:
        # Наложение изображения
        background[y:y+h, x:x+w] = overlay

        # Сохранение и отображение результата
        cv2.imshow('Result', background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Overlay image не помещается на фон.")
