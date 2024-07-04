import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

        # Aiuti dropdown
        self._partenza = None
        self._arrivo = None
        self._shape = None
        self._age = None

        # Aiuti con un input di testo
        self._input = None #Questo è un int

    
    def fillDD(self):
        pass

    def handle_graph(self, e):
        self._model.buildGraph(self._age, self._shape)
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nEdges} archi."))

        for p in self._model.get_sum_weight_per_node():
             self._view.txt_result.controls.append(ft.Text(f"Nodo {p[0]}, somma pesi su archi ={p[1]}"))

        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):

        self._model.computePath()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0].id} --> {ii[1].id}: weight {ii[2]} distance {str(self._model.get_distance_weight(ii))}")) #ii[2]

        self._view.update_page()

    ################ Aiuti con il dropdown ########################
    def loadShapes(self, dd: ft.Dropdown()): # type: ignore

        #Cosa scrivere in view
        shapes = self._model._shape

        for s in shapes:
            dd.options.append(ft.dropdown.Option(text=s,
                                                    data=s,
                                                    on_click=self.read_shape))

    def read_shape(self,e):
        print("read_shape called ")
        if e.control.data is None:
            self._shape = None
        else:
            self._shape = e.control.data

        if self._shape is not None and self._age is not None:
            self._view.btn_graph.disabled = False
            self._view.update_page()
    
    def loadAnni(self, dd: ft.Dropdown()): # type: ignore

        #Cosa scrivere in view
        # self._controller.loadFermate(self._comeSiChiamaIlDropDownInView)
        ages = self._model._ages

        for a in ages:
            dd.options.append(ft.dropdown.Option(text=str(a),
                                                    data=a,
                                                    on_click=self.read_age))

    def read_age(self,e):
        print("read_shape called ")
        if e.control.data is None:
            self._age = None
        else:
            self._age = e.control.data

        if self._shape is not None and self._age is not None:
            self._view.btn_graph.disabled = False
            self._view.update_page()

    def loadStates(self, dd: ft.Dropdown()): # type: ignore

        #Cosa scrivere in view
        # self._controller.loadFermate(self._comeSiChiamaIlDropDownInView)

        states = self._stateList

        if dd.label == "Inizio":
            for s in states:
                dd.options.append(ft.dropdown.Option(text=s.Name,
                                                     data=s,
                                                     on_click=self.read_Partenza))
        elif dd.label == "Fine":
            for s in states:
                dd.options.append(ft.dropdown.Option(text=s.Name,
                                                     data=s,
                                                     on_click=self.read_Arrivo))

    def read_Partenza(self,e):
        print("read_Partenza called ")
        if e.control.data is None:
            self._partenza = None
        else:
            self._partenza = e.control.data

    def read_Arrivo(self,e):
        print("read_Arrivo called ")
        if e.control.data is None:
            self._arrivo = None
        else:
            self._arrivo = e.control.data

    ################ Aiuti con il bottone ########################
    def leggi_tendina(self, e):
        self._input = int(e.control.value)

    
    def get_qualcosa(self, e):
        #pd = self._view.dd_periodo.value
        if self._input is None:
            self._view.create_alert("Selezionare...")
            return
        #studenti = self._model.get_studenti_corso(self._codins)
        #self._view.lst_result.controls.clear()
        #for studente in studenti:
        #    self._view.lst_result.controls.append(ft.Text(studente))
        #self._view.update_page()
