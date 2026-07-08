import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Запуск приложения 'Менеджер рецептов'")
    try:
        app = QApplication(sys.argv)
        app.setFont(QFont('Segoe UI', 10))
        app.setApplicationName('Менеджер рецептов')

        window = MainWindow()
        window.show()

        logger.info("Приложение успешно запущено")
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
