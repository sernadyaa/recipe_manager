import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QLineEdit, QTextEdit, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
                             QSplitter, QSpinBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
from database import Database


class MainWindow(QMainWindow):
    """Главное окно приложения Менеджер рецептов"""

    def __init__(self):
        super().__init__()

        # Настраиваем окно
        self.setWindowTitle("Менеджер рецептов (PyQt5 Practice)")
        self.resize(1200, 750)
        self.setMinimumSize(1000, 600)

        # Подключаемся к базе данных
        self.db = Database()
        # Здесь будем хранить путь к загруженному фото
        self.current_image_path = ""
        # Создаём интерфейс
        self._setup_ui()
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
        self.le_title = QLineEdit()
        self.le_title.setPlaceholderText("Например: Борщ")
        form_layout.addRow("Название:", self.le_title)

        # Поле: Категория
        self.cb_category = QComboBox()
        self.cb_category.addItems(["Завтрак", "Суп", "Основное блюдо", "Салат", "Десерт"])

        # Поле: Порции (число от 1 до 99)
        self.spin_servings = QSpinBox()
        self.spin_servings.setMinimum(1)
        self.spin_servings.setMaximum(99)
        form_layout.addRow("Порции:", self.spin_servings)

        # Поле: Время готовки
        self.spin_cook_time = QSpinBox()
        self.spin_cook_time.setMinimum(1)
        self.spin_cook_time.setMaximum(999)
        self.spin_cook_time.setSuffix(" мин")
        form_layout.addRow("Время готовки:", self.spin_cook_time)

        # Поле: Ингредиенты (многострочное)
        self.te_ingredients = QTextEdit()
        self.te_ingredients.setPlaceholderText(
            "Введите ингредиенты по одному на строку:\n"
            "картошка 500г\n"
            "свекла 200г\n"
            "лук 1шт"
        )
        self.te_ingredients.setMaximumHeight(120)
        form_layout.addRow("Ингредиенты:", self.te_ingredients)

        right_layout.addWidget(form_widget)

        # Место для изображения
        self.lbl_image = QLabel("Обложка/Фото")
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setMinimumHeight(200)
        self.lbl_image.setStyleSheet("background-color: #f5f5f5; border: 2px dashed #bbb; border-radius: 8px;")
        right_layout.addWidget(self.lbl_image)

        # Кнопки для фото и списка покупок
        image_buttons_layout = QHBoxLayout()
        self.btn_load_image = QPushButton("Загрузить фото")
        self.btn_shopping_list = QPushButton("Список покупок")
        image_buttons_layout.addWidget(self.btn_load_image)
        image_buttons_layout.addWidget(self.btn_shopping_list)
        right_layout.addLayout(image_buttons_layout)

        # разделитель
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([550, 450])
        main_layout.addWidget(splitter)

        # Применение стиля
        self._apply_style()

    def _apply_style(self):
        style ="""
            QPushButton {
                background-color: #FFFFFF;
                color: black;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:pressed {
                background-color: #E5F4FF;
            }
            QPushButton#delete_button {
                background-color: #006BBE;
            }
            QPushButton#delete_button:hover {
                background-color: #006BBE;
            }
            QTableWidget {
                gridline-color: #F0F0F0;
                alternate-background-color: #F0F0F0;
            }
            QTableWidget::item:selected {
                background-color: #E5F4FF;
                color: black;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                padding: 6px;
                border: 1px solid #8F949C;
                border-radius: 3px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus
            {border: 2px solid #006BBE;}
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
        title = self.le_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Внимание", "Введите название рецепта!")
            self.le_title.setFocus()
            return

        # Собираем данные из полей
        category = self.cb_category.text().strip()
        servings = self.spin_servings.value()
        cook_time = self.spin_cook_time.value()
        ingredients = self.te_ingredients.toPlainText().strip()
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

        title = self.le_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Внимание", "Введите название рецепта!")
            return

        # Получаем ID рецепта
        row = selected_rows[0].row()
        recipe_id = self.table.item(row, 0).data(Qt.UserRole)

        # Собираем данные
        category = self.cb_category.text().strip()
        servings = self.spin_servings.value()
        cook_time = self.spin_cook_time.value()
        ingredients = self.te_ingredients.toPlainText().strip()
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

    def _on_select_recipe(self):
        """Когда кликаем на строку в таблице - заполняем форму"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        recipe_id = self.table.item(row, 0).data(Qt.UserRole)

        # Получаем данные из базы
        recipe = self.db.get_one(recipe_id)
        if recipe:
            # Заполняем поля
            self.le_title.setText(recipe[1] or "")
            self.cb_category.setText(recipe[2] or "")
            self.spin_servings.setValue(recipe[3] or 1)
            self.spin_cook_time.setValue(recipe[4] or 0)
            self.te_ingredients.setText(recipe[5] or "")

            # Загружаем фото, если есть
            image_path = recipe[6] or ""
            if image_path and os.path.exists(image_path):
                self.current_image_path = image_path
                self._show_image(image_path)
            else:
                self.current_image_path = ""
                self.lbl_image.setText("Нет фото")
                self.lbl_image.setStyleSheet("""
                    background-color: #f0f0f0;
                    border: 2px dashed #aaaaaa;
                    border-radius: 8px;
                    font-size: 16px;
                    color: #888888;
                """)

    def _refresh_table(self):
        """Обновляем таблицу - загружаем все рецепты из БД"""
        self.table.setRowCount(0)  # Очищаем таблицу

        recipes = self.db.get_all()

        for i, recipe in enumerate(recipes):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(recipe[1] or ""))
            self.table.setItem(i, 1, QTableWidgetItem(recipe[2] or ""))
            self.table.setItem(i, 2, QTableWidgetItem(str(recipe[3] or "")))
            self.table.setItem(i, 3, QTableWidgetItem(str(recipe[4] or "")))

            # Сохраняем ID рецепта (для редактирования/удаления)
            self.table.item(i, 0).setData(Qt.UserRole, recipe[0])

    def _load_image(self):
        """Загружаем фото"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото для рецепта", "",
                                                   "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)")

        if not file_path:
            return

        try:
            self.current_image_path = file_path
            self._show_image(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка!", f"Не получилось загрузить фото:\n{e}")

    def _show_image(self, path):
        """Показываем фото в QLabel (уменьшаем до 300x200)"""
        image = Image.open(path).convert("RGBA")

        # Уменьшаем до 300x200 с сохранением пропорций
        image.thumbnail((300, 200), Image.Resampling.LANCZOS)

        # Конвертируем для PyQt5
        data = image.tobytes("raw", "RGBA")
        qt_image = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qt_image)

        self.lbl_image.setPixmap(pixmap)
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px solid #4CAF50;
            border-radius: 8px;
        """)

    def _generate_shopping_list(self):
        """Создаём список покупок из ингредиентов"""
        ingredients_text = self.te_ingredients.toPlainText().strip()

        if not ingredients_text:
            QMessageBox.warning(self, "Внимание", "Нет ингредиентов для списка!")
            return

        items = [line.strip() for line in ingredients_text.split('\n') if line.strip()]

        if not items:
            QMessageBox.warning(self, "Внимание", "Нет ингредиентов для списка!")
            return

        # Формируем список покупок
        shopping_list = "Список покупок\n"
        shopping_list += "=" * 30 + "\n\n"

        for i, item in enumerate(items, 1):
            shopping_list += f"{i}. {item}\n"

        # Добавляем название рецепта
        title = self.le_title.text().strip()
        if title:
            shopping_list += f"\nРецепт: {title}"

        QMessageBox.information(self, "Список покупок", shopping_list)

    def _clear_fields(self):
        """Очищаем все поля формы"""
        self.le_title.clear()
        self.cb_category.clear()
        self.spin_servings.setValue(1)
        self.spin_cook_time.setValue(0)
        self.te_ingredients.clear()
        self.current_image_path = ""

        self.lbl_image.setText("Нет фото")
        self.lbl_image.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #aaaaaa;
            border-radius: 8px;
            font-size: 16px;
            color: #888888;
        """)
        self.lbl_image.setPixmap(QPixmap())  # Убираем картинку

        def closeEvent(self, event):
        """Переопределение закрытия окна """
        reply = QMessageBox.question(self, "Выход", "Сохранить изменения перед выходом?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if reply == QMessageBox.Cancel:
            event.ignore()
        else:
            self.db.close()
            event.accept()
