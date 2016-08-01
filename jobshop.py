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
        self.startTime = 0
        self.finishTime = 0
        if self.rootP():
            self.readyToRun = 1
        else:
            self.readyToRun = 0

    def leafP(self):
        return not self.childTasks

    def rootP(self):
        return not self.parentTasks

    def __repr__(self):
        return "<Task %s, coresR %s, eTime %s, pTasks %s, cTasks %s, mp %s>" % (
        self.name,self.coresRequired,self.executionTime,
        [t.name for t in self.parentTasks],
        [t.name for t in self.childTasks],
        self.maxPath)


class Machine:
    """Hold information about a machine"""
    def __init__(self,n,c):
        self.name = n
        self.cores = c
        self.coresAvailable = self.cores

    def __repr__(self):
        return "<Machine: name: %s, cores: %s, available %s>" % (self.name, self.cores, self.coresAvailable)

class Scheduler:
    """Outer class that holds all the bits of the problem, intermediate
    states, and relevant functions"""
    def __init__(self):
        self.machines = [] # sorted by coresAvailable, least first
        self.tasks = [] # sorted by maxPath, longest first
        self.tasksRunning = [] # list of tasks sorted by finishtime
        self.tasksDict = {} # enable fast access based on name
        self.scheduleSteps = [] # list of (task,startTime,endTime,machine,cores)
        self.currentTime = 0

    def schedule(self,tasksfile,machinesfile):
        """Outermost function that reads in task and machines YAML files and
        then fires off the scheduling algorithm; results go in scheduleSteps"""
        self.machines = self.createMachines(machinesfile)
        self.machines.sort(key=lambda m: m.coresAvailable)

        self.tasks = self.createTasks(tasksfile)
        self.backflow(self.tasks)
        self.tasks.sort(key=lambda t: t.maxPath)
        self.tasks.reverse() # the tasks are now in a priority list based on length of critical path

        self.createSchedule()


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

    def backflow(self,tasks):
        """implements the backflow algorithm which labels each task with the
        longest path from it to a leaf"""
        for t in tasks:
            if t.leafP():
                t.maxPath = t.executionTime
                self.bf(t)
    def bf(self,task):
        """recursive part of backflow implementation"""
        if task.rootP():
            return
        else:
            for p in task.parentTasks:
                m = task.maxPath + p.executionTime
                if m > p.maxPath:
                    p.maxPath = m
                self.bf(p)

    def createSchedule(self):
        """check if ready to run; some sort of while loop that ends when task list is empty"""
        pass


if __name__ == "__main__":
    s = Scheduler()
    s.schedule("jobshop/examples/task1.yaml","jobshop/examples/machines1.yaml")
    print s.machines
    print s.tasks
    print s.scheduleSteps


