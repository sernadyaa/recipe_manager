import sqlite3


class Database:
    # Класс для работы с БД рецептов

    def __init__(self, db_name='recipes.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        # Создаёт таблицу recipes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                servings INTEGER,
                cook_time INTEGER,
                ingredients TEXT,
                image_path TEXT
            )
        """)
        self.connection.commit()

    def get_all(self):
        # Получает все рецепты из БД
        self.cursor.execute("SELECT * FROM recipes ORDER BY title")
        return self.cursor.fetchall()

    def get_one(self, recipe_id):
        # Получает рецепт по ID
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        return self.cursor.fetchone()

    def add(self, title, category, servings, cook_time, ingredients, image_path):
        # Добавляет новый рецепт
        self.cursor.execute("""
            INSERT INTO recipes (title, category, servings, cook_time, ingredients, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, servings, cook_time, ingredients, image_path))
        self.connection.commit()

    def update(self, recipe_id, title, category, servings, cook_time, ingredients, image_path):
        # Обновляет рецепт
        self.cursor.execute("""
            UPDATE recipes 
            SET title=?, category=?, servings=?, cook_time=?, ingredients=?, image_path=?
            WHERE id=?
        """, (title, category, servings, cook_time, ingredients, image_path, recipe_id))
        self.connection.commit()

    def delete(self, recipe_id):
        # Удаляет рецепт по ID
        self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        self.connection.commit()

    def close(self):
        # Закрывает соединение с БД
        self.connection.close()
