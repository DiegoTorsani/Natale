import csv
import os

class Libro:
    def __init__(self, titolo, autore, anno, prestato=False):
        self.titolo = titolo
        self.autore = autore
        self.anno = anno
        self.prestato = prestato

    def __repr__(self):
        return f"Libro(titolo='{self.titolo}', autore='{self.autore}', anno={self.anno}, prestato={self.prestato})"

class Biblioteca:
    def __init__(self, filename='biblioteca.csv'):
        self.filename = filename
        self.libri = self.carica_libri()

    def carica_libri(self):
        libri = []
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    libro = Libro(row['titolo'], row['autore'], int(row['anno']), row['prestato'] == 'True')
                    libri.append(libro)
        except FileNotFoundError:
            print(f"File {self.filename} non trovato. Verrà creato un nuovo file.")
        return libri

    def salva_libri(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['titolo', 'autore', 'anno', 'prestato']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for libro in self.libri:
                writer.writerow({
                    'titolo': libro.titolo,
                    'autore': libro.autore,
                    'anno': libro.anno,
                    'prestato': libro.prestato
                })

    def aggiungi_libro(self, libro):
        self.libri.append(libro)
        self.salva_libri()

    def rimuovi_libro(self, titolo):
        self.libri = [libro for libro in self.libri if libro.titolo != titolo]
        self.salva_libri()

    def mostra_libri(self):
        for libro in self.libri:
            print(libro)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def staff_authentication():
    nome = input("Nome: ")
    cognome = input("Cognome: ")
    data_nascita = input("Data di nascita (gg/mm/aaaa): ")
    numero_badge = input("Numero del badge: ")
    print(f"Benvenuto {nome} {cognome} (Badge: {numero_badge})")

def main_menu():
    while True:
        clear_screen()
        print("\nBenvenuto nella Biblioteca 📚")
        print("1. Staff della biblioteca")
        print("2. Utente della biblioteca")
        print("3. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            staff_authentication()
            staff_menu()
        elif scelta == '2':
            utente_menu()
        elif scelta == '3':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

def verifica_credenziali_staff(nome, cognome, data_nascita, numero_badge):
        try:
            with open('credenziali_staff.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (row['nome'] == nome and row['cognome'] == cognome and 
                        row['data_nascita'] == data_nascita and row['numero_badge'] == numero_badge):
                        return True
        except FileNotFoundError:
            print("File credenziali_staff.csv non trovato.")
        return False

def staff_authentication():
    nome = input("Nome: ")
    cognome = input("Cognome: ")
    data_nascita = input("Data di nascita (gg/mm/aaaa): ")
    numero_badge = input("Numero del badge: ")
    if verifica_credenziali_staff(nome, cognome, data_nascita, numero_badge):
        print(f"Benvenuto {nome} {cognome} (Badge: {numero_badge})")
        return True
    else:
        print("Credenziali non valide. Accesso negato.")
        return False

def staff_menu():
    biblioteca = Biblioteca()
    while True:
        clear_screen()
        print("\nGestore Biblioteca - Staff 📚")
        print("1. Aggiungi libro")
        print("2. Rimuovi libro")
        print("3. Mostra libri")
        print("4. Torna al menu principale")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            titolo = input("Titolo: ")
            autore = input("Autore: ")
            anno = int(input("Anno: "))
            libro = Libro(titolo, autore, anno)
            biblioteca.aggiungi_libro(libro)
        elif scelta == '2':
            print("Libri disponibili:")
            biblioteca.mostra_libri()
            titolo = input("Titolo del libro da rimuovere: ")
            biblioteca.rimuovi_libro(titolo)
        elif scelta == '3':
            biblioteca.mostra_libri()
            input("\nPremi Invio per continuare...")
        elif scelta == '4':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

def utente_menu():
    biblioteca = Biblioteca()
    while True:
        clear_screen()
        print("\nGestore Biblioteca - Utente 📚")
        print("1. Mostra libri")
        print("2. Torna al menu principale")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            biblioteca.mostra_libri()
            input("\nPremi Invio per continuare...")
        elif scelta == '2':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

if __name__ == "__main__":
    main_menu()