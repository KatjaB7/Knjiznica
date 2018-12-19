import csv

def pobrisi_tabele(conn):
    """
    Pobriše tabele iz baze.
    """
    conn.execute("DROP TABLE IF EXISTS izposoja;")
    conn.execute("DROP TABLE IF EXISTS clan;")
    conn.execute("DROP TABLE IF EXISTS zalozba;")
    conn.execute("DROP TABLE IF EXISTS avtor;")
    conn.execute("DROP TABLE IF EXISTS knjiga;")


def ustvari_tabele(conn):
    """
    Ustvari tabele v bazi.
    """
    conn.execute("""
        CREATE TABLE knjiga (
            id        INTEGER PRIMARY KEY,
            naslov    TEXT,
            opis      TEXT,
            avtor     INTEGER REFERENCES avtor(id),
            zalozba   INTEGER REFERENCES zalozba(id)
        );
    """)
    conn.execute("""
        CREATE TABLE avtor (
            id  INTEGER PRIMARY KEY,
            ime TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE zalozba (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            naziv TEXT,
            kraj  TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE clan (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            ime   TEXT,
            dolg  REAL
        );
    """)
    conn.execute("""
        CREATE TABLE izposoja (
            id              INTEGER REFERENCES knjiga(id),
            datum_izposoje  DATE,
            datum_vracila   DATE,
            rok_vracila     DATE,
            strosek         REAL,
            clan            INTEGER REFERENCES clan(id)
        );
    """)


def uvozi_knjige(conn):
    """
    Uvozi podatke o knjigah.
    """
    conn.execute("DELETE FROM knjiga;")
    with open('podatki/knjiga.csv') as datoteka:
        podatki = csv.reader(datoteka, delimiter=";")
        next(podatki)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO knjiga VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)


def uvozi_avtorje(conn):
    """
    Uvozi podatke o avtorjih.
    """
    conn.execute("DELETE FROM avtor;")
    with open('podatki/avtor.csv') as datoteka:
        podatki = csv.reader(datoteka, delimiter=";")
        next(podatki)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO avtor VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)


def uvozi_zalozbe(conn):
    """
    Uvozi podatke o založbah.
    """
    conn.execute("DELETE FROM zalozba;")
    with open('podatki/zalozba.csv') as datoteka:
        podatki = csv.reader(datoteka, delimiter=";")
        next(podatki)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO zalozba VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            print(vrstica)
            conn.execute(poizvedba, vrstica)


def uvozi_clane(conn):
    """
    Uvozi podatke o članih.
    """
    conn.execute("DELETE FROM clan;")
    with open('podatki/clan.csv') as datoteka:
        podatki = csv.reader(datoteka, delimiter=";")
        next(podatki)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO clan VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_izposoje(conn):
    """
    Uvozi podatke o izposojah knjig.
    """
    conn.execute("DELETE FROM izposoja;")
    with open('podatki/izposoja.csv') as datoteka:
        podatki = csv.reader(datoteka, delimiter=";")
        next(podatki)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO izposoja VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)


def ustvari_bazo(conn):
    """
    Opravi celoten postopek postavitve baze.
    """
    pobrisi_tabele(conn)
    ustvari_tabele(conn)
    uvozi_knjige(conn)
    uvozi_avtorje(conn)
    uvozi_zalozbe(conn)
    uvozi_clane(conn)
    uvozi_izposoje(conn)


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)
