    def getSetAlbum(self, a1, dTOT):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._graph, a1)
        parziale = set([a1])
        connessa.remove(a1)

        self._ricorsione(parziale, connessa, dTOT)

        return self._bestSet, self.durataTot(self._bestSet)

    def _ricorsione(self, parziale, connessa, dTOT):
        #verificare se parziale è una sol ammissibile
        if self.durataTot(parziale) > dTOT:
            return

        #verificare se parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        #ciclo su nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                # rimanenti = copy.deepcopy(connessa)
                # rimanenti.remove(c)
                self._ricorsione(parziale, connessa, dTOT)
                parziale.remove(c)
