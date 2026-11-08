import cv2  # Імпорт бібліотеки OpenCV для обробки зображень та відео
from logic.workWithHand.GestureWriter import GestureWriter  # Імпорт класу для розпізнавання тексту нейромережею
from logic.workWithHand.HandTracker import HandTracker  # Імпорт класу для відстеження положення рук
from logic.canva.DrawingCanvas import DrawingCanvas  # Імпорт класу для малювання на полотні
from data.config import train_data_folder  # Імпорт шляхів до файлів конфігурації

class AirWritingApp:
    """Головний клас логіки програми"""
    def __init__(self):
        """Ініціалізація"""
        self.cap = cv2.VideoCapture(0)  # Відкриття відеопотоку з камери за замовчуванням
        self.tracker = HandTracker()  # Ініціалізація трекера рук
        self.canvas = None  # Змінна для полотна, на якому буде малюватися
        self.writer = GestureWriter(train_data_folder)  # Ініціалізація розпізнавача жестів
        self.is_write = True  # Прапор для включення/виключення режиму малювання

    def set_is_write(self, value: bool):
        """Встановлює прапор малювання."""
        self.is_write = value

    def generate_frames(self):
        """
        Генерує кадри для відеопотоку з обробленим зображенням.

        Повертає:
        - Генератор: кожен кадр у вигляді JPEG зображення.
        """
        while True:
            ret, frame = self.cap.read()  # Читання кадру з відеопотоку
            if not ret:  # Якщо кадр не отримано, виходимо
                break
            frame = cv2.flip(frame, 1)  # Дзеркальне відображення зображення по горизонталі
            h, w, _ = frame.shape  # Отримуємо розміри кадру
            if self.canvas is None:  # Якщо полотно ще не створено, створюємо його
                self.canvas = DrawingCanvas(400, 400)

            if (not self.tracker.fist_detect(frame)) and self.is_write:  # Якщо кулак не виявлений і малювання увімкнене
                finger_pos = self.tracker.get_finger_position(frame)  # Отримуємо координати вказівного пальця
                if finger_pos:  # Якщо координати пальця знайдені
                    x, y = finger_pos  # Витягуємо координати
                    self.canvas.draw_line(x, y)  # Малюємо лінію на полотні по координатах
            else:
                self.canvas.clear_prev()  # Якщо кулак виявлений, очищуємо попередні координати
            canvas_img = self.canvas.get_canvas()  # Отримуємо зображення полотна
            # Перевіряємо кількість каналів (уникаємо помилки OpenCV)
            if len(canvas_img.shape) == 2:  # Якщо зображення полотна в градаціях сірого (1 канал)
                canvas_bgr = cv2.cvtColor(canvas_img, cv2.COLOR_GRAY2BGR)  # Перетворюємо в 3 канали (кольорове зображення)
            else:
                canvas_bgr = canvas_img  # Якщо зображення вже кольорове, просто використовуємо його
            
            # Розміри полотна
            ch, cw, _ = canvas_bgr.shape
            x_offset = (w - cw) // 2
            y_offset = (h - ch) // 2
            # Вставляємо полотно по центру
            frame[y_offset:y_offset + ch, x_offset:x_offset + cw] = canvas_bgr
            # Код для відправки зображення у вигляді потоку
            _, buffer = cv2.imencode('.jpg', frame)  # Кодуємо кадр у формат JPEG
            frame_bytes = buffer.tobytes()  # Перетворюємо в байти для відправки по мережі
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')  # Відправка кадру як частини HTTP-відповіді