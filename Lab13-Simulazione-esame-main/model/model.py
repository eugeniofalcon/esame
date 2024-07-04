import geopy.distance
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._sightingList = DAO.getSighting()
        self._stateList = DAO.getStates()
        #self._neighborList = DAO.getNeighbors()
        self._shape = DAO.getShapes()
        self._ages = DAO.getAges()
        #self._sightings_by_state = DAO.getSightingByState()
        
        self._grafo = nx.Graph()  # DiGraph, MultiGraph
        self._grafo.add_nodes_from(self._stateList)

        self._nodes = []
        self._edges = []
        
        self._idMapSighting = {}
        for s in self._sightingList:
            self._idMapSighting[s.id] = s

        self._idMapState = {}
        for s in self._stateList:
            self._idMapState[s.id] = s

        # Ricorsione
        self.solBest = 0
        self.path = []
        self.path_edge = []

    def buildGraph(self, a, s):
        self._grafo.clear()

        for p in self._stateList:
            self._nodes.append(p)

        self._grafo.add_nodes_from(self._stateList)
        #self.addEdges()
        self.addEdges1(a, s)

    def addEdges(self):
        self._grafo.clear_edges()

        allEdges = self._neighborList
        for e in allEdges:
            if e.state1 in self._idMapState and e.state2 in self._idMapState:
                if not self._grafo.has_edge(self._idMapState[e.state1], self._idMapState[e.state2]):
                    weight = self.get_distance_weight(self._idMapState[e.state1], self._idMapState[e.state2])
                    self._grafo.add_edge(self._idMapState[e.state1], self._idMapState[e.state2], weight=weight)

    def addEdges2(self):
        self._grafo.clear_edges()

        self._sightingList.sort(key=lambda s: s.datetime)
        
        for i in range(len(self._sightingList) - 1):
            current_sighting = self._sightingList[i]
            next_sighting = self._sightingList[i + 1]
            self._grafo.add_edge(current_sighting.id, next_sighting.id, weight=1)

    def addEdges1(self, a, s):
        tmp_edges = DAO.getAllWeightedNeigh(a, s)

        for e in tmp_edges:
            self._edges.append((self._idMapState[e[0]], self._idMapState[e[1]], e[2]))

        self._grafo.add_weighted_edges_from(self._edges)

    def get_sum_weight_per_node(self):
        pp = []
        for n in self._grafo.nodes():
            sum_w = 0
            for e in self._grafo.edges(n, data=True):
                sum_w += e[2]['weight']
            pp.append((n.id, sum_w))
        return pp

    def addEdgePesati(self):
        """Questo metodo assegna come peso degli edges il numero di linee che congiungono i diversi nodi."""
        self._grafo.clear_edges()
        allConnessioni = []
        for c in allConnessioni:
            if self._grafo.has_edge(self._idMapState[c.state1], self._idMapState[c.state2]):
                self._grafo[self._idMapState[c.state1]][self._idMapState[c.state2]]["weight"] += 1
            else:
                self._grafo.add_edge(self._idMapState[c.state1], self._idMapState[c.state2], weight=1)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
        
    @property
    def forme(self):
        return self._shape

    ################ Aiuti con il grafo ########################
    def getBFSNodes(self, source):
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited

    def getDFSNodes(self, source):
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited
    
    def getConnessa(self, v0int):
        v0 = self._idMapSighting[v0int]

        connComp = nx.node_connected_component(self._grafo, v0)
        print(f"(connected comp): {len(connComp)}")

        return len(connComp)


##### RICORSIONE #####

    def computePath(self):
        self.path = []
        self.path_edge = []

        for n in self.get_nodes():
            partial = []
            partial.append(n)
            self.ricorsione(partial, [])

    def ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.getAdmissibleNeighbs(n_last, partial_edge)

        # stop
        if len(neighbors) == 0:
            weight_path = self.computeWeightPath(partial_edge)
            if weight_path > self.solBest:
                self.solBest = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return

        for n in neighbors:
            partial_edge.append((n_last, n, self._grafo.get_edge_data(n_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, partial_edge)
            partial.pop()
            partial_edge.pop()


    def getAdmissibleNeighbs(self, n_last, partial_edges):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result
    
    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += geopy.distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
        return weight
    
    def get_distance_weight(self, e):
        return geopy.distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))
    
    #getting shortest path
    #print(nx.dijkstra_path(G, 0, 8))
    #print(nx.dijkstra_path_length(G, 0, 7))
