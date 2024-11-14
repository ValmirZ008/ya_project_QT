import sys
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QMenu,
    QDateEdit,
    QComboBox,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QColor


class TaskTracker(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

    def dropEvent(self, event):
        if event.source() == self:
            super().dropEvent(event)
        else:
            event.acceptProposedAction()
            for item in event.source().selectedItems():
                self.addItem(item.clone())
                event.source().takeItem(event.source().row(item))

    def clone(self):
        return QListWidgetItem(self.text())

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        delete_action = context_menu.addAction("Удалить задачу")
        action = context_menu.exec(event.globalPos())

        if action == delete_action:
            self.delete_selected_tasks()

    def delete_selected_tasks(self):
        selected_tasks = self.selectedItems()
        if selected_tasks:
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                "Вы уверены, что хотите удалить выбранные задачи?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                for task in selected_tasks:
                    self.takeItem(self.row(task))
        else:
            QMessageBox.warning(
                self, "Ошибка", "Пожалуйста, выберите задачу для удаления."
            )


class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tru1l0")
        self.setGeometry(330, 250, 1000, 500)

        layout = QHBoxLayout()

        self.todo_list = TaskTracker()
        self.in_progress_list = TaskTracker()
        self.done_list = TaskTracker()

        self.create_headers()

        self.add_button = QPushButton("Добавить задачу")
        self.add_button.clicked.connect(self.add_task)

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
        todo_layout.addLayout(self.centered_layout(self.todo_header))
        todo_layout.addWidget(self.todo_list)

        in_progress_layout = QVBoxLayout()
        in_progress_layout.addLayout(self.centered_layout(self.in_progress_header))
        in_progress_layout.addWidget(self.in_progress_list)

        done_layout = QVBoxLayout()
        done_layout.addLayout(self.centered_layout(self.done_header))
        done_layout.addWidget(self.done_list)

        layout.addLayout(todo_layout)
        layout.addLayout(in_progress_layout)
        layout.addLayout(done_layout)

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

    def get_main_layout(self, layout):
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.add_button)
        return main_layout

    def add_task(self):
        dialog = QWidget()
        dialog.setWindowTitle("Добавить задачу")

        form_layout = QFormLayout()

        task_text_input = QLineEdit()

        deadline_input = QDateEdit()
        deadline_input.setDisplayFormat("dd.MM.yyyy")
        deadline_input.setDate(QDate.currentDate())

        difficulty_input = QComboBox()
        difficulty_input.addItems(["Легкая", "Средняя", "Сложная"])

        form_layout.addRow("Название задачи:", task_text_input)
        form_layout.addRow("Дедлайн:", deadline_input)
        form_layout.addRow("Сложность:", difficulty_input)

        dialog.setLayout(form_layout)

        add_button = QPushButton("Добавить")

        def add_clicked():
            task_text = task_text_input.text().strip()
            deadline = deadline_input.date().toString("dd.MM.yyyy")
            difficulty = difficulty_input.currentText()

            if task_text:
                new_task_text = f"{task_text}\nДедлайн: {deadline}\nСложность: {difficulty}"
                new_task = QListWidgetItem(new_task_text)
                new_task.setData(Qt.ItemDataRole.UserRole, deadline_input.date())
                new_task.setFlags(new_task.flags() | Qt.ItemFlag.ItemIsEditable)

                if difficulty == "Легкая":
                    new_task.setBackground(QColor(144, 238, 144))
                    new_task.setForeground(QColor(0, 0, 0))
                elif difficulty == "Средняя":
                    new_task.setBackground(QColor(255, 140, 0))
                    new_task.setForeground(QColor(0, 0, 0))
                elif difficulty == "Сложная":
                    new_task.setBackground(QColor(255, 99, 71))
                    new_task.setForeground(QColor(255, 255, 255))

                self.todo_list.addItem(new_task)
                dialog.close()
            else:
                QMessageBox.warning(dialog, "Ошибка", "Задача не может быть пустой, лентяй!")

        add_button.clicked.connect(add_clicked)

        form_layout.addRow(add_button)

        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Manager()
    window.show()
    sys.exit(app.exec())
