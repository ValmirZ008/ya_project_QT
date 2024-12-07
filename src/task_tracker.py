from task_tracker import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QListWidget, QMenu


class TaskTracker(QListWidget):
    def __init__(self, category, db_manager):
        super().__init__()
        self.category = category
        self.db_manager = db_manager
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.delete_menu)

    def dropEvent(self, event):
        if event.source() != self:
            event.acceptProposedAction()
            for item in event.source().selectedItems():
                task_id = item.data(Qt.ItemDataRole.UserRole)
                self.db_manager.update_task_category(task_id, self.category)
                event.source().takeItem(event.source().row(item))
                self.addItem(item)

    def delete_menu(self, position):
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
                    task_id = task.data(Qt.ItemDataRole.UserRole)
                    self.db_manager.delete_task(task_id)
                    self.takeItem(self.row(task))
        else:
            QMessageBox.warning(
                self, "Ошибка", "Пожалуйста, выберите задачу для удаления."
            )

