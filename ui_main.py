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
        """Конструктор - вызывается при создании окна"""
        super().__init__()
        self.setWindowTitle("Менеджер рецептов (PyQt5 Practice)")
        self.resize(1200, 750)
        self.setMinimumSize(1000, 600)
        # Центральная часть окна
        self.db = Database()
        self.current_image_path = ""
        # 1. Верстка интерфейса
        self._setup_ui()
        # 2. Привязка событий
        self._bind_signals()
        # 3. Загрузка начальных данных
        self._refresh_table()

    def _setup_ui(self):
        """Создаём весь интерфейс окна"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Левая панель: Таблица с рецептами и кнопки
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Порции", "Время (мин)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        left_layout.addWidget(self.table)

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

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        self.le_title = QLineEdit()
        self.le_title.setPlaceholderText("Например: Борщ")
        form_layout.addRow("Название:", self.le_title)

        self.cb_category = QComboBox()
        self.cb_category.addItems(["Завтрак", "Суп", "Основное блюдо", "Салат", "Десерт"])
        form_layout.addRow("Категория:", self.cb_category)

        self.spin_servings = QSpinBox()
        self.spin_servings.setMinimum(1)
        self.spin_servings.setMaximum(99)
        form_layout.addRow("Порции:", self.spin_servings)

        self.spin_cook_time = QSpinBox()
        self.spin_cook_time.setMinimum(1)
        self.spin_cook_time.setMaximum(999)
        self.spin_cook_time.setSuffix(" мин")
        form_layout.addRow("Время готовки:", self.spin_cook_time)

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

        # Кнопки управления
        image_buttons_layout = QHBoxLayout()
        self.btn_load_image = QPushButton("Загрузить фото")
        self.btn_shopping_list = QPushButton("Список покупок")
        image_buttons_layout.addWidget(self.btn_load_image)
        image_buttons_layout.addWidget(self.btn_shopping_list)
        right_layout.addLayout(image_buttons_layout)

        # Разделитель
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([550, 450])
        main_layout.addWidget(splitter)

        # Применение стиля
        self._apply_style()

    def _apply_style(self):
        """Применяем стили"""
        style = """
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
            QMessageBox.warning(self, "Ошибка!", "Введите название рецепта!")
            self.le_title.setFocus()
            return
        try:
            self.db.add(
                title,
                self.cb_category.currentText(),
                self.spin_servings.value(),
                self.spin_cook_time.value(),
                self.te_ingredients.toPlainText().strip(),
                self.current_image_path
            )
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

        row = selected_rows[0].row()
        recipe_id = self.table.item(row, 0).data(Qt.UserRole)

        try:
            self.db.update(
                recipe_id,
                title,
                self.cb_category.currentText(),
                self.spin_servings.value(),
                self.spin_cook_time.value(),
                self.te_ingredients.toPlainText().strip(),
                self.current_image_path
            )
            self._refresh_table()
            self._clear_fields()
            QMessageBox.information(self, "Успех", "Рецепт обновлён!")
        except Exception as e:
            QMessageBox.critical(self, "Внимание", f"Не получилось обновить рецепт:\n{e}")

    def _delete_recipe(self):
        """Удаляем выбранный рецепт"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание!", "Сначала выберите рецепт!")
            return
          
        reply = QMessageBox.question(self,
                                 "Подтверждение", "Вы уверены, что хотите удалить этот рецепт?",
                                 QMessageBox.Yes | QMessageBox.No)

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
        """Заполнение формы при клике на строку таблицы"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        recipe_id = self.table.item(row, 0).data(Qt.UserRole)

        recipe = self.db.get_one(recipe_id)
        if recipe:
            self.le_title.setText(recipe[1] or "")
            category = recipe[2] or ""
            index = self.cb_category.findText(category)
            if index >= 0:
                self.cb_category.setCurrentIndex(index)
            else:
                self.cb_category.setCurrentIndex(0)
            self.spin_servings.setValue(recipe[3] or 1)
            self.spin_cook_time.setValue(recipe[4] or 0)
            self.te_ingredients.setText(recipe[5] or "")

            image_path = recipe[6] or ""
            if image_path and os.path.exists(image_path):
                self.current_image_path = image_path
                self._show_image(image_path)
            else:
                self.current_image_path = ""
                self.lbl_image.setText("Нет фото")
                self.lbl_image.setStyleSheet("background-color: #fff; border: 2px solid #999; border-radius: 8px;")

    def _refresh_table(self):
        """Обновление данных таблицы из БД"""
        self.table.setRowCount(0)
        recipes = self.db.get_all()

        for i, recipe in enumerate(recipes):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(recipe[1] or ""))
            self.table.setItem(i, 1, QTableWidgetItem(recipe[2] or ""))
            self.table.setItem(i, 2, QTableWidgetItem(str(recipe[3] or "")))
            self.table.setItem(i, 3, QTableWidgetItem(str(recipe[4] or "")))

            self.table.item(i, 0).setData(Qt.UserRole, recipe[0])

    def _load_image(self):
        """Загрузка и масштабирование изображения через Pillow"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото для рецепта", "",
                                                   "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_path:
            try:
                self.current_image_path = file_path
                self._show_image(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Внимание", f"Не удалось загрузить фото:\n{e}")

    def _show_image(self, path):
        """Показываем фото в QLabel (уменьшаем до 300x200)"""
        image = Image.open(path).convert("RGBA")
        image.thumbnail((300, 200), Image.Resampling.LANCZOS)

        data = image.tobytes("raw", "RGBA")
        qt_image = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qt_image)

        self.lbl_image.setPixmap(pixmap)
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setStyleSheet("background-color: #fff; border: 2px solid #006BBE; border-radius: 6px; ")

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
          
        shopping_list = "Список покупок\n" + "=" * 30 + "\n\n"

        for i, item in enumerate(items, 1):
            shopping_list += f"{i}. {item}\n"

        title = self.le_title.text().strip()
        if title:
            shopping_list += f"\nРецепт: {title}"

        QMessageBox.information(self, "Список покупок", shopping_list)

    def _clear_fields(self):
        """Очищаем все поля формы"""
        self.le_title.clear()
        self.cb_category.setCurrentIndex(0)
        self.spin_servings.setValue(1)
        self.spin_cook_time.setValue(1)
        self.te_ingredients.clear()
        self.current_image_path = ""

        self.lbl_image.setText("Фото")
        self.lbl_image.setStyleSheet(("background-color: #f5f5f5; border: 2px dashed #bbb; border-radius: 8px;"))
        self.lbl_image.setPixmap(QPixmap())

    def closeEvent(self, event):
        """Переопределение закрытия окна"""
        reply = QMessageBox.question(self, "Выход", "Сохранить изменения перед выходом?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if reply == QMessageBox.Cancel:
            event.ignore()
        else:
            self.db.close()
            event.accept()
