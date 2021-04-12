from dearpygui.core import *
from dearpygui.simple import *
import time

def calculate_solution(task_data: list, cycle_time: float, priority: int):

    delete_item("Calculating solution...")

    with child(name="Work station table child", parent="Solution", height=370):
        add_text("Work station table:")
        add_separator()
        add_dummy(height=10)

        with managed_columns(name="Work station table", columns=5, border=True):
            add_text("Workstation number")
            add_text("Task assigned")
            add_text("Task time")
            add_text("Cumulative task time")
            add_text("Idle time at workstation")

            add_separator()
            add_separator()
            add_dummy()
            add_dummy()
            add_dummy()

    set_managed_column_width("Work station table", column=0, width=180)
    set_managed_column_width("Work station table", column=1, width=550)
    set_managed_column_width("Work station table", column=2, width=200)
    set_managed_column_width("Work station table", column=3, width=200)
    set_managed_column_width("Work station table", column=4, width=200)

    station = 0
    completed_task = []
    remaining_tasks = []
    total_time = 0

    for task in task_data:
        remaining_tasks.append(task[0])

    if priority == 0 or priority == 1:
        while remaining_tasks:

            for i in range(5):
                add_dummy(height=10, parent="Work station table")

            station += 1
            station_idle_time = cycle_time
            station_cumulative_time = 0
            station_eligible_tasks = {}

            while station_idle_time > 0:
                for task in task_data:
                    task_name = task[0]

                    if not task_name in completed_task:

                        task_precede = task[1].split(", ")
                        task_time = task[2]
                        task_type = task[3]

                        if task_type == 0:
                            if task_time <= station_idle_time:
                                station_eligible_tasks[task_name] = task_time

                        else:
                            flag = 1
                            for task in task_precede:
                                if not task in completed_task:
                                    flag = 0

                            if flag == 1:
                                if task_time <= station_idle_time:
                                    station_eligible_tasks[task_name] = task_time

                if not station_eligible_tasks:
                    break

                while station_eligible_tasks:

                    task = ""

                    if priority == 0:
                        task = max(station_eligible_tasks, key=station_eligible_tasks.get)

                    elif priority == 1:
                        task = min(station_eligible_tasks, key=station_eligible_tasks.get)

                    if station_eligible_tasks[task] <= station_idle_time:

                        station_cumulative_time += station_eligible_tasks[task]
                        station_idle_time -= station_eligible_tasks[task]

                        add_text(f"Station {station}", parent="Work station table")
                        add_text(task, parent="Work station table")
                        add_text(str(station_eligible_tasks[task]), parent="Work station table")
                        add_text(str(station_cumulative_time), parent="Work station table")
                        add_text(str(station_idle_time), parent="Work station table")
                        time.sleep(0.02)
                        total_time += station_eligible_tasks[task]

                        completed_task.append(task)
                        remaining_tasks.remove(task)

                    del station_eligible_tasks[task]

    efficiency = ((total_time/cycle_time)/station)*100

    add_dummy(height=10, parent="Solution")
    with child(name="Results", parent="Solution", width=500, height=160):
        add_text("Results:")
        add_separator()
        add_dummy(height=10)
        time.sleep(0.02)
        add_text(f"Cycle time = {cycle_time}")
        time.sleep(0.02)
        add_text(f"Theoretical number of stations = {round((total_time/cycle_time), 2)}")
        time.sleep(0.02)
        add_text(f"Actual number of stations = {station}")
        time.sleep(0.02)
        add_text(f"Efficiency of assembly line = {round(efficiency, 2)}%")
        time.sleep(0.02)
        add_text(f"Balance delay = {round(100 - efficiency, 2)}%")