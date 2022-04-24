import graph

a = graph.Graph()
a.sommets()
c = a.arc()
p=a.degre()
listeLigne =a.recup_ligne()

def underscore():
    with open("metro.txt", "r") as f1, open("new.txt", "w") as f2:
        nb_line = 0
        for line in f1:
            divide = line.split()
            if nb_line < 3:
                f2.write(line) 
            if 3 <= nb_line < 379:
                if len(divide) > 3:
                    f2.write(line[::-1].replace(" "[::-1], "_"[::-1], len(divide) - 3)[::-1])
                else:
                    f2.write(line)
            if nb_line >= 379:
                f2.write(line)
            nb_line += 1

def ligne():
    with open ("new.txt", "a") as file:
        for ligne in listeLigne:
            ele = list(ligne.keys())
            for start, next in ligne.items():
                if ele[-1] == start:
                    file.write(str(start)+ " ")
                    for val in next:
                        file.write(str(val+"\n"))
                else :
                    file.write(str(start)+" ")

