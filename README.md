# README #

## Virtual Environment ##

1. Sofern nicht geschehen, muss virtualenv installiert werden: `sudo pip3 install virtualenv` oder wenn Python Probleme hat `sudo python3 -m pip install virtualenv`
2. Nun muss ein virtuelles environment erstellt werden mit `virtualenv -p /usr/bin/python3 venv`
3. Aktiviert wird die die virtuelle Umgebung durch: `source venv/bin/activate`
4. Jetzt die entsprechenden Packages installieren:
    1. `pip install numpy`
    2. `pip install tensorflow==1.12`
    3. `pip install tqdm`
5. Jetzt kann man Pakete installieren oder die Programme laufen lassen.


## Test Environment ##

1. Um die Tests auszuführen muss im Hauptordner nur `pytest` aufgerufen werden.

