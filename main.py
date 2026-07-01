import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Verdana', 12))
    app.setApplicationName('Менеджер рецептов')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
