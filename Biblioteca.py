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

    def modifica_prestito(self, titolo, prestato):
        for libro in self.libri:
            if libro.titolo == titolo:
                libro.prestato = prestato
                self.salva_libri()
                return True
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("\nBenvenuto nella Biblioteca 📚")
        print("1. Staff della biblioteca")
        print("2. Utente della biblioteca")
        print("3. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            staff_choice()
        elif scelta == '2':
            utente_choice()
        elif scelta == '3':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare")
class Staff:
    def __init__(self, filename='credenziali_staff.csv'):
        self.filename = filename

    def verifica_credenziali_staff(self, username, password):
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        return True
        except FileNotFoundError:
            print(f"File {self.filename} non trovato.")
        return False

    def crea_account_staff(self, username, password):
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'username': username, 'password': password})

def staff_choice():
    while True:
        clear_screen()
        print("\nStaff della Biblioteca 📚")
        print("1. Accedi con un account esistente")
        print("2. Torna al menu principale")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            if staff_authentication():
                staff_menu()
        elif scelta == '2':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

def staff_authentication():
    username = input("Username: ")
    password = input("Password: ")
    staff = Staff()
    if staff.verifica_credenziali_staff(username, password):
        return username, password
    else:
        print("Credenziali non valide. Accesso negato.")
        input("\nPremi Invio per continuare...")
        return None, None

def crea_account_staff():
    username = input("Inserisci un nuovo username: ")
    password = input("Inserisci una nuova password: ")
    staff = Staff()
    staff.crea_account_staff(username, password)
    print("Account staff creato con successo!")
    input("\nPremi Invio per continuare...")

def staff_menu():
    biblioteca = Biblioteca()
    username, password = staff_authentication()
    while True:
        clear_screen()
        print("\nGestore Biblioteca - Staff 📚")
        print("1. Aggiungi libro")
        print("2. Rimuovi libro")
        print("3. Mostra libri")
        print("4. Modifica stato di prestito di un libro")
        if username == 'Angelo_Galanti' and password == 'Il_Galo':
            print("5. Crea nuovo account staff")
        print("6. Torna al menu principale")
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
            print("Libri disponibili:")
            biblioteca.mostra_libri()
            titolo = input("Titolo del libro: ")
            prestato = input("Il libro è prestato? (s/n): ").lower() == 's'
            if biblioteca.modifica_prestito(titolo, prestato):
                print("Stato di prestito modificato con successo.")
            else:
                print("Libro non trovato.")
            input("\nPremi Invio per continuare...")
        elif scelta == '5' and username == 'Angelo_Galanti' and password == 'Il_Galo':
            crea_account_staff()
        elif scelta == '6':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

class Utente:
    def __init__(self, filename='credenziali_utente.csv'):
        self.filename = filename

    def verifica_credenziali_utente(self, username, password):
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        return True
        except FileNotFoundError:
            print(f"File {self.filename} non trovato.")
        return False

    def crea_account_utente(self, username, password):
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'username': username, 'password': password})

def utente_choice():
    while True:
        clear_screen()
        print("\nUtente della Biblioteca 📚")
        print("1. Crea un nuovo account")
        print("2. Accedi con un account esistente")
        print("3. Torna al menu principale")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            crea_account_utente()
        elif scelta == '2':
            if utente_authentication():
                utente_menu()
        elif scelta == '3':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

def crea_account_utente():
    username = input("Inserisci un nuovo username: ")
    password = input("Inserisci una nuova password: ")
    utente = Utente()
    utente.crea_account_utente(username, password)
    print("Account creato con successo!")
    input("\nPremi Invio per continuare...")

def utente_authentication():
    username = input("Username: ")
    password = input("Password: ")
    utente = Utente()
    if utente.verifica_credenziali_utente(username, password):
        return True
    else:
        print("Credenziali non valide. Accesso negato.")
        input("\nPremi Invio per continuare...")
        return False

def utente_menu():
    biblioteca = Biblioteca()
    while True:
        clear_screen()
        print("\nGestore Biblioteca - Utente 📚")
        print("Libri disponibili:")
        biblioteca.mostra_libri()
        print("\n1. Prendi in prestito un libro")
        print("2. Torna al menu principale")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            titolo = input("Inserisci il titolo del libro che vuoi prendere in prestito: ")
            libro_trovato = False
            for libro in biblioteca.libri:
                if libro.titolo == titolo and not libro.prestato:
                    libro.prestato = True
                    biblioteca.salva_libri()
                    print(f"Hai preso in prestito il libro: {libro.titolo}. Ora puoi venirlo a ritirare.")
                    libro_trovato = True
                    break
            if not libro_trovato:
                print("Libro non disponibile o già in prestito.")
            input("\nPremi Invio per continuare...")
        elif scelta == '2':
            break
        else:
            print("Opzione non valida, riprova.")
            input("\nPremi Invio per continuare...")

if __name__ == "__main__":
    main_menu()
