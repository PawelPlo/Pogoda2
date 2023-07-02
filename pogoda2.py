import os
import pickle
import requests
import datetime

from datetime import timedelta


class Prognoza:
    def __init__(self,baza_danych=None, nazwa_pliku = "baza_danych.txt"):
        self.nazwa_pliku = nazwa_pliku
        if not baza_danych:
            self.baza_danych = self.wczytywanie_danych_z_pliku(self.nazwa_pliku)
        else:
            self.baza_danych = {}

    def wczytywanie_danych_z_pliku(self, searched_date_in):
        self.searched_date_in = searched_date_in
        if not os.path.exists(self.nazwa_pliku):
            print("Nie znaleziono pliku z bazą danych. Tworzę dodatkowy plik.")
            self.baza_danych = {}
        else:
            with open (self.nazwa_pliku) as f:
                for line in f:
                    if line.startswith(searched_date_in):
                        return line

    def wczytywanie_danych_do_pliku(self, baza_danych, nowa_prognoza):
        self.baza_danych = baza_danych
        self.nowa_prognoza=nowa_prognoza
        with open (self.nazwa_pliku, "a") as f:
            f.write(f"{searched_date_in} {opad}\n")


    def __setitem__(self, searched_date_in, opad):
        self.baza_danych[searched_date_in] = opad

    def __getitem__(self, data):
        return self.baza_danych[data]

    def __iter__(self):
        iter(self.baza_danych)
        return(self)


print("-------- SPRAWDŹ CZY BĘDZIE PADAŁO W WARSZAWIE ---------\n")


while True:
    nowa_prognoza = Prognoza(baza_danych="baza_danych.txt")
    date_today = datetime.datetime.now().date()
    date_tomorrow = date_today + timedelta(1)
    date_today = datetime.datetime.now().date().strftime('%Y-%m-%d')
    date_today = str(date_today).strip()
    date_tomorrow = str(date_tomorrow).strip()
    print(f"Dzisiejsza data:{date_today}\n")
    searched_date_in=input('''Wciśni "ENTER" jeśli chcesz prognozę na jutro. 
Jeśli chcesz prognozę na inny dzień, wpisz date w formacie YYYY-MM-DD: ''')
    if not searched_date_in:
        searched_date_in = date_tomorrow
        print(searched_date_in, "wziął datę z netu")
    prognoza_dzienna = nowa_prognoza.wczytywanie_danych_z_pliku(searched_date_in)
    if not prognoza_dzienna == None:
        print("Z bazy", prognoza_dzienna)
        zapytanie = input("Czy chcesz sprawdzić inną datę ? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue
    else:
        print("Nie było w bazie")
        pass


    params = {
        "latitude": 52,
        "longitude": -21,
        "hourly": "rain",
        "timezone": "Europe/London",
        "daily": "rain_sum",
        "start_date": str(searched_date_in),
        "end_date": str(searched_date_in)
}
    url = "https://api.open-meteo.com/v1/forecast"


    resp = requests.get(url,params=params)


    if resp.ok:
        nowa_prognoza = Prognoza(baza_danych="baza_danych.txt")
        opad = resp.json()["daily"]["rain_sum"][0]
        opad = float(opad)
        searched_date_in = str(searched_date_in)
        print(searched_date_in, opad)
        nowa_prognoza[searched_date_in] = opad
        print("To jest chyba z bazy", nowa_prognoza[searched_date_in])
        prognoza_dzienna = nowa_prognoza.wczytywanie_danych_do_pliku(searched_date_in, nowa_prognoza[searched_date_in])
        zapytanie = input("Czy chcesz sprawdzić inną datę ? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue
    if not resp.ok:
        print("Wpisałeś datę w złym formacie, lub nie ma prognozy na tą datę!\n")
        print(resp.text)
        zapytanie = input("Czy chcesz spróbować raz jeszcze? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue