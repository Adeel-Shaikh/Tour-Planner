import pandas as pd
import numpy as np
class Graph:
    def __init__(self,edges):
        self.edges=edges
        self.no_of_edges=len(self.edges)
        matrix=pd.read_csv('travel_matrix.csv')
        self.data={}
        for i in self.edges:
            row=[]
            for j in self.edges:
                row.append((j,matrix.iloc[i][j+1]))
            self.data[i]=row
    
    def find_next_best_move(self,queue,valueList):
        best_cost=999999
        best_node=""
        for neighbor in valueList:
            node,cost=neighbor
            if node not in queue:
                if cost<best_cost:
                    best_cost=cost
                    best_node=node
        return best_node,best_cost
            
           
            
    def get_shortest(self,start):
        visited=[]
        queue=[]
        resultant_cost=0
        visited.append(start)
        queue.append(start)
        while len(queue)<self.no_of_edges:
            current=visited.pop()
            node,cost=self.find_next_best_move(queue,self.data[current])
            resultant_cost+=cost
            visited.append(node)
            queue.append(node)

        return queue,resultant_cost
#edges=[12,6,1,4]
#g=Graph(edges)
#path,cost=g.get_shortest(int(6))
#print(path,cost)    
