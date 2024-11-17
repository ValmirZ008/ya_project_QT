from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QMenu,
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
