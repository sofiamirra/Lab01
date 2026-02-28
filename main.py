import random

# Definizione classe domanda
class Domanda:
    def __init__(self, testo, difficolta, risposta_corretta, risposte_errate):
        self.testo = testo
        self.difficolta = difficolta
        self.risposta_corretta = risposta_corretta
        self.risposte_errate = risposte_errate  # lista di 3 elementi

# Lettura file
domande = []  # lista con tutti gli oggetti domanda
blocco = []
with open("domande.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line == "":  # se la riga non è vuota, la salvo
            blocco.append(line)

        # Quando ho 6 righe, creo l'oggetto domanda
        if len(blocco) == 6:
            testo = blocco[0]
            difficolta = int(blocco[1])
            risposta_corretta = blocco[2]
            risposte_errate = blocco[3:6]
            domanda = Domanda(testo, difficolta, risposta_corretta, risposte_errate)
            domande.append(domanda)
            blocco = []  # reset per la prossima domanda

# Definizione classe Giocatore
class Giocatore:
    def __init__(self, nome, punteggio=0):
        self.nome = nome
        self.punteggio = punteggio

    def incrementa_punteggio(self):
        self.punteggio += 1

# Implementazione regole del gioco
class Game:
    def __init__(self, domande, giocatore):
        self.domande = domande  # lista di oggetti Domanda
        self.giocatore = giocatore  # oggetto Giocatore
        self.livello_corrente = 0

    def gioca_turno(self):
        while True:
            domande_livello = []
            for d in self.domande:
                if d.difficolta == self.livello_corrente:
                    domande_livello.append(d)

            # Pesco domanda casuale
            domanda_scelta = random.choice(domande_livello)

            # Preparo risposte casuali
            opzioni = [domanda_scelta.risposta_corretta] + domanda_scelta.risposte_errate  # concatenazione lista di 4 elementi
            random.shuffle(opzioni)

            # Mostra domanda e opzioni
            print(f"Livello {self.livello_corrente}")
            print(domanda_scelta.testo)
            for i, opzione in enumerate(opzioni, 1):
                print(f"    {i}. {opzione}")   # stampa indentata tipo quiz

            # Input utente
            scelta = int(input("Inserisci la risposta: "))

            # Controllo risposta
            if scelta - 1 == opzioni.index(domanda_scelta.risposta_corretta):  # Se la risposta è giusta
                self.giocatore.incrementa_punteggio()
                self.livello_corrente += 1
                print(f"Risposta corretta!\n")

                # Controllo se ci sono domande per il livello successivo
                livello_successivo_disponibile = False
                for d in self.domande:
                    if d.difficolta == self.livello_corrente:
                        livello_successivo_disponibile = True

                # Fine gioco se non ci sono domande per il livello successivo
                if not livello_successivo_disponibile:
                    break

            else:  # se la risposta è sbagliata
                print(f"Risposta sbagliata! La risposta corretta era: {opzioni.index(domanda_scelta.risposta_corretta) + 1}\n")
                break

        print(f"Hai totalizzato {self.giocatore.punteggio} punti!")
        nickname = input("Inserisci il tuo nickname: ")
        print("\n")
        self.giocatore.nome = nickname

# Lettura punteggi già presenti
lista_giocatori = []
with open("punti.txt", "r") as f:
    for riga in f:
        campi = riga.strip().split(" ")
        nome = campi[0]
        punteggio = int(campi[1])
        lista_giocatori.append(Giocatore(nome, punteggio))

# Turno di Gioco
giocatore_corrente = Giocatore("anonimo")
game = Game(domande, giocatore_corrente)
game.gioca_turno()
lista_giocatori.append(giocatore_corrente)

# Salvataggio su file in ordine decrescente
lista_giocatori.sort(key=lambda g: g.punteggio, reverse=True)
with open("punti.txt", "w") as f:
    for g in lista_giocatori:
        f.write(f"{g.nome} {g.punteggio}\n")