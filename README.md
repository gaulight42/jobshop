# jobshop
Job scheduling with precedent
Marc Light
8/2/2016

Characterization of the task: It is a job shop scheduling task where jobs have precedence constraints and jobs and machines have mutual constraints.  In addition, it is an offline makespan minimization optimization problem.  Finally, it is NP complete.

General approach: The approach I take is to build a greedy algorithm based on working on tasks that have the longest chain of dependencies to a leaf of DAG (where each link length is the task execution time).  More specifically, I built a critical path-based priority list algorithm extended to handle machine size constraints.  Used the backflow algorithm to calculate these lengths.  A task is scheduled on the machine with the smallest number of cores available that can accommodate the task.  This algorithm will produce suboptimal results both because of the greedy task choice and because of the greedy machine choice.

The backflow algorithm is linear in the number of tasks.  The machine-size constrained priority list algorithm is O(M*T^2) where T is the number of tasks and M is the number of machines.

Coding decisions: There are objects for Tasks, Machines, and the Scheduler.  The state of the scheduling algorithm is spread out over all of these classes.  If I had time to refactor, I would pull all the state aspects into the scheduler class.  Then the Tasks and Machines would be unchanged by the scheduling algorithm, making debugging easier and would allow multiple scheduling algorithms to work on the same set of tasks. The primary function is createSchedule.

Note that this is my first Python program.  I have been wanting to learn Python and this task was a great forcing function...  I using a Chromebook, pythonanywhere.com, and github to do my development.  I need to use a unit testing module to make it easy to write and run tests for functions.

Effort: I spent 4 hours thinking about the algorithm and the general architecture of the code, 8 hours doing the coding, and an hour writing this document.  If I were a more experienced Python coder, I would have been able to half the coding time.

Further work: In addition to the refactoring mentioned above, I would ask for a sample of actual scheduling tasks and look for patterns and/or constraints that could be exploited to make more optimal decisions.  Generally, focus on understanding where the greedy decisions result in suboptimal solutions.  I would also look into the job scheduling literature further.  Finally, I would make a suite of tasks and extend the code to spit out a total time to make comparisons between different algorithms easier.  The code also needs to be hardened with exception handling, checks for ill-defined tasks, and machines, etc.

4. How to run: The code is written for the Python 2.7 interpreter.  To run it execute

python jobshop.py tasks.yaml machines.yaml

where the yaml files include their paths.  The output is a list of schedule steps, each in the following form:

(taskName,startTime,endTime,machineName,cores)

Two yaml task files are provided: task1.yaml and task2.yaml

