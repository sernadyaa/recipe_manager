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
      
        # Место для изображения
      
        self.image_label = QLabel("Нет фото")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #aaaaaa;
            border-radius: 8px;
            font-size: 16px;
            color: #888888;
        """)
        right_layout.addWidget(self.image_label)
        
        # Кнопки для фото и списка покупок
        image_buttons_layout = QHBoxLayout()
        self.btn_load_image = QPushButton("Загрузить фото")
        self.btn_shopping_list = QPushButton("Список покупок")
        image_buttons_layout.addWidget(self.btn_load_image)
        image_buttons_layout.addWidget(self.btn_shopping_list)
        right_layout.addLayout(image_buttons_layout)
      
      # разделитель (позволяет менять размер панелей мышкой)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([550, 450])
        main_layout.addWidget(splitter)
      
       # Применение стиля
        self._apply_style()
      def _apply_style(self):
        style = """
            /* Кнопки - зелёные */
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            /* Кнопка Удалить - красная */
            QPushButton#delete_button {
                background-color: #f44336;
            }
            QPushButton#delete_button:hover {
                background-color: #da190b;
            }
            
            /* Таблица */
            QTableWidget {
                gridline-color: #dddddd;
                alternate-background-color: #f9f9f9;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            /* Поля ввода */
            QLineEdit, QTextEdit, QSpinBox {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """
        self.setStyleSheet(style)
        self.btn_delete.setObjectName("delete_button")
        
    def _bind_signals(self):
      """Привязываем кнопки к функциям"""
      self.btn_add.clicked.connect(self._add_recipe)
      self.btn_edit.clicked.connect(self._edit_recipe)
      self.btn_delete.clicked.connect(self._delete_recipe)
      self.btn_load_image.clicked.connect(self._load_image)
      self.btn_shopping_list.clicked.connect(self._generate_shopping_list)
      self.table.itemSelectionChanged.connect(self._on_select_recipe)

    def _add_recipe(self):
      """Добавляем новый рецепт"""
      title = self.title_input.text().strip()
      if not title:
          QMessageBox.warning(self, "Внимание", "Введите название рецепта!")
          self.title_input.setFocus()
          return
      
      # Собираем данные из полей
      category = self.category_input.text().strip()
      servings = self.servings_input.value()
      cook_time = self.cook_time_input.value()
      ingredients = self.ingredients_input.toPlainText().strip()
      image_path = self.current_image_path
      
      # Добавляем в базу данных
      try:
          self.db.add(title, category, servings, cook_time, ingredients, image_path)
          self._refresh_table()
          self._clear_fields()
          QMessageBox.information(self, "Успех", "Рецепт добавлен!")
      except Exception as e:
          QMessageBox.critical(self, "Внимание", f"Не получилось добавить рецепт:\n{e}")
  
   def _edit_recipe(self):
      """Редактируем выбранный рецепт"""
      selected_rows = self.table.selectionModel().selectedRows()
      if not selected_rows:
          QMessageBox.warning(self, "Внимание", "Сначала выберите рецепт!")
          return
      
      title = self.title_input.text().strip()
      if not title:
          QMessageBox.warning(self, "Внимание", "Введите название рецепта!")
          return
      
      # Получаем ID рецепта
      row = selected_rows[0].row()
      recipe_id = self.table.item(row, 0).data(Qt.UserRole)
      
      # Собираем данные
      category = self.category_input.text().strip()
      servings = self.servings_input.value()
      cook_time = self.cook_time_input.value()
      ingredients = self.ingredients_input.toPlainText().strip()
      image_path = self.current_image_path
      
      # Обновляем в базе
      try:
          self.db.update(recipe_id, title, category, servings, cook_time, ingredients, image_path)
          self._refresh_table()
          self._clear_fields()
          QMessageBox.information(self, "Успех", "Рецепт обновлён!")
      except Exception as e:
          QMessageBox.critical(self, "Внимание", f"Не получилось обновить рецепт:\n{e}")
  
  def _delete_recipe(self):
      """Удаляем выбранный рецепт"""
      # Проверяем, что выбрана строка
      selected_rows = self.table.selectionModel().selectedRows()
      if not selected_rows:
          QMessageBox.warning(self, "Внимание!", "Сначала выберите рецепт!")
          return
      
      # Спрашиваем подтверждение
      reply = QMessageBox.question(
          self, 
          "Подтверждение удаления", 
          "Вы уверены, что хотите удалить этот рецепт?",
          QMessageBox.Yes | QMessageBox.No
      )
      
      if reply == QMessageBox.Yes:
          row = selected_rows[0].row()
          recipe_id = self.table.item(row, 0).data(Qt.UserRole)
          
          try:
              self.db.delete(recipe_id)
              self._refresh_table()
              self._clear_fields()
              QMessageBox.information(self, "Успех", "Рецепт удалён!")
          except Exception as e:
              QMessageBox.critical(self, "Внимание", f"Не получилось удалить рецепт:\n{e}")



