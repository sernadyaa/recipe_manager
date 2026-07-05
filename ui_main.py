import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QLineEdit, QTextEdit, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
                             QSplitter, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
from database import Database

class MainWindow(QMainWindow):
    """Главное окно приложения Менеджер рецептов"""

    def __init__(self):
        super().__init__()

        # Настраиваем окно
        self.setWindowTitle("Менеджер рецептов")
        self.resize(1200, 750)
        self.setMinimumSize(1000, 600)

        # Подключаемся к базе данных
        self.db = Database()
        # Здесь будем хранить путь к загруженному фото
        self.current_image_path = ""
        # Создаём интерфейс
        self.setupUi(self)
        # Привязываем кнопки к функциям
        self._bind_signals()
        # Загружаем рецепты в таблицу
        self._refresh_table()
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Левая панель: Таблица с рецептами и кнопки
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Порции", "Время (мин)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        left_layout.addWidget(self.table)

        # Кнопки под таблицей
        buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_edit)
        buttons_layout.addWidget(self.btn_delete)
        left_layout.addLayout(buttons_layout)

        # Правая панель: Форма для ввода данных
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Форма с полями ввода
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        # Поле: Название
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Например: Борщ")
        form_layout.addRow("Название:", self.title_input)

        # Поле: Категория
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Например: Супы")
        form_layout.addRow("Категория:", self.category_input)

        # Поле: Порции (число от 1 до 99)
        self.servings_input = QSpinBox()
        self.servings_input.setMinimum(1)
        self.servings_input.setMaximum(99)
        form_layout.addRow("Порции:", self.servings_input)

        # Поле: Время готовки
        self.cook_time_input = QSpinBox()
        self.cook_time_input.setMinimum(1)
        self.cook_time_input.setMaximum(999)
        self.cook_time_input.setSuffix(" мин")
        form_layout.addRow("Время готовки:", self.cook_time_input)

        # Поле: Ингредиенты (многострочное)
        self.ingredients_input = QTextEdit()
        self.ingredients_input.setPlaceholderText(
            "Введите ингредиенты по одному на строку:\n"
            "картошка 500г\n"
            "свекла 200г\n"
            "лук 1шт"
        )
        self.ingredients_input.setMaximumHeight(120)
        form_layout.addRow("Ингредиенты:", self.ingredients_input)

        right_layout.addWidget(form_widget)
