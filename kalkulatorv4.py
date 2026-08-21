from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import time
import os

calosc = ""
wynik_koncowy = ""
tryb_kolor = True
czy_leci = False
licznik = 0
start_czasu = 0

okno = Tk()
okno.title("Kalkulator")
okno.geometry("1000x800")


def klikniecie(co):
    global calosc
    if calosc == "0" and str(co).isdigit():
        calosc = str(co)
    else:
        calosc = calosc + str(co)
    ekran.delete(1.0, END)
    ekran.insert(1.0, calosc)


def policz_to():
    global calosc
    global wynik_koncowy
    if calosc != "":
        try:
            wynik_koncowy = str(eval(calosc))
            zapisz_wynik(calosc, wynik_koncowy)
            ekran.delete(1.0, END)
            ekran.insert(1.0, wynik_koncowy)
            calosc = wynik_koncowy
        except:
            ekran.delete(1.0, END)
            ekran.insert(1.0, "ERROR")
            calosc = ""
    else:
        ekran.delete(1.0, END)
        ekran.insert(1.0, "Pusto")


def wyczysc_wszystko():
    global calosc
    calosc = ""
    ekran.delete(1.0, END)


def cofnij_jeden():
    global calosc
    try:
        calosc = calosc[:-1]
        ekran.delete(1.0, END)
        ekran.insert(1.0, calosc)
    except:
        calosc = ""


def zapisz_wynik(dzialanie, wynik):
    linia = str(dzialanie) + " = " + str(wynik) + "\n"
    try:
        pole_male_wyniki.insert(1.0, linia)
    except:
        pass
    try:
        plik = open("wyniki.txt", "a", encoding="utf-8")
        plik.write(linia)
        plik.close()
    except:
        pass
    pokaz_historie()


def wczytaj_stare():
    if os.path.exists("wyniki.txt"):
        try:
            plik = open("wyniki.txt", "r", encoding="utf-8")
            tresc = plik.read()
            pole_male_wyniki.insert(1.0, tresc)
            plik.close()
        except:
            pass


def odswiezaj_zegar():
    if czy_leci:
        global licznik
        licznik = time.time() - start_czasu
        m, s = divmod(int(licznik), 60)
        h, m = divmod(m, 60)
        csetne = int((licznik - int(licznik)) * 100)
        tekst = "{:02d}:{:02d}:{:02d}.{:02d}".format(h, m, s, csetne)
        label_czas.config(text=tekst)
        okno.after(10, odswiezaj_zegar)


def start_klik():
    global czy_leci, start_czasu
    if not czy_leci:
        start_czasu = time.time() - licznik
        czy_leci = True
        odswiezaj_zegar()


def stop_klik():
    global czy_leci
    czy_leci = False


def reset_klik():
    global czy_leci, licznik
    czy_leci = False
    licznik = 0
    label_czas.config(text="00:00:00.00")


def szukaj_pliku():
    sciezka = filedialog.askopenfilename()
    if sciezka:
        input_sciezka.delete(0, END)
        input_sciezka.insert(0, sciezka)
        licz_slowa(sciezka)


def licz_slowa(plik_nazwa):
    try:
        w = pole_wpm.get()
        if w:
            speed = int(w)
        else:
            speed = 200
        f = open(plik_nazwa, "r", encoding="utf-8")
        txt = f.read()
        f.close()
        ilosc = len(txt.split())
        calosc_minut = ilosc / speed
        godziny = int(calosc_minut / 60)
        minuty = int(calosc_minut) - (godziny * 60)
        sekundy = int((calosc_minut - int(calosc_minut)) * 60)

        label_wynik_czyt.config(
            text="Słów: "
            + str(ilosc)
            + "\nCzas: "
            + str(godziny)
            + " h "
            + str(minuty)
            + " min "
            + str(sekundy)
            + " sek"
        )
    except Exception as e:
        messagebox.showerror("Blad", "Blad pliku: " + str(e))


