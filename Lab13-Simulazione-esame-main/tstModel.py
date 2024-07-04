from datetime import datetime
from model.model import Model

mymodel = Model()
mymodel.buildGraph(1929, "disk")
print(mymodel._grafo)

#tic = datetime.now()
#mymodel.addEdgeMode3()
#toc = datetime.now()
#print(f"Time elapsed: {toc-tic}")

print(f"The graph has {mymodel.getNumNodes()} nodes.")
print(f"The graph has {mymodel.getNumEdges()} edges.")
