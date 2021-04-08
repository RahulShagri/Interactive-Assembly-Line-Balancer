from dearpygui.core import *
from dearpygui.simple import *
import time
import math

class TaskHandler:
    def __init__(self, name: str, type:int):
        self.parent = "Assembly line"
        self.name = name
        self.type = type

        if type == 0:
            with node(name, parent=self.parent):
                with node_attribute(f"TaskAtt1##{name}", output=True):
                    add_input_float(f"Task time##{name}", width=120, min_value=0)

        elif type == 2:
            with node(name, parent=self.parent):
                with node_attribute(f"TaskAtt1##{name}"):
                    add_input_float(f"Task time##{name}", width=120, min_value=0)

        else:
            with node(name, parent=self.parent):
                with node_attribute(f"TaskAtt1##{name}", output=True):
                    add_input_float(f"Task time##{name}", width=120, min_value=0)

                with node_attribute(f"TaskAtt2##{name}", output=False):
                    pass

    def get_type(self):
        return self.type

    def set_task_variables(self, type: int, name: str):
        self.type = type

        delete_item(self.name, children_only=True)

        if type == 0:
            with node_attribute(f"TaskAtt1##{name}", output=True, parent=self.name):
                add_input_float(f"Task time##{name}", width=120, min_value=0)

        elif type == 2:
            with node_attribute(f"TaskAtt1##{name}", parent=self.name):
                add_input_float(f"Task time##{name}", width=120, min_value=0)

        else:
            with node_attribute(f"TaskAtt1##{name}", output=True, parent=self.name):
                add_input_float(f"Task time##{name}", width=120, min_value=0)

            with node_attribute(f"TaskAtt2##{name}", output=False, parent=self.name):
                pass

        self.name = name

    def get_task_name(self):
        return self.name

    def get_task_time(self):
        return round(get_value(f"Task time##{self.name}"), 3)

tasks = {}

def add_task():
    global tasks

    task_name = get_value("task name")

    if task_name:
        invalid_characters = ["\\", "/", ":", "?", "\"", "<", ">", "|"]

        for character in task_name:
            # Check for invalid characters in task name
            if character in invalid_characters:
                if not does_item_exist("Task name cannot include \\ / : ? \" < >  |"):
                    add_text("Task name cannot include \\ / : ? \" < >  |", color=[255, 0, 0],
                             parent="Add new task", before="addTaskDummy02")
                    delete_item("addTaskDummy02")
                return

            # Check if task name already exists
            if task_name in tasks.keys():
                if not does_item_exist("Task name already in use. Please enter a new name."):
                    add_text("Task name already in use. Please enter a new name.", color=[255, 0, 0],
                             parent="Add new task", before="addTaskDummy02")
                    delete_item("addTaskDummy02")
                return

        # Reset add task window
        set_value("task name", value='')

        if does_item_exist("Task name already in use. Please enter a new name."):
            delete_item("Task name already in use. Please enter a new name.")
            add_dummy(name="addTaskDummy02", height=20, before="Task type")

        if does_item_exist("Task name cannot include \\ / : ? \" < >  |"):
            delete_item("Task name cannot include \\ / : ? \" < >  |")
            add_dummy(name="addTaskDummy02", height=20, before="Task type")

        # Creating new task nodes
        tasks[task_name] = TaskHandler(name=task_name, type=get_value("Task type"))

        set_value("Task type", 1)
        close_popup("Add new task")

def delete_task():
    global tasks

    for node in get_selected_nodes(node_editor="Assembly line"):
        delete_item(node)
        del tasks[node]