def pokaz_historie():
    try:
        duze_pole_historia.config(state="normal")
        duze_pole_historia.delete(1.0, "end")
        if os.path.exists("wyniki.txt"):
            f = open("wyniki.txt", "r", encoding="utf-8")
            duze_pole_historia.insert(1.0, f.read())
            f.close()
        else:
            duze_pole_historia.insert(1.0, "Nie ma pliku")
        duze_pole_historia.config(state="disabled")
    except:
        pass


def zmien_tryb():
    global tryb_kolor
    if tryb_kolor == True:
        tlo = "#26242f"
        napisy = "white"
        guzik_tlo = "black"
        guzik_txt = "white"
        tryb_kolor = False
    else:
        tlo = "gray"
        napisy = "black"
        guzik_tlo = "SystemButtonFace"
        guzik_txt = "black"
        tryb_kolor = True

    okno.config(bg=tlo)
    pasek_gora.config(bg=tlo)
    karta1.config(bg=tlo)
    karta2.config(bg=tlo)
    karta3.config(bg=tlo)
    karta4.config(bg=tlo)

    style = ttk.Style()
    style.configure("TFrame", background=tlo)
    style.configure("TLabel", background=tlo, foreground=napisy)

    for dziecko in karta1.winfo_children():
        if isinstance(dziecko, Button):
            if dziecko["text"] != "=":
                dziecko.config(bg=guzik_tlo, fg=guzik_txt)

    ekran.config(bg=guzik_tlo, fg=guzik_txt)
    pole_male_wyniki.config(bg=guzik_tlo, fg=guzik_txt)


pasek_gora = Frame(okno, bg="gray")
pasek_gora.pack(side="top", fill="x")

przycisk_tryb = Button(pasek_gora, text="Tryb Noc/Dzien", command=zmien_tryb)
przycisk_tryb.pack(side="left", padx=10, pady=5)

zakladki = ttk.Notebook(okno)
tab1 = ttk.Frame(zakladki)
tab2 = ttk.Frame(zakladki)
tab3 = ttk.Frame(zakladki)
tab4 = ttk.Frame(zakladki)

zakladki.add(tab1, text="Kalkulator")
zakladki.add(tab2, text="Stoper")
zakladki.add(tab3, text="Czytanie")
zakladki.add(tab4, text="Historia")
zakladki.pack(expand=1, fill="both")

karta1 = Frame(tab1, bg="gray")
karta1.pack(fill="both", expand=True)

karta1.columnconfigure(0, weight=1)
karta1.columnconfigure(1, weight=1)
karta1.columnconfigure(2, weight=1)
karta1.columnconfigure(3, weight=1)
karta1.columnconfigure(4, weight=1)

karta1.rowconfigure(0, weight=1)
karta1.rowconfigure(1, weight=1)
karta1.rowconfigure(2, weight=1)
karta1.rowconfigure(3, weight=1)
karta1.rowconfigure(4, weight=1)
karta1.rowconfigure(5, weight=1)
karta1.rowconfigure(6, weight=1)
karta1.rowconfigure(7, weight=1)

pole_male_wyniki = Text(karta1, font=("Arial", 10), height=8, width=20)
pole_male_wyniki.grid(row=0, column=0, rowspan=8, padx=5, pady=5, sticky="nsew")

ekran = Text(karta1, height=2, font=("Arial", 30))
ekran.grid(row=1, column=1, columnspan=4, pady=5, padx=5, sticky="nsew")

Button(karta1, text="1", font=("Arial", 14), command=lambda: klikniecie(1)).grid(
    row=2, column=1, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="2", font=("Arial", 14), command=lambda: klikniecie(2)).grid(
    row=2, column=2, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="3", font=("Arial", 14), command=lambda: klikniecie(3)).grid(
    row=2, column=3, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="+", font=("Arial", 14), command=lambda: klikniecie("+")).grid(
    row=2, column=4, sticky="nsew", padx=2, pady=2
)

Button(karta1, text="4", font=("Arial", 14), command=lambda: klikniecie(4)).grid(
    row=3, column=1, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="5", font=("Arial", 14), command=lambda: klikniecie(5)).grid(
    row=3, column=2, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="6", font=("Arial", 14), command=lambda: klikniecie(6)).grid(
    row=3, column=3, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="-", font=("Arial", 14), command=lambda: klikniecie("-")).grid(
    row=3, column=4, sticky="nsew", padx=2, pady=2
)

