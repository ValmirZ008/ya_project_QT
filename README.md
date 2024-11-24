# **Папка src**

      Класс DatabaseManager(файл database_manager.py)
**Назначение:**  предназначен для работы с базой данных SQLite и выполнения операций с таблицей задач.

**Методы:** 
1.**__init__(self, db_path):** Устанавливает подключение к базе данных по указанному пути и создает таблицы, если они не существуют.

2.**create_tables(self):** Создает таблицу tasks с полями для хранения задач, если таблица еще не существует.

3.**add_task(self, title, description, priority, deadline, category):** Добавляет новую задачу в таблицу tasks и возвращает ID добавленной задачи.

4.**fetch_tasks(self):** Извлекает все задачи из таблицы tasks и возвращает их в виде списка.

5.**update_task_category(self, task_id, category):** Обновляет категорию задачи с указанным ID.

6.**delete_task(self, task_id):** Удаляет задачу с указанным ID из таблицы tasks.

      Класс TaskTracker(файл task_tracker.py)
**Назначение:** Это кастомный виджет, основанный на QListWidget, предназначенный для отображения списка задач и управления ими.

**Методы:**

1.**__init__(self):** Инициализирует виджет с поддержкой перетаскивания задач (drag-and-drop), возможности принимать перетаскиваемые элементы, отображать индикатор перетаскивания и поддерживать множественный выбор.

2.**dropEvent(self, event):** Обрабатывает событие перетаскивания, добавляя задачи из другого списка и удаляя их из исходного списка.

3.**add_task_to_category(self, task_id, item):** Обновляет категорию задачи в базе данных после ее добавления в этот список. Также добавляет задачу в текущий список.

4.**show_context_menu(self, position):** Отображает контекстное меню при щелчке правой кнопкой мыши по элементу задачи. Это меню предлагает возможность удалить выбранную задачу.

5.**delete_selected_tasks(self):** Удаляет выбранные задачи после подтверждения пользователем.

        Класс Manager(файл main.py)
**Назначение:** Основной класс приложения, управляющий интерфейсом и логикой работы с задачами.

**Методы:**

1. **__init__(self):** Инициализирует окно, задает размеры, название и видимость фильтра. Настроен на создание пользовательского интерфейса.
2. **setup_ui(self):** Создает и настраивает элементы управления, включая кнопки, поля для поиска, фильтры по сложности и дедлайну, а также макет для отображения задач.
4. **create_headers(self):** Создает заголовки для каждой из категорий задач («Надо выполнить», «В процессе», «Выполнено») и применяет стиль.
5. **centered_layout(self, widget):** Помещает переданный виджет в центр горизонтального макета с отступами.
6. **create_add_button(self):** Создает кнопку для добавления новой задачи.
7. **toggle_filter(self):** Открывает или скрывает панель фильтрации задач.
8. **add_task(self):** Открывает окно для добавления новой задачи с полями для ввода информации.
9. **on_add_task(self, dialog, task_text_input, description_input, priority_input, deadline_input):** Обрабатывает добавление задачи, проверяя введенные данные и добавляя задачу в список, а также применяет цветовую кодировку по приоритету.
10. **filter_tasks_by_search(self):** Фильтрует задачи по введенному тексту в поле поиска.
11. **apply_filters(self):** Применяет фильтры по сложности и дедлайну к задачам.
12. **change_background_color** Позволяет пользователям настраивать внешний вид приложения, выбирая цвет фона.
13. **get_task_difficulty(self, item):** Определяет сложность задачи, анализируя ее текст.
14. **reset_filters(self)**: Сбрасывает все фильтры и показывает все задачи.
15. **show_all_tasks(self):** Открывает все задачи, сбрасывая любые фильтры.
# Общие функциональные особенности:

-  **Фильтрация задач:** Пользователи могут фильтровать задачи по сложности, дедлайну и поисковым запросам.
-  **Настройка базы данных:** Manager класс создает базу данных SQLite для хранения данных задач.
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