def configure_task():
    global tasks

    try:
        node = get_selected_nodes(node_editor="Assembly line")[0]

        for task in tasks.keys():
            if task == node:
                if does_item_exist(f"Configure {node}"):
                    i = 0
                    while i <= 1:
                        x_pos = int((1 - math.pow((1 - i), 6)) * (250))
                        i += 0.01

                        configure_item(f"Configure {node}", x_pos=-x_pos)

                        configure_item("Interactive Task Window", x_pos=250 - x_pos, width=1365 - 250 + x_pos)

                        time.sleep(0.004)

                    delete_item(f"Configure {node}")

                    return

            elif does_item_exist(f"Configure {task}"):

                i = 0
                while i <= 1:
                    x_pos = int((1 - math.pow((1 - i), 6)) * (250))
                    i += 0.01

                    configure_item(f"Configure {task}", x_pos=-x_pos)

                    configure_item("Interactive Task Window", x_pos=250 - x_pos, width=1365 - 250 + x_pos)

                    time.sleep(0.004)

                delete_item(f"Configure {task}")

        if does_item_exist("Finalize tasks"):
            close_finalize_window()

        with window(name=f"Configure {node}", x_pos=-250, y_pos=100, no_collapse=True, no_resize=True, no_move=True, no_close=True, width=250, height=600): # width 250
            set_item_style_var(item=f"Configure {node}", style=mvGuiStyleVar_WindowPadding, value=[10, 10])

            add_dummy(height=10)
            add_input_text(name=f"task name##{node}", label="    Task name", hint="Task name", width=140, default_value=node)
            add_dummy(name="configureTaskDummy01", height=20)
            add_radio_button(name=f"Task type##{node}", items=["Entry point task", "Intermediate task", "Exit point task"], default_value=tasks[node].get_type())
            add_dummy(name="configureTaskDummy03", height=20)
            add_button(f"Update##UpdateTask??{node}", width=235, callback=update_task)
            add_dummy(height=5)
            add_button(f"Cancel##UpdateTask??{node}", width=235, callback=close_popups)

        i = 0
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 6)) * (250))
            i += 0.01

            configure_item(f"Configure {node}", x_pos=-250 + x_pos)

            configure_item("Interactive Task Window", x_pos=x_pos, width=1365-x_pos)

            time.sleep(0.004)

    except:
        pass

def update_task(sender):
    global tasks

    node = sender[20:]
    task_name = get_value(f"task name##{node}")

    if task_name:
        if task_name != node:
            invalid_characters = ["\\", "/", ":", "?", "\"", "<", ">", "|"]

            for character in task_name:
                # Check for invalid characters in task name
                if character in invalid_characters:
                    if not does_item_exist("Task name cannot include \\ / : ? \" < >  |"):
                        add_text("Task name cannot include \\ / : ? \" < >  |", color=[255, 0, 0],
                                 parent=f"Configure {node}", before="configureTaskDummy01", wrap=250)
                    return

                # Check if task name already exists
                elif task_name in tasks.keys():
                    if not does_item_exist("Task name already in use. Please enter a new name."):
                        add_text("Task name already in use. Please enter a new name.", color=[255, 0, 0],
                                 parent=f"Configure {node}", before="configureTaskDummy01")
                    return

        if does_item_exist("Task name cannot include \\ / : ? \" < >  |"):
            delete_item("Task name cannot include \\ / : ? \" < >  |")
        if does_item_exist("Task name already in use. Please enter a new name."):
            delete_item("Task name already in use. Please enter a new name.")

        task_type = get_value(f"Task type##{node}")

        if task_type == 0:
            configure_item(f"TaskAtt1##{node}", output=True)
            if does_item_exist(f"TaskAtt2##{node}"):
                delete_item(f"TaskAtt2##{node}")

        elif task_type == 1:
            configure_item(f"TaskAtt1##{node}", output=True)
            if not does_item_exist(f"TaskAtt2##{node}"):
                with node_attribute(f"TaskAtt2##{node}", output=False, parent=node):
                    pass

        else:
            configure_item(f"TaskAtt1##{node}", output=False)
            if does_item_exist(f"TaskAtt2##{node}"):
                delete_item(f"TaskAtt2##{node}")

        tasks[node].set_task_variables(type=task_type, name=task_name)
        configure_item(node, name=task_name, label=task_name)
        # Replacing name in tasks dictionary
        if task_name != node:
            tasks[task_name] = tasks[node]
            del tasks[node]

        i = 0
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 6)) * (250))
            i += 0.01

            configure_item(f"Configure {node}", x_pos=-x_pos)

            configure_item("Interactive Task Window", x_pos=250 - x_pos, width=1365 - 250 + x_pos)

            time.sleep(0.004)

        delete_item(f"Configure {node}")

