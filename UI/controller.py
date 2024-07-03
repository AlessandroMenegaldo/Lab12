import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        nazioni = self._model.getAllCountries()
        for n in nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(n))

        years = self._model.getAllYears()
        for a in years:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._view.update_page()

    def handle_graph(self, e):
        country = self._view.ddcountry.value
        year = self._view.ddyear.value

        if year is None:
            self._view.create_alert("Inserire l'anno")
            return

        if country is None:
            self._view.create_alert("Inserire la nazione")
            return


        self._model.buildGraph(country, year)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi: {self._model.getNumNodi()} Archi: {self._model.getNumArchi()}"))
        self._view.update_page()



    def handle_volume(self, e):
        listOfRet = self._model.getVolumi()
        for ret in listOfRet:
            self._view.txtOut2.controls.append(
                ft.Text(f"{ret[0].Retailer_name} - {ret[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        nStr = self._view.txtN.value
        self._view.txtOut3.controls.clear()

        try: n = int(nStr)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Inserisci un numero valido"))
            return

        if n <= 2:
            self._view.txtOut3.controls.append(ft.Text("Inserisci un numero maggiore di 2"))
            return

        self._model.getBestPath(n+1) #controllo numero nodi (n+1 archi)




