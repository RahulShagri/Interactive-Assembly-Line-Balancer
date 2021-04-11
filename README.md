# Interactive Assembly Line Balancer

A python based GUI to add multiple tasks and link them together to create and balance an assembly line by assigning tasks to various workstations so as to achieve the desired output rate with the smallest number of workstations according to the longest or shortest work element rule.

This helps create well-balanced workloads for each workstation and minimizes bottlenecks.

<h3>Demonstration</h3>

![Intro](resources/demo.gif)

<h3>Instructions</h3>

1. Make sure you have Python 3.9 installed and working
   
2. Clone the repo:

```git clone https://github.com/RahulShagri/Interactive-Assembly-Line-Balancer.git```

3. Install prerequisites using pip, preferably in a virtual environment:

```pip install -r requirements.txt```

4. Run the <i>assembly_line_balancer.py</i> file to start the application

5. Click on the "Add a new task" button to add a new task. Assign a unique name to the task and set the type

6. Adjust the task time and link each task in the line to each other to complete the assembly line. You can choose to delete or update any of the task details at any point

7. Click on the Finalize button to open up the precedence table. This table lists all the different tasks that have added, any immediate predecessors detected, and their respective tasks times

8. Make sure you do not see any errors on the top of the window. If you do, please resolve it before proceeding

9. Set the cycle time (or leave blank if you want the cycle time to be equal to the maximum task time in the line). Check the total time for producing one unit of product, and the minimum theoretical number of tasks

10. Select an appropriate priority rule and click on the Calculate button

11. In the Solution window, you can see that all the tasks have been assigned a workstation according to the priority rule you selected

12. In the results box below, you can view the actual number of workstations, efficiency of the line if these stations were introduced, and the balance delay

13. If you wish to save the assembly line, you can go to File > Save assembly line. Similarly, you can open an assembly line by going to File > Open assembly line*

* Due to the limitations of the GUI framework being used, the tasks are added one over each other after the assembly line is opened. You need to drag all the tasks to their respective places for a better view of the line