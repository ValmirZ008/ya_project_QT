import sys
from task_tracker import *
from database_manager import *
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QMessageBox,
    QLabel,
    QColorDialog,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tre1l0")
        self.setGeometry(330, 250, 1000, 500)

        self.db_manager = DatabaseManager("tasks.db")
        self.setup_ui()
        self.tasks()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.filter_button = QPushButton("Открыть фильтр")
        self.filter_button.clicked.connect(self.filter)

        self.change_color_button = QPushButton("Изменить цвет фона")
        self.change_color_button.clicked.connect(self.change_background_color)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск задач...")
        self.search_input.textChanged.connect(self.filter_tasks)

        self.difficulty_filter = QComboBox()
        self.difficulty_filter.addItems(["Все", "Низкий", "Средний", "Высокий"])
        self.difficulty_filter.currentIndexChanged.connect(self.filter_tasks)

        self.deadline_filter = QDateEdit()
        self.deadline_filter.setDisplayFormat("dd.MM.yyyy")
        self.deadline_filter.setDate(QDate.currentDate())
        self.deadline_filter.dateChanged.connect(self.filter_tasks)

        self.reset_filter_button = QPushButton("Сбросить фильтр")
        self.reset_filter_button.clicked.connect(self.reset_filters)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Приоритет:"))
        filter_layout.addWidget(self.difficulty_filter)
        filter_layout.addWidget(QLabel("Дедлайн до:"))
        filter_layout.addWidget(self.deadline_filter)
        filter_layout.addWidget(self.reset_filter_button)
        filter_layout.addStretch()

        self.filter_widget = QWidget()
        self.filter_widget.setLayout(filter_layout)
        self.filter_widget.setVisible(False)

        main_layout = QHBoxLayout()
        self.todo_list = TaskTracker("todo", self.db_manager)
        self.in_progress_list = TaskTracker("in_progress", self.db_manager)
        self.done_list = TaskTracker("done", self.db_manager)

        self.create_headers()

        todo_layout = QVBoxLayout()
        todo_layout.addLayout(self.centered_layout(self.todo_header))
        todo_layout.addWidget(self.todo_list)

        in_progress_layout = QVBoxLayout()
        in_progress_layout.addLayout(self.centered_layout(self.in_progress_header))
        in_progress_layout.addWidget(self.in_progress_list)

        done_layout = QVBoxLayout()
        done_layout.addLayout(self.centered_layout(self.done_header))
        done_layout.addWidget(self.done_list)

        main_layout.addLayout(todo_layout)
        main_layout.addLayout(in_progress_layout)
        main_layout.addLayout(done_layout)

        layout.addWidget(self.filter_button)
        layout.addWidget(self.change_color_button)
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.search_input)
        layout.addLayout(main_layout)

        add_button = QPushButton("Добавить задачу")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, color)
            self.setPalette(palette)

    def filter(self):
        is_visible = self.filter_widget.isVisible()
        self.filter_widget.setVisible(not is_visible)
        self.filter_button.setText(
            "Скрыть фильтр" if not is_visible else "Открыть фильтр"
        )

    def tasks(self):
        tasks = self.db_manager.fetch_tasks()
        for task_id, title, description, priority, deadline, category in tasks:
            task_text = f"{title}\nОписание: {description}\nПриоритет: {priority}\nДедлайн: {QDate.fromString(deadline, 'yyyy-MM-dd').toString('dd.MM.yyyy')}"
            item = QListWidgetItem(task_text)
            item.setData(Qt.ItemDataRole.UserRole, task_id)
            self.set_task_color(item, priority)

            if category == "todo":
                self.todo_list.addItem(item)
            elif category == "in_progress":
                self.in_progress_list.addItem(item)
            elif category == "done":
                self.done_list.addItem(item)

    def set_task_color(self, item, priority):
        colors = {
            "Низкий": QColor("green"),
            "Средний": QColor("dark orange"),
            "Высокий": QColor("red"),
        }
        item.setBackground(colors.get(priority, QColor("white")))

    def create_headers(self):
        self.todo_header = QLabel("Надо выполнить")
        self.in_progress_header = QLabel("В процессе")
        self.done_header = QLabel("Выполнено")

        for header in [self.todo_header, self.in_progress_header, self.done_header]:
            header.setStyleSheet("font-weight: bold; font-size: 20px;")

    def centered_layout(self, widget):
        hbox = QHBoxLayout()
        hbox.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        hbox.addWidget(widget)
        hbox.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        return hbox

    def add_task(self):
        dialog = QWidget()
        dialog.setWindowTitle("Добавить задачу")
        form_layout = QFormLayout()

        task_text_input = QLineEdit()
        description_input = QLineEdit()
        priority_input = QComboBox()
        priority_input.addItems(["Низкий", "Средний", "Высокий"])
        deadline_input = QDateEdit()
        deadline_input.setDisplayFormat("dd.MM.yyyy")
        deadline_input.setDate(QDate.currentDate())

        form_layout.addRow("Название задачи:", task_text_input)
        form_layout.addRow("Описание:", description_input)
        form_layout.addRow("Приоритет:", priority_input)
        form_layout.addRow("Дедлайн:", deadline_input)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(
            lambda: self.add_task_to_database(
                dialog,
                task_text_input.text(),
                description_input.text(),
                priority_input.currentText(),
                deadline_input.date().toString("yyyy-MM-dd"),
                "todo",
            )
        )
        form_layout.addRow(add_button)

        dialog.setLayout(form_layout)
        dialog.show()

    def add_task_to_database(
        self, dialog, title, description, priority, deadline, category
    ):
        if not title.strip():
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым.")
            return

        task_id = self.db_manager.add_task(
            title, description, priority, deadline, category
        )
        task_text = f"{title}\nОписание: {description}\nПриоритет: {priority}\nДедлайн: {QDate.fromString(deadline, 'yyyy-MM-dd').toString('dd.MM.yyyy')}"
        item = QListWidgetItem(task_text)
        item.setData(Qt.ItemDataRole.UserRole, task_id)
        self.set_task_color(item, priority)
        self.todo_list.addItem(item)
        dialog.close()

    def filter_tasks(self):
        search_text = self.search_input.text().lower()
        selected_priority = self.difficulty_filter.currentText()
        deadline = self.deadline_filter.date().toString("yyyy-MM-dd")

        for task_list in [self.todo_list, self.in_progress_list, self.done_list]:
            for i in range(task_list.count()):
                item = task_list.item(i)
                task_text = item.text().lower()
                task_deadline = QDate.fromString(
                    item.text().split("\n")[-1].split(": ")[1], "dd.MM.yyyy"
                ).toString("yyyy-MM-dd")

                matches_priority = (
                    selected_priority == "Все"
                    or f"приоритет: {selected_priority.lower()}" in task_text
                )
                matches_deadline = QDate.fromString(
                    task_deadline, "yyyy-MM-dd"
                ) <= QDate.fromString(deadline, "yyyy-MM-dd")
                matches_search = search_text in task_text

                item.setHidden(
                    not (matches_priority and matches_deadline and matches_search)
                )

    def reset_filters(self):
        self.search_input.clear()
        self.difficulty_filter.setCurrentIndex(0)
        self.deadline_filter.setDate(QDate.currentDate())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
