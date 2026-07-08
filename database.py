import sqlite3
import logging

logger = logging.getLogger(__name__)


class Database:
    """Класс для работы с базой данных рецептов"""

    def __init__(self, db_name="recipes.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        logger.info(f"Подключение к БД: {db_name}")

    def _create_table(self):
        try:
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
            logger.info("Таблица recipes создана/проверена")
        except Exception as e:
            logger.error(f"Ошибка создания таблицы: {e}")
            raise

    def get_all(self):
        try:
            self.cursor.execute("SELECT * FROM recipes ORDER BY title")
            recipes = self.cursor.fetchall()
            logger.info(f"Загружено рецептов: {len(recipes)}")
            return recipes
        except Exception as e:
            logger.error(f"Ошибка загрузки рецептов: {e}")
            return []

    def add(self, title, category, servings, cook_time, ingredients, image_path):
        try:
            self.cursor.execute("""
                INSERT INTO recipes (title, category, servings, cook_time, ingredients, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, category, servings, cook_time, ingredients, image_path))
            self.connection.commit()
            logger.info(f"Добавлен рецепт: {title}")
        except Exception as e:
            logger.error(f"Ошибка добавления рецепта '{title}': {e}")
            raise

    def update(self, recipe_id, title, category, servings, cook_time, ingredients, image_path):
        try:
            self.cursor.execute("""
                UPDATE recipes 
                SET title=?, category=?, servings=?, cook_time=?, ingredients=?, image_path=?
                WHERE id=?
            """, (title, category, servings, cook_time, ingredients, image_path, recipe_id))
            self.connection.commit()
            logger.info(f"Обновлён рецепт: {title} (ID: {recipe_id})")
        except Exception as e:
            logger.error(f"Ошибка обновления рецепта ID {recipe_id}: {e}")
            raise

    def delete(self, recipe_id):
        try:
            self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            self.connection.commit()
            logger.info(f"Удалён рецепт с ID: {recipe_id}")
        except Exception as e:
            logger.error(f"Ошибка удаления рецепта ID {recipe_id}: {e}")
            raise

    def close(self):
        try:
            self.connection.close()
            logger.info("Соединение с БД закрыто")
        except Exception as e:
            logger.error(f"Ошибка закрытия БД: {e}")
