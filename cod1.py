import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QInputDialog,
    QLabel,
    QMessageBox,
)


class TaskTracker(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, event):
        if event.source() == self:
            super().dropEvent(event)
        else:
            event.acceptProposedAction()
            item = event.source().currentItem()
            self.addItem(item.clone())
            event.source().takeItem(event.source().row(item))

    def clone(self):
        return QListWidgetItem(self.text())


class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tru1lo")
        self.setGeometry(330, 250, 1000, 500)

        layout = QHBoxLayout()

        self.todo_list = TaskTracker()
        self.in_progress_list = TaskTracker()
        self.done_list = TaskTracker()

        self.create_headers()

        self.add_button = QPushButton("Добавить задачу")
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Удалить задачу")
        self.delete_button.clicked.connect(self.delete_task)

        self.setup_layout(layout)

        main_container = QWidget()
        main_container.setLayout(self.get_main_layout(layout))
        self.setCentralWidget(main_container)

    def create_headers(self):
        self.todo_header = QLabel("Надо выполнить")
        self.in_progress_header = QLabel("В процессе")
        self.done_header = QLabel("Выполнено")

        for header in [self.todo_header, self.in_progress_header, self.done_header]:
            header.setStyleSheet("font-weight: bold; font-size: 20px;")

    def setup_layout(self, layout):
        todo_layout = QVBoxLayout()
        todo_layout.addWidget(self.todo_header)
        todo_layout.addWidget(self.todo_list)

        in_progress_layout = QVBoxLayout()
        in_progress_layout.addWidget(self.in_progress_header)
        in_progress_layout.addWidget(self.in_progress_list)

        done_layout = QVBoxLayout()
        done_layout.addWidget(self.done_header)
        done_layout.addWidget(self.done_list)

        layout.addLayout(todo_layout)
        layout.addLayout(in_progress_layout)
        layout.addLayout(done_layout)

    def get_main_layout(self, layout):
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.delete_button)
        return main_layout

    def add_task(self):
        task_text, user_response = QInputDialog.getText(
            self, "Добавить задачу", "Введите текст задачи:")

        # Проверка на пустое значение
        if user_response:
            if task_text.strip():
                new_task = QListWidgetItem(task_text)
                self.todo_list.addItem(new_task)
            else:
                QMessageBox.warning(
                    self, "Ошибка", "Задача не может быть пустой, лентяй!")

    def delete_task(self):
        current_list = self.focusWidget()
        if isinstance(current_list, TaskTracker):
            selected_tasks = current_list.selectedItems()
            if selected_tasks:
                for task in selected_tasks:
                    current_list.takeItem(current_list.row(task))
            else:
                QMessageBox.warning(
                    self, "Ошибка", "Пожалуйста, выберите задачу для удаления.")

            # Переделать delete_task


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Manager()
    window.show()
    sys.exit(app.exec())
