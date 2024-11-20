import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from task_tracker import *
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
)


class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Tracker")
        self.setGeometry(330, 250, 1000, 500)

        self.filter_widget = QWidget()
        self.filter_widget.setVisible(False)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.filter_button = QPushButton("Открыть фильтр")
        self.filter_button.clicked.connect(self.toggle_filter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск задач...")
        self.search_input.textChanged.connect(self.filter_tasks_by_search)

        self.difficulty_filter = QComboBox()
        self.difficulty_filter.addItems(["Все", "Легкая", "Средняя", "Сложная"])
        self.difficulty_filter.currentIndexChanged.connect(self.apply_filters)

        self.deadline_filter = QDateEdit()
        self.deadline_filter.setDisplayFormat("dd.MM.yyyy")
        self.deadline_filter.setDate(QDate.currentDate())
        self.deadline_filter.dateChanged.connect(self.apply_filters)

        self.reset_filter_button = QPushButton("Сбросить фильтр")
        self.reset_filter_button.clicked.connect(self.reset_filters)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Сложность:"))
        filter_layout.addWidget(self.difficulty_filter)
        filter_layout.addWidget(QLabel("Дедлайн до:"))
        filter_layout.addWidget(self.deadline_filter)
        filter_layout.addWidget(self.reset_filter_button)
        filter_layout.addStretch()

        self.filter_widget.setLayout(filter_layout)

        main_layout = QHBoxLayout()
        self.todo_list = TaskTracker()
        self.in_progress_list = TaskTracker()
        self.done_list = TaskTracker()

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
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.search_input)
        layout.addLayout(main_layout)
        layout.addWidget(self.create_add_button())

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_headers(self):
        self.todo_header = QLabel("Надо выполнить")
        self.in_progress_header = QLabel("В процессе")
        self.done_header = QLabel("Выполнено")

        for header in [self.todo_header, self.in_progress_header, self.done_header]:
            header.setStyleSheet("font-weight: bold; font-size: 20px;")

    def centered_layout(self, widget):
        hbox = QHBoxLayout()
        spacer_left = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        spacer_right = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        hbox.addItem(spacer_left)
        hbox.addWidget(widget)
        hbox.addItem(spacer_right)

        return hbox

    def create_add_button(self):
        add_button = QPushButton("Добавить задачу")
        add_button.clicked.connect(self.add_task)
        return add_button

    def toggle_filter(self):
        is_visible = self.filter_widget.isVisible()
        self.filter_widget.setVisible(not is_visible)
        self.filter_button.setText(
            "Скрыть фильтр" if not is_visible else "Открыть фильтр"
        )

    def add_task(self):
        dialog = QWidget()
        dialog.setWindowTitle("Добавить задачу")
        form_layout = QFormLayout()

        task_text_input = QLineEdit()
        task_text_input.setPlaceholderText("Название задачи")

        description_input = QLineEdit()
        description_input.setPlaceholderText("Описание задачи")

        priority_input = QComboBox()
        priority_input.addItems(["Низкий", "Средний", "Высокий"])

        deadline_input = QDateEdit()
        deadline_input.setDisplayFormat("dd.MM.yyyy")
        deadline_input.setDate(QDate.currentDate())

        form_layout.addRow("Название задачи:", task_text_input)
        form_layout.addRow("Описание:", description_input)
        form_layout.addRow("Приоритет:", priority_input)
        form_layout.addRow("Дедлайн:", deadline_input)

        dialog.setLayout(form_layout)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(
            lambda: self.on_add_task(
                dialog,
                task_text_input,
                description_input,
                priority_input,
                deadline_input,
            )
        )
        form_layout.addRow(add_button)

        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.show()

    def on_add_task(
        self, dialog, task_text_input, description_input, priority_input, deadline_input
    ):
        task_text = task_text_input.text().strip()
        description = description_input.text().strip()
        priority = priority_input.currentText()
        deadline = deadline_input.date()

        if task_text:
            new_task_text = f"{task_text}\nОписание: {description}\nПриоритет: {priority}\nДедлайн: {deadline.toString('dd.MM.yyyy')}"
            new_task = QListWidgetItem(new_task_text)
            new_task.setData(Qt.ItemDataRole.UserRole, description)
            new_task.setData(Qt.ItemDataRole.UserRole + 1, deadline)

            if priority == "Высокий":
                new_task.setBackground(QColor(255, 99, 71))
                new_task.setForeground(QColor(255, 255, 255))
            elif priority == "Средний":
                new_task.setBackground(QColor(255, 140, 0))
                new_task.setForeground(QColor(255, 255, 255))
            elif priority == "Низкий":
                new_task.setBackground(QColor(144, 238, 144))
                new_task.setForeground(QColor(0, 0, 0))

            self.todo_list.addItem(new_task)
            dialog.close()
        else:
            QMessageBox.warning(
                dialog, "Ошибка", "Название задачи не может быть пустым."
            )

    def filter_tasks_by_search(self):
        search_text = self.search_input.text().lower()

        def filter_list(task_list):
            for i in range(task_list.count()):
                item = task_list.item(i)
                item.setHidden(search_text not in item.text().lower())

        filter_list(self.todo_list)
        filter_list(self.in_progress_list)
        filter_list(self.done_list)

    def apply_filters(self):
        selected_difficulty = self.difficulty_filter.currentText()
        selected_deadline = self.deadline_filter.date()

        def filter_list(task_list):
            for i in range(task_list.count()):
                item = task_list.item(i)
                task_text = item.text()
                task_deadline = item.data(Qt.ItemDataRole.UserRole + 1)
                task_difficulty = self.get_task_difficulty(item)

                matches_difficulty = (
                    selected_difficulty == "Все"
                    or selected_difficulty in task_difficulty
                )

                matches_deadline = task_deadline <= selected_deadline

                item.setHidden(not (matches_difficulty and matches_deadline))

        filter_list(self.todo_list)
        filter_list(self.in_progress_list)
        filter_list(self.done_list)

    def get_task_difficulty(self, item):

        if "Легкая" in item.text():
            return "Легкая"
        elif "Средняя" in item.text():
            return "Средняя"
        elif "Сложная" in item.text():
            return "Сложная"
        return ""

    def reset_filters(self):
        self.difficulty_filter.setCurrentIndex(0)
        self.deadline_filter.setDate(QDate.currentDate())
        self.search_input.clear()
        self.show_all_tasks()

    def show_all_tasks(self):
        for task_list in [self.todo_list, self.in_progress_list, self.done_list]:
            for i in range(task_list.count()):
                task_list.item(i).setHidden(False)
        QMessageBox.information(self, "Фильтры сброшены", "Фильтры успешно сброшены.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Manager()
    window.show()
    sys.exit(app.exec())
