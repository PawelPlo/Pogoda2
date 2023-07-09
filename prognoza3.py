import os
import requests
import datetime
from datetime import timedelta


class Prognoza:

    def __init__(self, baza_danych=None, nazwa_pliku="baza_danych.txt"):
        self.nazwa_pliku = nazwa_pliku
        if not baza_danych:
            self.baza_danych = self.pobieranie_danych_z_pliku(self.nazwa_pliku)
        else:
            self.baza_danych = {}
    def __setitem__(self, searched_date_in, opad):
        self.baza_danych[searched_date_in]=opad
    def __getitem__(self, searched_date_in):
        return self.baza_danych[searched_date_in]


    def pobieranie_danych_z_pliku(self, searched_date_in):
        self.searched_date_in = searched_date_in
        if not os.path.exists(self.nazwa_pliku):
            print("Nie znaleziono pliku z bazą danych. Tworzę dodatkowy plik.")
            self.baza_danych = {}
        else:
            with open(self.nazwa_pliku) as f:
                for line in f:
                    if line.startswith(searched_date_in):
                        line = line.replace("\n", "")
                        return line

    def wczytywanie_danych_do_pliku(self, baza_danych, nowa_prognoza):
        self.baza_danych = baza_danych
        self.nowa_prognoza=nowa_prognoza
        with open (self.nazwa_pliku, "a") as f:
            f.write(f"{searched_date_in} {opad}\n")

class FileReader:
    def __init__(self, filepath):
        self.fp = open(filepath)
        self.lines=[]
        self.done = False

    def __iter__(self):
        if self.done:
            return iter(self.lines)
        return(self)

    def __next__ (self):
        line = self.fp.readline()
        if not line:
            self.done = True
            self.fp.close()
            raise StopIteration
        self.lines.append(line[:-1])
        return line[:-1]



nowa_prognoza = Prognoza(baza_danych = "baza_danych.txt")
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
opad = nowa_prognoza.pobieranie_danych_z_pliku(searched_date_in)
print("Dane pobrane z pliku baza_danych.txt: ",opad)
nowa_prognoza[searched_date_in] = opad
nowa_prognoza[searched_date_in]
if not nowa_prognoza[searched_date_in] == None:
    print("Dane uzyskane za pomocą funkcji getitem: ", nowa_prognoza[searched_date_in])

if nowa_prognoza[searched_date_in] == None:
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

    resp = requests.get(url, params=params)

    if resp.ok:
        nowa_prognoza = Prognoza(baza_danych="baza_danych.txt")
        opad = resp.json()["daily"]["rain_sum"][0]
        opad = float(opad)
        searched_date_in = str(searched_date_in)
        nowa_prognoza[searched_date_in] = opad
        print(f"""Brak informacji w twojej bazie danych. Pobrano dane z internetu. W dniu {searched_date_in} spadnie {nowa_prognoza[searched_date_in]} mm deszczu""")
        prognoza_dzienna = nowa_prognoza.wczytywanie_danych_do_pliku(searched_date_in, nowa_prognoza[searched_date_in])


suma_opadow = {}
print("Zebrane dane o opadach")
for line in FileReader("baza_danych.txt"):
    print(line)
    line = line.split()
    k, v = line
    k = str(k)
    v= float(v)
    suma_opadow[k] = v

print("Zebrane dane o pogodzie dla następujących dat")
for k, v in suma_opadow.items:
    print(k)


print(suma_opadow)