Button(karta1, text="7", font=("Arial", 14), command=lambda: klikniecie(7)).grid(
    row=4, column=1, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="8", font=("Arial", 14), command=lambda: klikniecie(8)).grid(
    row=4, column=2, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="9", font=("Arial", 14), command=lambda: klikniecie(9)).grid(
    row=4, column=3, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="*", font=("Arial", 14), command=lambda: klikniecie("*")).grid(
    row=4, column=4, sticky="nsew", padx=2, pady=2
)

Button(karta1, text="(", font=("Arial", 14), command=lambda: klikniecie("(")).grid(
    row=5, column=1, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="0", font=("Arial", 14), command=lambda: klikniecie(0)).grid(
    row=5, column=2, sticky="nsew", padx=2, pady=2
)
Button(karta1, text=")", font=("Arial", 14), command=lambda: klikniecie(")")).grid(
    row=5, column=3, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="/", font=("Arial", 14), command=lambda: klikniecie("/")).grid(
    row=5, column=4, sticky="nsew", padx=2, pady=2
)

Button(karta1, text="Del", font=("Arial", 14), command=cofnij_jeden).grid(
    row=6, column=1, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="C", font=("Arial", 14), command=wyczysc_wszystko).grid(
    row=6, column=2, sticky="nsew", padx=2, pady=2
)
Button(karta1, text="^2", font=("Arial", 14), command=lambda: klikniecie("**2")).grid(
    row=6, column=3, sticky="nsew", padx=2, pady=2
)
Button(
    karta1, text="V", font=("Arial", 14), command=lambda: klikniecie("**(0.5)")
).grid(row=6, column=4, sticky="nsew", padx=2, pady=2)

Button(karta1, text="=", font=("Arial", 14), bg="orange", command=policz_to).grid(
    row=7, column=1, columnspan=4, sticky="nsew", padx=2, pady=2
)

wczytaj_stare()

karta2 = Frame(tab2, bg="gray")
karta2.pack(fill="both", expand=True)
label_czas = Label(karta2, text="00:00:00.00", font=("Consolas", 50), bg="gray")
label_czas.pack(pady=50)
Button(karta2, text="START", font=("Arial", 20), bg="green", command=start_klik).pack(
    pady=10, fill="x", padx=100
)
Button(karta2, text="STOP", font=("Arial", 20), bg="red", command=stop_klik).pack(
    pady=10, fill="x", padx=100
)
Button(karta2, text="RESET", font=("Arial", 20), bg="yellow", command=reset_klik).pack(
    pady=10, fill="x", padx=100
)
Label(
    karta2, text="Czytaj przez minute i policz ile słów udało ci sie przeczytać"
).pack(pady=20)

karta3 = Frame(tab3, bg="gray")
karta3.pack(fill="both", expand=True)
Label(karta3, text="1. Prędkość czytania (słowa/min):", font=("Arial", 14)).pack(
    pady=20
)
pole_wpm = Entry(karta3, font=("Arial", 14))
pole_wpm.insert(0, "200")
pole_wpm.pack()
Label(karta3, text="2. Wybierz plik:", font=("Arial", 14)).pack(pady=20)
input_sciezka = Entry(karta3, font=("Arial", 12), width=50)
input_sciezka.pack(pady=5)
Button(karta3, text="Wybierz i Oblicz", command=szukaj_pliku, bg="cyan").pack(pady=10)
label_wynik_czyt = Label(
    karta3, text="---", font=("Arial", 18), bg="lightgray", width=40, height=4
)
label_wynik_czyt.pack(pady=20)

karta4 = Frame(tab4, bg="gray")
karta4.pack(fill="both", expand=True)
Label(karta4, text="Historia obliczeń:", font=("Arial", 14)).pack(pady=10)
duze_pole_historia = Text(karta4, font=("Consolas", 12), height=25, width=80)
duze_pole_historia.pack(pady=10, padx=20)
Button(karta4, text="Odśwież Historię", command=pokaz_historie, bg="lightblue").pack(
    pady=10
)
pokaz_historie()

okno.mainloop()
