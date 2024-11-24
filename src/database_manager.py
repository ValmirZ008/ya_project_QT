import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT,
                deadline TEXT,
                category TEXT
            )
        """
        )
        self.connection.commit()

    def add_task(self, title, description, priority, deadline, category):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, description, priority, deadline, category)
            VALUES (?, ?, ?, ?, ?)
        """,
            (title, description, priority, deadline, category),
        )
        self.connection.commit()
        return cursor.lastrowid

    def fetch_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, title, description, priority, deadline, category FROM tasks"
        )
        return cursor.fetchall()

    def update_task_category(self, task_id, category):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE tasks SET category = ? WHERE id = ?", (category, task_id)
        )
        self.connection.commit()

    def delete_task(self, task_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()
