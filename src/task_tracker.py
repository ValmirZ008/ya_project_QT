from task_tracker import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QListWidget, QMenu


class TaskTracker(QListWidget):
    def __init__(self, category, db_connection):
        super().__init__()
        self.category = category
        self.db_connection = db_connection
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def dropEvent(self, event):
        if event.source() != self:
            event.acceptProposedAction()
            for item in event.source().selectedItems():
                task_id = item.data(Qt.ItemDataRole.UserRole)
                self.add_task_to_category(task_id, item)
                event.source().takeItem(event.source().row(item))
                self.addItem(item)

    def add_task_to_category(self, task_id, item):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE tasks SET category = ? WHERE id = ?", (self.category, task_id)
        )
        self.db_connection.commit()
        self.addItem(item)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        delete_action = context_menu.addAction("Удалить задачу")
        action = context_menu.exec(self.mapToGlobal(position))

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
                    self.remove_task_from_db(task)
                    self.takeItem(self.row(task))
        else:
            QMessageBox.warning(
                self, "Ошибка", "Пожалуйста, выберите задачу для удаления."
            )

    def remove_task_from_db(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db_connection.commit()
