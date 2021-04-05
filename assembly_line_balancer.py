from dearpygui.core import *
from dearpygui.simple import *
import webbrowser
from TaskHandlerAPI import *

# function to open up website
def open_website(sender, data):
    webbrowser.open(data)

with window("Main"):
    # Styling
    set_theme(theme="Grey")
    set_main_window_title("Assembly Line Balancer")
    set_main_window_pos(x=0, y=0)
    set_main_window_size(width=1370, height=740)
    add_additional_font("fonts/glacial_font.otf", 19)
    set_style_window_border_size(0.0)
    set_style_window_title_align(0.5, 0.5)
    set_style_window_rounding(5.0)
    set_style_frame_rounding(5.0)

    # Colour
    set_theme_item(mvGuiCol_TextDisabled, 143, 143, 143, 255)

    # adding a menu bar
    with menu_bar("Main menu bar"):
        with menu("File"):
            add_menu_item("Save assembly line")
            add_menu_item("Open assembly line")
        with menu("Help"):
            add_menu_item("About", callback=open_website, callback_data="https://github.com/RahulShagri/Assembly-Line-Balancer")

with window(name="Toolbar", no_title_bar=True, no_resize=True, no_close=True, no_collapse=True, no_move=True, x_pos=0, y_pos=30, autosize=True):
    add_image_button(name="Add task button", value="icons/add_task_button.png", width=55, height=55, tip="Add a new task")

    with popup(popupparent="Add task button", name="Add new task", mousebutton=mvMouseButton_Left, modal=True):
        set_item_style_var(item="Add new task", style=mvGuiStyleVar_WindowPadding, value=[10, 10])
        set_item_color(item="Add new task", style=mvGuiCol_PopupBg, color=[64,64,64,180])

        add_dummy(name="addTaskDummy01", height=10)
        add_input_text(name="task name", label="    Enter task name", hint="Task name", width=250, on_enter=True, callback=add_task, callback_data=lambda: add_task)
        add_dummy(name="addTaskDummy02", height=20)
        add_radio_button(name="Task type", items=["Entry point task", "Intermediate task", "Exit point task"], default_value=1)
        add_dummy(name="addTaskDummy03", height=20)
        add_button("Add##AddTask", width=220, callback=add_task, callback_data=lambda: add_task)
        add_same_line(spacing=10)
        add_button("Cancel##AddTask", width=220, callback=close_popups)

    add_same_line()
    add_image_button(name="Delete task button", value="icons/delete_task_button.png", width=55, height=55, tip="Delete selected task", callback=delete_task)
    add_same_line()
    add_image_button(name="Configure task button", value="icons/configure_task_button.png", width=55, height=55, tip="Configure selected task", callback=configure_task)
    add_same_line()
    add_image_button(name="Finalize task button", value="icons/finalize_task_button.png", width=55, height=55, tip="Finalize all tasks and setup\nassembly line parameters", callback=finalize_tasks)
    add_same_line(spacing=35)
    add_image_button(name="Calculate button", value="icons/calculate_button.png", width=171, height=55, tip="Calculate solution")

with window("Interactive Task Window", no_title_bar=True, no_resize=True, no_close=True, no_collapse=True, no_move=True, x_pos=0, y_pos=100, width=1365, height=600):
     with tab_bar(name="Main tab bar"):
        with tab(name="Assembly line diagram"):
            with node_editor("Assembly line"):
                pass

        with tab(name="Solutions"):
            add_text("Solution here!")


# Start app
start_dearpygui(primary_window="Main")