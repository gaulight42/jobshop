#!/usr/bin/env python2.7
import yaml
import argparse

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
        self.machine = None # an instance of Machine
        self.running = 0
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
        self.scheduleSteps = [] # list of (taskName,startTime,endTime,machineName,cores)
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
        """Driver of the scheduling algorithm which starts with all
        the tasks sorted by length of longest path to a leaf from that task,
        the root tasks are marked as ready,
        and the machines sorted in ascending order by number of available cores.
        Schedule as many ready tasks in the list (put on tasksRunning list)
        Then a loop is executed until all the tasks are finished and removed from the list.
        The loop consists of the following steps...
          pop the first task, tf, off tasksRunning list (which is the next to finish)
          remove it from the tasks list
          set currentTime to tf.finishTime
          free up cores on machine that is running the task
          take tf off the dependencies of its children and mark them as runable if there are no more dependencies
          schedule as many ready tasks in the list
          """
        self.scheduleReadyTasksOnAvailableMachines()
        while (self.tasks != []):
            tf = self.tasksRunning.pop(0)
            self.tasks.remove(tf)
            self.currentTime = tf.finishTime
            tf.machine.coresAvailable += tf.coresRequired
            for k in tf.childTasks:
                k.parentTasks.remove(tf)
                if not k.parentTasks: k.readyToRun = 1
            self.scheduleReadyTasksOnAvailableMachines()



    def scheduleReadyTasksOnAvailableMachines(self):
        """Schedule all the ready tasks that can be scheduled.
        loop through tasks list looking for ready tasks
        for each ready task run it if there is an available machine
          update the task, the machine, machines, tasksRunning, scheduleSteps
        """
        for t in self.tasks:
            if (t.readyToRun and not t.running and self.findMachine(t.coresRequired)):
                t.running = 1
                t.machine = self.findMachine(t.coresRequired)
                t.startTime = self.currentTime
                t.finishTime = t.startTime + t.executionTime
                t.machine.coresAvailable -= t.coresRequired
                self.machines.sort(key=lambda m: m.coresAvailable)
                self.tasksRunning.append(t)
                self.tasksRunning.sort(key=lambda s: s.finishTime)
                self.scheduleSteps.append((t.name,t.startTime,t.finishTime,
                t.machine.name,t.coresRequired))

    def findMachine(self,crequired):
        i = (m for m in self.machines if m.coresAvailable >= crequired)
        return next(i,None)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("taskFilename", help="YAML task filename")
    parser.add_argument("machineFilename", help="YAML machine filename")
    args = parser.parse_args()

    s = Scheduler()
    s.schedule(args.taskFilename,args.machineFilename)
    #print s.machines
    #print s.tasks
    print s.scheduleSteps


