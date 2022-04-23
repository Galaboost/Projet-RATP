class Graph():

    def __init__(self):
        self.station = dict()
        self.prochaine_station = dict()
        self.ligne = dict()

    def sommets(self):
        """
        chaque station avec leur ligne correspondante
        modèle de type {Nom_station : {(num_station)}}
        """
        nb_line = 0
        with open("new.txt", "r") as file:
            for line in file:
                divide = line.split()
                if 3 <= nb_line < 379:
                    if divide[2] not in self.station:
                        self.station[divide[2]] = set()
                    self.station[divide[2]].add(divide[1])
                nb_line += 1
        return self.station


    def arc(self):
        """
        On relie chaque arc, ce qui nous donne un graph
        Modèle de type {numero_station : {(numero_station, temps_en_seconde) ...}}
        """
        l = ["201", "52", "198", "373", "196", "248","259", "280", "92"] # les station de la ligne 7bis et 10 qui ont 1 successeur
        nb_line = 0
        with open("new.txt", "r") as file:
            for line in file:
                divide = line.split()
                if 379 <= nb_line < 852:
                    if divide[1]  not in self.prochaine_station:
                        self.prochaine_station[divide[1]] = set()
                    if divide[2] not in self.prochaine_station:
                        self.prochaine_station[divide[2]] = set()
                    self.prochaine_station[divide[1]].add((divide[2], divide[3]))
                    if divide[2] not in l and divide[1] not in l:
                        self.prochaine_station[divide[2]].add((divide[1], divide[3]))
                    
                nb_line += 1
        return self.prochaine_station


#################### CONNEXE ####################

    def connectedComponent(self):
        deja_traite = []
        couleur = []
        comp_connexe = []
        for sommet in range(len(self.prochaine_station.keys())):
            couleur.append("Blanc")
        for sommet in range(len(self.prochaine_station.keys())):
            if couleur[sommet] == "Blanc":
                comp_connexe.append(self.parcoursProfondeur(deja_traite, sommet,couleur))
        return comp_connexe

    def parcoursProfondeur(self,deja_traite, sommet, couleur) :
        couleur[int(sommet)] = "Noir"
        deja_traite.append(sommet)
        for successeur in self.prochaine_station.values():
            for v, temps in successeur:
                if couleur[int(v)] == "Blanc":
                    deja_traite = self.parcoursProfondeur(deja_traite,v , couleur)
        return deja_traite
    
    def checkConnected(self):
        """
        Pour vérifier si un graph est connexe, on fait un parcours en profondeur 
        si à la fin on trouve 1 et seulement 1 composant connexe alors tout le graph est connexe
        sinon il faut qu'on ajoute des liaisons pour avoir un seul composant connexe
        """
        nb_connectedComponent = self.connectedComponent()
        if len(nb_connectedComponent) == 1:
            print("Le graph est connexe")
        else:
            print("Le graph n'est pas connexe")


