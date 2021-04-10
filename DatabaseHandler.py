import sqlite3
import os
import shutil

def create_database():

    if os.path.exists("_temp_.db"):
        os.remove("_temp_.db")

    conn = sqlite3.connect("_temp_.db")

def create_table():
    conn = sqlite3.connect("_temp_.db")
    c = conn.cursor()

    c.execute(f"""CREATE TABLE TaskData (
                        task_name text,
                        immediate_predecessor text,
                        task_time real,
                        task_type int)""")

    c.execute(f"""CREATE TABLE AssemblyLineData (
                            cycle_time real,
                            priority integer)""")

    c.execute(f"""INSERT INTO AssemblyLineData (cycle_time, priority)
                    VALUES (?, ?)""", (0, 0))

    conn.commit()
    conn.close()

def save_all(file_path: str):
    original = os.path.abspath("_temp_.db")
    target = file_path
    shutil.copyfile(original, target)

def get_all_tasks():
    conn = sqlite3.connect("_temp_.db")
    c = conn.cursor()

    c.execute(f"SELECT task_name, immediate_predecessor, task_time, task_type FROM TaskData")
    task_data = c.fetchall()

    conn.commit()
    conn.close()

    return task_data

def write_task(task_name: str, predecessor: str, task_time:float, task_type: int):
    conn = sqlite3.connect("_temp_.db")
    c = conn.cursor()

    c.execute(f"""INSERT INTO TaskData (task_name, immediate_predecessor, task_time, task_type)
                VALUES (?, ?, ?, ?)""", (task_name, predecessor, task_time, task_type))

    conn.commit()
    conn.close()

def update_assembly_parameters(cycle_time: float, priority: int):
    conn = sqlite3.connect("_temp_.db")
    c = conn.cursor()

    c.execute(f"""UPDATE AssemblyLineData SET cycle_time = ?, priority = ?""", (cycle_time, priority))

    conn.commit()
    conn.close()

def get_assembly_parameters():
    conn = sqlite3.connect("_temp_.db")
    c = conn.cursor()

    c.execute(f"SELECT cycle_time, priority FROM AssemblyLineData")
    assembly_parameters = c.fetchall()

    conn.commit()
    conn.close()

    return assembly_parameters