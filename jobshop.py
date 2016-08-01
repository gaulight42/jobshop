#!/usr/bin/env python2.7
import yaml

class Task:
    """Hold information about a task"""
    def __init__(self,n,coresR,eTime,pTasks):
        self.name = n
        self.coresRequired = coresR
        self.executionTime = eTime
        self.parentTasks   = pTasks # a list of strings
        self.childTasks = [] # a list of Task objects
        self.maxPath = 0
        self.readyToRun = 0
        self.startTime = 0
        self.finishTime = 0

    def leafP(self):
        return self.childTasks

    def rootP(self):
        return self.parentTasks

    def __repr__(self):
        return "<Task %s, coresR %s, eTime %s, pTasks %s, cTasks %s>" % (self.name,self.coresRequired,self.executionTime,[t.name for t in self.parentTasks],[t.name for t in self.childTasks])


class Machine:
    """Hold information about a machine"""
    def __init__(self,n,c):
        self.name = n
        self.cores = c
        self.coresAvailable = self.cores

    def __repr__(self):
        return "<Machine: name: %s, cores: %s, available %s>" % (self.name, self.cores, self.coresAvailable)

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
        self.tasksDict = {} # enable fast access based on name
        self.Schedule = [] # list of (task,startTime,endTime,machine,cores)

    def schedule(self,tasksfile,machinesfile):
        """Outermost function that reads in task and machines YAML files and
        then fires off the scheduling algorithm"""
        self.machines = self.createMachines(machinesfile)
        self.machines.sort(key=lambda m: m.coresAvailable)

        self.tasks = self.createTasks(tasksfile)


    def createMachines(self,filename):
        """create machines from YAML file to be resources for a schedule"""
        with open(filename, 'r') as stream:
            try:
                mData = yaml.load(stream)
                return [Machine(n,c) for n, c in mData.items()]
            except yaml.YAMLError as exc:
                print(exc)

    def createTasks(self,filename):
        """create tasks from YAML file to be scheduled"""
        with open(filename, 'r') as stream:
            try:
                tData = yaml.load(stream)
                ts = [self.cTask(n,attrs) for n,attrs in tData.items()]
                self.createChildrenPointers(ts)
                return ts
            except yaml.YAMLError as exc:
                print(exc)
    def cTask(self,name,ats):
        """helper function of createTasks: does one task"""
        t = Task(name,ats['cores_required'],ats['execution_time'],ats['parent_tasks'].keys())
        self.tasksDict[name] = t
        return t
    def createChildrenPointers(self,tasks):
        """file in the children field for each task"""
        for t in tasks:
            for p in t.parentTasks:
                self.tasksDict[p].childTasks.append(t)
            newParents = []
            for p in t.parentTasks:
                newParents.append(self.tasksDict[p])
            t.parentTasks = newParents



if __name__ == "__main__":
    s = Scheduler()
    s.schedule("jobshop/examples/task1.yaml","jobshop/examples/machines1.yaml")
    print s.machines
    print s.tasks