def finalize_tasks():

    for task in tasks.keys():
        if does_item_exist(f"Configure {task}"):
            i = 0
            while i <= 1:
                x_pos = int((1 - math.pow((1 - i), 6)) * (250))
                i += 0.01

                configure_item(f"Configure {task}", x_pos=-x_pos)

                configure_item("Interactive Task Window", x_pos=250 - x_pos, width=1365 - 250 + x_pos)

                time.sleep(0.004)

            delete_item(f"Configure {task}")

    if does_item_exist("Finalize tasks"):
        close_finalize_window()
        return

    with window(name="Finalize tasks", x_pos=-300, y_pos=100, no_collapse=True, no_resize=True, no_move=True, no_close=True, width=1365, height=600): # width 250
        set_item_style_var(item="Finalize tasks", style=mvGuiStyleVar_WindowPadding, value=[10, 10])

    refresh_data()

    open_finalize_window()

def refresh_data():
    global tasks

    entry_tasks = []
    exit_tasks = []
    intermediates = []
    links = get_links("Assembly line")

    for task in tasks.values():
        if task.get_type() == 0:
            entry_tasks.append(task.get_task_name())

        elif task.get_type() == 2:
            exit_tasks.append(task.get_task_name())

        else:
            intermediates.append(task.get_task_name())

    delete_item("Finalize tasks", children_only=True)
    add_dummy(height=5, parent="Finalize tasks")

    error_flag = 0

    if tasks:
        if not entry_tasks:
            add_text("No entry points found. Please add at least one entry point.", wrap=1100, parent="Finalize tasks", color=[255, 0, 0])
            add_dummy(height=10, parent="Finalize tasks")
            error_flag = 1

        elif not exit_tasks:
            add_text("No exit points found. Please add at least one exit point.", wrap=1100, parent="Finalize tasks", color=[255, 0, 0])
            add_dummy(height=10, parent="Finalize tasks")
            error_flag = 1

        elif links:
            not_connected_tasks = ""
            for task in tasks:
                flag = 0
                for link in links:

                    if link[0][10:] == task:
                        flag = 1
                        break

                    if link[1][10:] == task:
                        flag = 1
                        break

                if flag == 0:
                    not_connected_tasks += f", {task}"

            not_connected_tasks = not_connected_tasks[2:]

            if not_connected_tasks:
                add_text(f"Please connect all the tasks added in the assembly. The following tasks are not connected to any other tasks:\n\n{not_connected_tasks}", wrap=1100, parent="Finalize tasks", color=[255, 0, 0])
                add_dummy(height=10, parent="Finalize tasks")
                error_flag = 1

            else:
                not_fully_connected_tasks = ""
                for task in intermediates:
                    input_flag = 0
                    output_flag = 0
                    for link in links:
                        if link[0][10:] == task:
                            input_flag = 1

                        if link[1][10:] == task:
                            output_flag = 1

                    if input_flag == 0 or output_flag == 0:
                        not_fully_connected_tasks += f", {task}"

                if not_fully_connected_tasks:
                    not_fully_connected_tasks = not_fully_connected_tasks[2:]
                    add_text(
                        f"Please connect both inputs and outputs of all intermediate tasks. The following intermediate tasks are not fully connected:\n\n{not_fully_connected_tasks}",
                        wrap=1100, parent="Finalize tasks", color=[255, 0, 0])
                    add_dummy(height=10, parent="Finalize tasks")
                    error_flag = 1


        elif not links:
            add_text("No links found. Please connect the tasks.", wrap=1100, parent="Finalize tasks", color=[255, 0, 0])
            add_dummy(height=10, parent="Finalize tasks")
            error_flag = 1

    else:
        add_text("No tasks found. Please add some tasks", wrap=1100, parent="Finalize tasks", color=[255,0,0])
        add_dummy(height=10, parent="Finalize tasks")
        error_flag = 1

    if error_flag == 0:
        add_text("All data have been verified. No errors were found.", wrap=1100, parent="Finalize tasks",
                 color=[0, 255, 0])
        add_dummy(height=10, parent="Finalize tasks")

    with child(name="Precedence table child window", parent="Finalize tasks", height=290):
        add_text("Precedence table:")
        add_dummy(height=10)
        add_table(name="Precedence table", headers=["Task", "Immediate\nPredecessor", "Task time"])

    add_dummy(height=2, parent="Finalize tasks")

    with child(name="Assembly line parameters", parent="Finalize tasks", height=215):
        add_text("Assembly line parameters:")
        add_separator()
        add_dummy(height=10)
        with child(name="Variables", height=160, width=800):
            add_input_float(name="Cycle time", default_value=0.0, min_value=0.0, step=1.0, width=150, callback=refresh_assembly_parameters)
            add_same_line(spacing=10)
            add_text("[Leave at zero to assume equal to maximum task time.]", color=[170, 170, 170, 255])
            add_dummy(height=20)
            add_text("Time for producing one unit of product = ")
            add_same_line(spacing=1)
            add_text("0", source="time for one unit")
            add_same_line(spacing=10)
            add_text("[Value automatically calculated by adding all the task times.]", color=[170, 170, 170, 255])
            add_dummy(height=20)
            add_text("Theoretical minimum number of stations = ")
            add_same_line(spacing=1)
            add_text("0", source="theoretical number of stations")
            add_same_line(spacing=20)
            add_text("[Value automatically calculated by dividing total time by cycle time.]", color=[170, 170, 170, 255])

        add_same_line()

        with child(name="Priority rules child", height=160, width=250):
            add_text("Select priority rule:")
            add_dummy(height=2)
            add_radio_button(name="Priority rule", items=["Longest work element", "Shortest work element", "Most followers", "Fewest followers"])

        add_same_line()

        add_button(name="Go back to assembly line diagram", width=265, callback=close_finalize_window)

    refresh_assembly_parameters()

    for entry_task in entry_tasks:
        add_row("Precedence table", row=[entry_task, "NULL", tasks[entry_task].get_task_time()])

    for task in intermediates:
        immediate_predecessor = ""
        for link in links:
            if link[1][10:] == task:
                immediate_predecessor += f", {link[0][10:]}"

        immediate_predecessor = immediate_predecessor[2:]

        add_row("Precedence table", row=[task, immediate_predecessor, tasks[task].get_task_time()])

    for task in exit_tasks:
        immediate_predecessor = ""
        for link in links:
            if link[1][10:] == task:
                immediate_predecessor += f", {link[0][10:]}"

        immediate_predecessor = immediate_predecessor[2:]

        add_row("Precedence table", row=[task, immediate_predecessor, tasks[task].get_task_time()])

