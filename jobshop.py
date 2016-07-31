#!/usr/bin/env python2.7
import yaml

class Task:
    """Hold information about a task"""
    def __init__(self):
        coresRequired = 0
        executionTime = 0
        parentTasks = ()
        childTasks = ()
        maxPath = 0
        readyToRun = 0
        startTime = 0
        finishTime = 0

    def leafP(self):
        return childTasks

    def rootP(self):
        return parentTasks

class Machine:
    """Hold information about a machine"""
    def __init__(self,c):
        name = ""
        cores = c
        coresAvailable = 0

class SchedState:
    """Hold information about a state where a schedule is a list of such states"""
    def __init__(self):
        time = 0
        priorityList = [] #tasks ordered by priority based on critical path algorithm
        tasksRunning = [] # list of tasks sorted by finishtime
        machines     = [] # list of Machine objects sorted by coresAvailable in ascending order

    def setupStartState(self,priorityList,machines):
        pass

    def nextState(self,currentState):
        pass


class Scheduler:
    """Outer class that holds all the bits of the problem, intermediate
    states, and relevant functions"""
    def __init__(self):
        machines = []
        tasks = []
        Schedule = [] # list of (task,startTime,endTime,machine,cores)

    def schedule(self,tasksfile,machinesfile):
        """Outermost function that reads in task and machines YAML files and
        then fires off the scheduling algorithm"""
        with open(tasksfile, 'r') as stream:
            try:
             print(yaml.load(stream))
            except yaml.YAMLError as exc:
               print(exc)




if __name__ == "__main__":
    s = Scheduler()
    s.schedule("jobshop/examples/task1.yaml","jobshop/examples/machine1.yaml")


