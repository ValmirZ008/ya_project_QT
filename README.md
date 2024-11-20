# **Папка src**

      Класс TaskTracker
**Назначение:** Это кастомный виджет, основанный на QListWidget, предназначенный для отображения списка задач и управления ими.

**Методы:**
1.**__init__(self):** Инициализирует виджет с поддержкой перетаскивания задач (drag-and-drop), возможности принимать перетаскиваемые элементы, отображать индикатор перетаскивания и поддерживать множественный выбор.

2.**dropEvent(self, event):** Обрабатывает событие перетаскивания, добавляя задачи из другого списка и удаляя их из исходного списка.

3.**clone(self):** Создает новый элемент списка с таким же текстом, что и у текущего.

4.**contextMenuEvent(self, event):** Открывает контекстное меню с возможностью удаления задачи.

5.**delete_selected_tasks(self):** Удаляет выбранные задачи после подтверждения пользователем.

        Класс Manager
**Назначение:** Основной класс приложения, управляющий интерфейсом и логикой работы с задачами.

**Методы:**

1. **__init__(self):** Инициализирует окно, задает размеры, название и видимость фильтра. Настроен на создание пользовательского интерфейса.
2. **setup_ui(self):** Создает и настраивает элементы управления, включая кнопки, поля для поиска, фильтры по сложности и дедлайну, а также макет для отображения задач.
3. **create_headers(self):** Создает заголовки для каждой из категорий задач («Надо выполнить», «В процессе», «Выполнено») и применяет стиль.
4. **centered_layout(self, widget):** Помещает переданный виджет в центр горизонтального макета с отступами.
5. **create_add_button(self):** Создает кнопку для добавления новой задачи.
6. **toggle_filter(self):** Открывает или скрывает панель фильтрации задач.
7. **add_task(self):** Открывает окно для добавления новой задачи с полями для ввода информации.
8. **on_add_task(self, dialog, task_text_input, description_input, priority_input, deadline_input):** Обрабатывает добавление задачи, проверяя введенные данные и добавляя задачу в список, а также применяет цветовую кодировку по приоритету.
9. **filter_tasks_by_search(self):** Фильтрует задачи по введенному тексту в поле поиска.
10. **apply_filters(self):** Применяет фильтры по сложности и дедлайну к задачам.
11. **get_task_difficulty(self, item):** Определяет сложность задачи, анализируя ее текст.
12. **reset_filters(self)**: Сбрасывает все фильтры и показывает все задачи.
13. **show_all_tasks(self):** Открывает все задачи, сбрасывая любые фильтры.
# Общие функциональные особенности:

-  **Фильтрация задач:** Пользователи могут фильтровать задачи по сложности, дедлайну и поисковым запросам.
- **Управление задачами:** Задачи можно перетаскивать между различными категориями (например, с "Надо выполнить" в "В процессе").
- **Цветовая кодировка:** Задачи отображаются с цветами, соответствующими их приоритету: красный для высокого, оранжевый для среднего и зеленый для низкого.
- **Добавление задач:** Через форму можно добавить новые задачи с описанием, приоритетом и дедлайном.
- **Удаление задач:** Через контекстное меню можно удалить одну или несколько задач, после подтверждения действия пользователем.
- **Drag-and-drop** функциональность позволяет пользователю легко управлять задачами, перетаскивая их между различными состояниями.

# Логика связи классов:

1.TaskTracker отвечает за отображение задач в виде списка и управление ими. Он позволяет добавлять, удалять и перемещать задачи с помощью перетаскивания.

2.Manager является центральным элементом, который создает интерфейс, управляет состоянием задач (todo, in progress, done) и фильтрацией задач. Он взаимодействует с TaskTracker через метод добавления задач в нужный список (например, в список "Надо выполнить").

3.При добавлении задачи (в методе add_task) создается новый объект QListWidgetItem, который добавляется в список "Надо выполнить". Каждой задаче присваивается цвет в зависимости от сложности:
Легкая — зеленый цвет
Средняя — оранжевый цвет
Сложная — красный цвет

4.В классе TaskTracker реализованы функции для удаления задач, а также для обработки события перетаскивания. Это позволяет перемещать задачи между различными списками (например, из "Надо выполнить" в "В процессе" или "Выполнено").

5.Фильтрация реализована через комбинированные элементы (QComboBox для сложности и QDateEdit для дедлайна), которые позволяют отфильтровывать задачи в списке по выбранным критериям. Методы фильтрации (apply_filters и reset_filters) скрывают задачи, которые не соответствуют условиям.

6.Взаимодействие между классами происходит через передачу данных между ними: задачи передаются между различными состояниями через TaskTracker, а в Manager выполняется их фильтрация и добавление.
