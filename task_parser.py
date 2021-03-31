def parseTask(filename='demo.task'):
    f = open(filename, 'r')

    M, N = [int(item) for item in f.readline().strip().split(" ")]
    
    
    agentsData = []
    taskData = []
    blocked = []
        
    m = int(f.readline().strip())
    
    for i in range(m):
        row = [int(item) for item in f.readline().strip().split()]
        agentsData.append([(row[0],row[1]), (row[2],row[3])])
        
    n = int(f.readline().strip())
    
    for i in range(n):
        row = [int(item) for item in f.readline().strip().split()]
        taskData.append([(row[0],row[1]), (row[2],row[3])])
        
    o = int(f.readline().strip())
    
    for i in range(o):
        row = [int(item) for item in f.readline().strip().split()]
        blocked.append((row[0],row[1]))
        
    return (M, N), blocked, agentsData, taskData