def close_finalize_window():
    configure_item("Interactive Task Window", show=True)
    i = 0
    while i <= 1:
        x_pos = int((1 - math.pow((1 - i), 6)) * (1365))
        i += 0.01

        configure_item("Finalize tasks", x_pos=-x_pos)

        configure_item("Interactive Task Window", x_pos=1365 - x_pos)

        time.sleep(0.004)

    delete_item("Finalize tasks")

def open_finalize_window():
    i = 0
    while i <= 1:
        x_pos = int((1 - math.pow((1 - i), 6)) * (1365))
        i += 0.01

        configure_item("Finalize tasks", x_pos=-1365 + x_pos)

        configure_item("Interactive Task Window", x_pos=x_pos)

        time.sleep(0.004)

    configure_item("Interactive Task Window", show=False)

def refresh_assembly_parameters():
    total_time = 0
    task_times = []

    for task in tasks:
        total_time += tasks[task].get_task_time()
        task_times.append(tasks[task].get_task_time())

    set_value("time for one unit", value=total_time)

    if get_value("Cycle time") == 0:
        if task_times:
            if max(task_times)!= 0:
                set_value("theoretical number of stations", value=str(round((total_time / max(task_times)), 2)))


    else:
        set_value("theoretical number of stations", value=str(round((total_time / get_value("Cycle time")), 2)))

def close_popups(sender):
    if sender == "Cancel##AddTask":

        set_value("task name", value='')

        if does_item_exist("Task name already in use. Please enter a new name."):
            delete_item("Task name already in use. Please enter a new name.")
            add_dummy(name="addTaskDummy01", height=20, before="Task type")

        elif does_item_exist("Task name cannot include \\ / : ? \" < >  |"):
            delete_item("Task name cannot include \\ / : ? \" < >  |")
            add_dummy(name="addTaskDummy02", height=20, before="Task type")

        set_value("Task type", 1)

        close_popup("Add new task")

    elif sender[:20] == "Cancel##UpdateTask??":
        node = sender[20:]

        i = 0
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 6)) * (250))
            i += 0.01

            configure_item(f"Configure {node}", x_pos=-x_pos)

            configure_item("Interactive Task Window", x_pos=250 - x_pos, width=1365 - 250 + x_pos)

            time.sleep(0.004)

        delete_item(f"Configure {node}")