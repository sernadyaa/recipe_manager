import sqlite3

class Database:
    def __init__(self, db_name='recipes.db'):  # подключение к БД
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):  # cоздаём таблицу recipes
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

def get_all(self):  # получаем все рецепты из бд
    self.cursor.execute("SELECT * FROM recipes ORDER BY title")
    recipes = self.cursor.fetchall()
    print(f"Загружено рецептов: {len(recipes)}")
    return recipes

def get_one(self, recipe_id):  # получаем рецепт по его ID
    self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    return self.cursor.fetchone()

def add(self, title, category, servings, cook_time, ingredients, image_path):  # добавление нового рецепта
    self.cursor.execute("""
            INSERT INTO recipes (title, category, servings, cook_time, ingredients, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, servings, cook_time, ingredients, image_path))
    self.connection.commit()
    print(f"Добавлен рецепт: {title}")

def update(self, recipe_id, title, category, servings, cook_time, ingredients, image_path):  # обновляем рецепт
    self.cursor.execute("""
            UPDATE recipes 
            SET title=?, category=?, servings=?, cook_time=?, ingredients=?, image_path=?
            WHERE id=?
        """, (title, category, servings, cook_time, ingredients, image_path, recipe_id))
    self.connection.commit()
    print(f"Обновлён рецепт: {title}")

def delete(self, recipe_id):  # удаляем рецепт ID
    self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    self.connection.commit()
    print(f"Удалён рецепт с ID: {recipe_id}")

def close(self):  # закрываем соединение с бд
    self.connection.close()
    print("Соединение с БД закрыто")
