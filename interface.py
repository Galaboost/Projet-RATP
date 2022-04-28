
import graph
import tkinter as tk
from tkinter import N, ttk

unGraph = graph.Graph()

station = []
unGraph.sommets()
graph1 = unGraph.arc()
unGraph.stockLigne()

for nom_station in unGraph.station:
    station.append(nom_station)

    

root = tk.Tk()
root.title("Itinéraire")
root.geometry("400x200")


def getstation1(event):
    station1.get()
    
    
def getstation2(event):
    station2.get()

def cherche_court_chemin():

    texte2 = ""
    s1 = station1.get()
    station_depart = unGraph.change_Station_to_Num(s1)

    s2 = station2.get()
    station_darrive = unGraph.change_Station_to_Num(s2)

    unGraph.init(graph1, str(station_depart))
    temps, chemin = unGraph.dijkstra(graph1, str(station_depart), str(station_darrive), str(station_depart))
    print(temps)

    for ligne,val in unGraph.ligne.items(): # ligne et direction de depart
        for index, num in enumerate(val):
            if str(station_depart) == num:
                l = ligne
                if val[index] + val[index+1] == str(station_depart) + str(chemin[1]):
                    direction = val[-1]
                    direction = unGraph.change_Un_num_to_Station(direction)
                else:
                    direction = val[0]
                    direction = unGraph.change_Un_num_to_Station(direction)

            if str(chemin[1]) == num: # ligne et direction au cas où si ya un changement au début
                in_case = ligne
                if val[index] + val[index+1] == str(chemin[1]) + str(chemin[2]):
                    in_case_direction = val[-1]
                    in_case_direction = unGraph.change_Un_num_to_Station(in_case_direction)
                else:
                    in_case_direction = val[0]
                    in_case_direction = unGraph.change_Un_num_to_Station(in_case_direction)

    for index, station in enumerate(chemin): # si il y a changement pendant le trajet
        if station != chemin[-1]:
            if station in graph1:
                for ele in graph1[station]:
                    num, temp = ele
                    if chemin[index+1] == num and temp in unGraph.time_change_line:
                        for ligne,val in unGraph.ligne.items():
                            for pos, numero_station in enumerate(val):
                                if chemin[index+1] == numero_station:
                                    l2 = ligne
                                    if (val[pos] + val[pos+1] == str(chemin[index+1]) + str(chemin[index+2])
                                                 or val[pos] + val[pos+1] == str(chemin[index+1]) ):
                                        direction2 = val[-1]
                                        direction2 = unGraph.change_Un_num_to_Station(direction2)
                                    else:
                                        direction2 = val[0]
                                        direction2 = unGraph.change_Un_num_to_Station(direction2)

                        Num_to_Nom = unGraph.change_Un_num_to_Station(chemin[index+1])
                        stock = "A {0}, changez et prenez la ligne {1}, direction {2} ".format(Num_to_Nom, l2, direction2)
                        texte2 = texte2 + stock + "\n"
                        del chemin[index]

    unGraph.change_Num_to_Station(chemin)
    if chemin[0] == chemin[1]: # si changement de ligne au point de départ on le supprime
        del chemin[0]
        l = in_case
        direction = in_case_direction
        if station_depart in unGraph.prochaine_station:
            for ele in unGraph.prochaine_station[station_depart]:
                station, duree = ele
                if duree in unGraph.time_change_line:
                    temps = temps - int(duree)
                    break
    if chemin[-1] == chemin[-2]: # si changement de ligne au point d'arrivé on le supprime
        del chemin[-1]
        if station_darrive in unGraph.prochaine_station:
            for ele in unGraph.prochaine_station[station_depart]:
                station, duree = ele
                if duree in unGraph.time_change_line:
                    temps = temps - int(duree)
                    break


    texte = "Vous êtes à la station {0} \n Prenez la ligne {1} direction {2}  ,".format(s1, l, direction)
    # texte2 est à la ligne 81
    temps = temps//60
    texte3 = "Vous devriez arriver à {0} dans {1} minites".format(s2, temps) +"\n", chemin

    root2 = tk.Tk()

    show = tk.Label(root2, text=texte)
    show2 = tk.Label(root2, text=texte2)
    show3 = tk.Label(root2, text=texte3)

    show.pack()
    show2.pack()
    show3.pack()
    root2.mainloop



# Widgets

label = tk.Label(root, text= "Sation de départ")
station1 = ttk.Combobox(root, values= station)
station1.bind("<<ComboboxSelected>>", getstation1)

label2 = tk.Label(root, text= "Sation d'arrivée")
station2 = ttk.Combobox(root, values= station)
station2.bind("<<ComboboxSelected>>", getstation2)

bouton = tk.Button(root, text="Rechercher", pady=10, padx=10, command=cherche_court_chemin)
# Placement widgets

label.place(x=10,y=50)
station1.place(x= 110, y=50)

label2.place(x=10,y=150)
station2.place(x= 110, y=150)
bouton.place(x=300, y=85)
root.mainloop()