#################### Les 16 lignes de metro  ####################
    terminus = []
    time_change_line = []
    nb_ligne = 0

    with open("new.txt", "r") as file:
        for line in file:
            divide = line.split()
            if 852>nb_ligne >= 742:
                if divide[3] not in time_change_line:
                    time_change_line.append(divide[3])
            nb_ligne += 1

    def degre(self):  
        l = [201, 52, 198, 373, 196, 248, 259, 92] # del 280
        l2 = []
        nom = dict() # sans les changement de ligne
        for i in range(len(self.prochaine_station)):
            nom[i] = set()

        for sommet, successeur in self.prochaine_station.items():
            for num, temps in successeur:
                if temps not in self.time_change_line:
                    nom[int(sommet)].add((num, temps))
        for station in nom:
            if len(nom[station]) == 1:
                l2.append(station)
        self.terminus = [val for val in l2 if val not in l]
        return self.terminus



    a_traite = None
    deja_traite = dict()

    def parcours(self, sommet): #parcours profondeurs
        self.deja_traite[int(sommet)] = set()
        
        for successeur in self.prochaine_station[sommet]:
            station, temps = successeur
            if int(station) not in self.deja_traite and temps not in self.time_change_line:
                self.a_traiter = station
                self.deja_traite[int(sommet)].add(station)

        if int(self.a_traiter) in self.terminus:
            for val in self.deja_traite.values():
                if len(val) == 2:
                    for num in val:
                        if int(num) not in self.deja_traite:
                            self.a_traite = num
                            self.parcours(self.a_traite)
                    else:
                        return self.deja_traite
        else:
            self.parcours(self.a_traiter)
        

    def recup_ligne(self):
        traiter = []
        lignePasTraite = [37, 117]
        ligne = []
        for station in self.terminus:
            if station not in traiter and station not in lignePasTraite:
                self.parcours(str(station))
                ligne.append(self.deja_traite)
                for val in self.deja_traite.values():
                    for num in val:
                        if int(num) in self.terminus:
                            traiter.append(int(num))
            self.deja_traite = dict()
        return ligne

    def stockLigne(self):
        nb_ligne = 0
        ligne = ["1", "2", "3", "3bis", "4", "5", "6", "7", "7bis","8", "9", "10", "11", "12", "13", "14"]
        ter_l = [66, 213, 114, 116, 262, 28, 57, 152, 170, 89, 181, 117, 68, 178, 72, 24]
        for i in ligne:
            self.ligne[i] = list()
        with open("new.txt", "r") as file:
            for line in file:
                divide = line.split()
                if 852 <= nb_ligne < 868:
                    for index, number in enumerate(ter_l):

                        if number == int(divide[0]):
                            if index == 3:
                                index = "3bis"
                                self.ligne[index].append(line)
                            elif index == 8:
                                index = "7bis"
                                self.ligne[index].append(line)
                            elif  3 < index < 8 :
                                self.ligne[str(index)].append(line)
                            elif 8 < index <= 15:
                                index = index -1
                                self.ligne[str(index)].append(line)
                            else:
                                index = index + 1
                                self.ligne[str(index)].append(line)        
                nb_ligne += 1  
        return self.ligne
#################### ALGO Dijkstra ####################

    duree = {}
    fini_traiter = []
    temps_toto = None
    chemin_emprunte = {}
    

    def init(self, graph, start):
        for sommet in graph:
            self.duree[sommet] = float("inf")
        self.duree[start] = 0

    def affiche_trajet(self,pere,start,end, suivant):

        if end == start:
            return [start] + suivant
        else:
            return (self.affiche_trajet(pere, start, pere[end], [end]+ suivant))

    def dijkstra(self,graph, entrain_de_traiter, end, start):

        minimun = float("inf")

        if entrain_de_traiter == end:
            return self.temps_toto, self.affiche_trajet(self.chemin_emprunte, start, end, [])

        for successeur, temps in self.prochaine_station[entrain_de_traiter]:
            if successeur not in self.fini_traiter:
                seconde = self.duree[entrain_de_traiter] + int(temps)
                if seconde < self.duree[successeur] :
                    self.duree[successeur] = seconde
                    self.chemin_emprunte[successeur] = entrain_de_traiter
                    if seconde < minimun:
                        minimun = seconde
                        self.temps_toto = minimun
                        
        self.fini_traiter.append(entrain_de_traiter) 
        pas_traite = dict(self.duree)
        for s in self.fini_traiter:
            pas_traite.pop(s)
        prochain_à_etre_traite = min(pas_traite, key= pas_traite.get)


        return self.dijkstra(graph, prochain_à_etre_traite, end, start)


#################### AUTRES ####################

    def changeLigne(self,ligne): # ligne
        """
        on change les numero de station par leur nom
        """
        for nom_station, ses_id in self.station.items():

            for id in ses_id:
                for nom, next in ligne.items():
                    for val in next: 
                        if len(val) == 1:
                            val = "000"+val
                        if len(val) == 2:
                            val ="00"+val
                        if len(val) == 3:
                            val = "0"+val
                        if id == val:
                            ligne[nom] = nom_station

    def changeChemin(self, chemin): # trajet plus cours chemin

        for nom_station, ses_id in self.station.items():
            for id in ses_id:
                for index, numero in enumerate(chemin):
                    if len(numero) == 1:
                        numero = "000"+numero
                    if len(numero) == 2:
                        numero ="00"+numero
                    if len(numero) == 3:
                        numero = "0"+numero
                    if id == numero:
                        chemin[index] = nom_station




if __name__ == "__main__":
    a = Graph() 

    b = a.sommets()
    c = a.arc()
    p=a.degre()
    a.recup_ligne()
    point_de_depart = "152"
    a.init(c , point_de_depart)
    temps , chemin = a.dijkstra(c , point_de_depart, "130", point_de_depart)
    a.changeChemin(chemin)
    print(chemin, temps)
