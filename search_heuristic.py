import numpy as np
from collections import defaultdict
import sys
from task_parser import parseTask

#Merging dictionaries
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
    
#INPUTS
try:
    grid_param, blocked, roboSrc, tasks = parseTask(sys.argv[1])
except:
    grid_param, blocked, roboSrc, tasks = parseTask()
   
#roboSrc = [[(0, 0), (0, 8)],[(5, 9), (5, 5)],[(0, 0), (5, 5)]]
#tasks = [[(5, 0), (3, 12)],[(5, 0), (0, 5)],[(4, 6), (0, 5)]]
#blocked=[(2,1),(5,3),(4,10),(0,13),(2,15)]
nodeType = [0 for i in range(len(roboSrc))] + [1 for i in range(len(tasks))]
nodeData = roboSrc + tasks
INT_MIN = float('-inf')
INT_MAX = float('inf')
#grid_param=(6,17)   #howrizontal 6 units width 17 units

class robo:


    def __init__(self, blocked, roboSrc, tasks, nodeData, nodeType, grid_param):

        self.x , self.y = grid_param
        self.blocked=blocked
        self.dist=0
        self.graph = defaultdict(list)
        self.task=[]
        self.tasks=tasks
        self.perms=[]
        self.nodeData=nodeData
        self.nodeType=nodeType
        self.h, self.w = len(roboSrc), len(tasks)
        self.relMat = [[0 for j in range(self.h+self.w)] for i in range(self.h+self.w)]
        self.visited=[]
        self.Maxdepth=self.x*self.y
        self.spanMin = INT_MAX

    def getPos(self):
        return (self.x, self.y)

    def getTime(self):
        return self.time

    def goUP(self,A):
        return (A[0],A[1]-1)

    def goDOWN(self,A):
        return (A[0],A[1]+1)

    def goLEFT(self,A):
        return (A[0]-1,A[1])

    def goRIGHT(self,A):
        return (A[0]+1,A[1])

    #DEPTH LIMITED SEARCH WITH MAXIMUM DEPTH
    def DLS(self,src,target, maxDepth):

        if src == target :
            self.task.append(src)
            return True

        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0 : return False

        self.graph[src]=[]

        temp = self.goUP(src)
        self.visited
        if((temp not in self.visited) and (temp not in self.blocked) and (min(temp)>=0) and (temp[0]<self.x) and (temp[1]<self.y)):
            self.graph[src].append(temp)

        temp = self.goDOWN(src)
        if((temp not in self.visited) and (temp not in self.blocked) and (min(temp)>=0) and (temp[0]<self.x) and (temp[1]<self.y)):
            self.graph[src].append(temp)

        temp = self.goLEFT(src)
        if((temp not in self.visited) and (temp not in self.blocked) and (min(temp)>=0) and (temp[0]<self.x) and (temp[1]<self.y)):
            self.graph[src].append(temp)

        temp = self.goRIGHT(src)
        if((temp not in self.visited) and (temp not in self.blocked) and (min(temp)>=0) and (temp[0]<self.x) and (temp[1]<self.y)):
            self.graph[src].append(temp)

        if(len(self.graph[src])==0):
            return False

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[src]:
            self.visited.append(src)
            if(self.DLS(i,target,maxDepth-1)):
                self.task.append(src)
                return True
            self.visited.remove(src)

        return False

    # IDDFS/Itteretive deepening Search to search if target is reachable from v.
    # It uses recursive DLS()

    def IDDFS(self,src, target):
        # Repeatedly depth-limit search till the
        # maximum depth
        self.Maxdepth=self.x*self.y
        for i in range(self.Maxdepth):

            self.visited = []

            self.task=[]
            if (self.DLS(src, target, i)):

                return (i)
        return -1


    def distMinAtoB(self,src,dst):
        #RETURN -1 IF PATH IS NULL
        self.dist = self.IDDFS(src, dst)

        if(self.dist == -1):
            print('no possible path from '+str(src)+" to "+str(dst))

        return self.dist

    def Search(self):
        ## BUILD THE AGENT-TASK GRAPH
        for i in range(self.w+self.h):
            for j in range(self.w+self.h):
                robot, task = nodeType[i], nodeType[j]
                if robot == 0 and task == 1:
                    self.relMat[i][j] = self.distMinAtoB(self.nodeData[i][0], self.nodeData[j][0])
                elif robot == 1 and task == 1:
                    self.relMat[i][j] = self.distMinAtoB(self.nodeData[i][0], self.nodeData[i][1]) + self.distMinAtoB(self.nodeData[i][1], self.nodeData[j][0])
                elif robot == 1 and task == 0:
                    self.relMat[i][j] = self.distMinAtoB(self.nodeData[i][0], self.nodeData[i][1]) + self.distMinAtoB(self.nodeData[i][1], self.nodeData[j][1])
                else:
                    pass


    def allPossiblePaths(self, a, size, perms):
        if size == 1:
            perms.append([0] + a)
            return
        for i in range(size):
            self.allPossiblePaths(a, size-1, perms)

            if size & 1:
                a[0], a[size-1] = a[size-1], a[0]
            else:
                a[i], a[size-1] = a[size-1], a[i]

    def HamCycle(self):
        ### SINCE adjMat IS A COMPLETE GRAPH, THIS WILL SIMPLY GENERATE ALL
        ### POSSIBLE HAMILTONIAN PATHS
        perms = []
        self.allPossiblePaths(list(range(1, self.h+self.w, 1)), self.w + self.h - 1, perms)


        return perms

    def getMakespan(self, pattern):
        a = 0
        for i in range(len(pattern)):
            if self.nodeType[pattern[i]] == 0:
                a = i
                break

        minm = INT_MIN
        pattern = pattern[a:] + pattern[:a]
        t = 0

        for i in range(len(pattern) - 1):
            t += self.relMat[pattern[i]][pattern[i+1]]
            if self.nodeType[pattern[i + 1]] == 0:
                ## next item is an agent
                minm  = max(minm , t)
                t = 0
        t += self.relMat[pattern[-1]][pattern[0]]
        minm  = max(minm , t)
        return minm

    def makeSchedule(self, pattern):
        a = 0
        for i in range(len(pattern)):
            if self.nodeType[pattern[i]] == 0:
                a = i
                break
        pattern = pattern[a:] + pattern[:a]
        k, l = 0, 0
        assignments = dict()
        for i in range(len(pattern)):
            if (i+1 < len(pattern) and self.nodeType[pattern[i + 1]] == 0) or i + 1 == len(pattern):
                l = i
                assignments[pattern[k]] = [pattern[k+1: l+1][0]-self.h]

                k, l = i+1, i+1

        return assignments


    def Schedule(self):

        id = 0
        self.paths = self.HamCycle()
        self.Search()

        for i in range(len(self.paths)):
            self.pattern = self.paths[i]
            span = self.getMakespan(self.pattern)
            if span < self.spanMin:
                self.spanMin = span
                id = i

        temp = self.makeSchedule(self.paths[id])
        print("Approximate makespan: ", self.spanMin)
        print("Task Allocation Status\n")
        for i in temp:
            print("For robot: "+str(i) + " task assigned is  "+str(temp[i]))
            
            
r=robo(blocked, roboSrc, tasks, nodeData, nodeType, grid_param)
r.distMinAtoB((0,0),(4,6))
r.Schedule()
