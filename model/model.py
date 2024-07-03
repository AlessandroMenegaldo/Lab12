import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0


    def getBestPath(self, lunghezza):
        self._bestPath = []
        self._bestScore = 0

        parziale = []
        for n in self._graph.nodes:
            parziale.append(n)
            self.ricorsione(parziale, lunghezza)
            parziale.pop()

        print(self._bestScore)
        self.printPath()

    def ricorsione(self, parziale, lunghezza_max):
        #controllo se soluzione ammissibile
        if len(parziale) == lunghezza_max:
            if  parziale[0] == parziale[-1]:
                #se ammissibile guardo se best soluzione
                score = self.getScore(parziale)
                if score > self._bestScore:
                    self._bestScore = score
                    self._bestPath = copy.deepcopy(parziale)

            return

        #altrimenti aggiungo nodi
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale[1:]:
                parziale.append(n)
                self.ricorsione(parziale, lunghezza_max)
                parziale.pop()



    def getScore(self, listOfNodes):
        score = 0
        for i in range(0, len(listOfNodes)-1):
            score += self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return score

    def printPath(self):
        listOfNodes = self._bestPath
        for i in range(0, len(listOfNodes) - 1):
            peso = self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
            print(f"{listOfNodes[i].Retailer_name} --> {listOfNodes[i+1].Retailer_name} ({peso})")





    def getAllCountries(self):
        return DAO.getAllCountries()

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, country, year):
        reatailers = DAO.getReatailers(country)
        for r in reatailers:
            self._idMap[r.Retailer_code]= r
        self._graph.add_nodes_from(reatailers)

        connections = DAO.getConnessioni(country, year, self._idMap)

        for c in connections:
            ret1 = c.Retailer_1
            ret2 = c.Retailer_2
            peso = c.score
            if ret1 in self._graph.nodes and ret2 in self._graph.nodes:
                self._graph.add_edge(ret1, ret2, weight = peso)


    def getVolumi(self):
        volumi = []
        for ret in self._graph.nodes:
            v = 0
            for n in self._graph.neighbors(ret):
                v += self._graph[ret][n]["weight"]
            volumi.append((ret,v))

        return sorted(volumi, key = lambda x: x[1], reverse=True)




    # HELPER FUNCTIONS

    def getScoreEdge(self, v1,v2):
        return self._graph[v1][v2]["weight"]
    def printGraphDetails(self):
        print(f"Num nodi: {len(self._graph.nodes)}")
        print(f"Num archi: {len(self._graph.edges)}")

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)

    def getAllNodes(self):
        return self._graph.nodes