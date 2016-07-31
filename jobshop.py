#!/usr/bin/env python2.7
import yaml

class Task:
    """Hold information about a task"""
    def __init__(self):
        self.coresRequired = 0
        self.executionTime = 0
        self.parentTasks = ()
        self.childTasks = ()
        self.maxPath = 0
        self.readyToRun = 0
        self.startTime = 0
        self.finishTime = 0

    def leafP(self):
        return self.childTasks

    def rootP(self):
        return self.parentTasks

class Machine:
    """Hold information about a machine"""
    def __init__(self,n,c):
        self.name = n
        self.cores = c
        self.coresAvailable = self.cores

class SchedState:
    """Hold information about a state where a schedule is a list of such states"""
    def __init__(self):
        self.time = 0
        self.priorityList = [] #tasks ordered by priority based on critical path algorithm
        self.tasksRunning = [] # list of tasks sorted by finishtime
        self.machines     = [] # list of Machine objects sorted by coresAvailable in ascending order

    def setupStartState(self,priorityList,machines):
        pass

    def nextState(self,currentState):
        pass


class Scheduler:
    """Outer class that holds all the bits of the problem, intermediate
    states, and relevant functions"""
    def __init__(self):
        self.machines = []
        self.tasks = []
        self.Schedule = [] # list of (task,startTime,endTime,machine,cores)

    def schedule(self,tasksfile,machinesfile):
        """Outermost function that reads in task and machines YAML files and
        then fires off the scheduling algorithm"""
        self.machines = self.createMachines(machinesfile)


    def createMachines(self,filename):
        with open(filename, 'r') as stream:
            try:
                mData = yaml.load(stream)
                return [Machine(n,c) for n, c in mData.items()]
            except yaml.YAMLError as exc:
                print(exc)




if __name__ == "__main__":
    s = Scheduler()
    s.schedule("jobshop/examples/task1.yaml","jobshop/examples/machines1.yaml")
    print ["%s-%s" % (m.name,m.cores) for m in s.machines]


