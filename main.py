import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import MainWindow

def main():
    # 1. Создаем экземпляр приложения. sys.argv обязателен для передачи аргументов Qt
    app = QApplication(sys.argv)
    # 2. Шрифт по умолчанию для лучшей читаемости на всех ОС
    app.setFont(QFont('Segoe UI', 10))
    # 3. Метаданные приложения (отображаются в заголовке окна и отладчике)
    app.setApplicationName('Менеджер рецептов')
    # 4. Создаем и показываем главное окно
    window = MainWindow()
    window.show()
    # 5. Запускаем цикл обработки событий. sys.exit() гарантирует корректное завершение
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
