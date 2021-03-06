import baza
import sqlite3
import random
import hashlib

conn = sqlite3.connect('Knjiznica.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

import datetime

def stevilo_knjig():
    poizvedba = """
        SELECT COUNT(*)
        FROM knjiga
    """
    (st_knjig,) = conn.execute(poizvedba).fetchone()
    return st_knjig

def stevilo_clanov():
    poizvedba = """
        SELECT COUNT(*)
        FROM clan
    """
    (st_clanov,) = conn.execute(poizvedba).fetchone()
    return st_clanov


def poisci_knjige(niz):
    """
    Funkcija, ki vrne šifre vseh knjig, katerih naslov vsebuje dani niz.
    """
    poizvedba = """
        SELECT id
        FROM knjiga
        WHERE naslov LIKE ?
    """
    return [id_knjige for (id_knjige,) in conn.execute(poizvedba, ['%' + niz + '%'])]


def podatki_knjig(idji_knjig):
    """
    Vrne osnovne podatke vseh knjig z danimi IDji.
    """
    poizvedba = """
        SELECT id, naslov, opis, avtor
        FROM knjiga 
        WHERE id IN ({})
    """.format(', '.join(len(idji_knjig) * ['?']))
    return conn.execute(poizvedba, idji_knjig).fetchall()


def podatki_knjige(id_knjige):
    """
    Vrne podatke o knjigi z danim IDjem.
    """
    poizvedba = """
        SELECT naslov, opis
        FROM knjiga
        WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_knjige])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        naslov, opis = osnovni_podatki
        poizvedba_za_avtorja = """
            SELECT avtor.ime
            FROM avtor
            JOIN knjiga ON avtor.id = knjiga.avtor
            WHERE knjiga.id = ?
        """
        avtor, = cur.execute(poizvedba_za_avtorja, [id_knjige]).fetchone()
        poizvedba_za_zalozbo = """
            SELECT zalozba.naziv
            FROM zalozba
            JOIN knjiga ON zalozba.id = knjiga.zalozba
            WHERE knjiga.id = ?
        """
        zalozba, = cur.execute(poizvedba_za_zalozbo, [id_knjige]).fetchone()
        return naslov, opis, avtor, zalozba


def id_avtorja(avtor, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podanega avtorja.
    Če avtor še ne obstaja, ga doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM avtor WHERE ime = ?", [avtor]).fetchone()
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO avtor (ime) VALUES (?)", [avtor]).lastrowid
    else:
        return None


def id_zalozbe(zalozba, kraj, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podane založbe.
    Če založba še ne obstaja, jo doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM zalozba WHERE naziv = ?", [zalozba]).fetchone() 
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO zalozba (naziv, kraj) VALUES (?, ?)", [zalozba, kraj]).lastrowid 
    else:
        return None

def id_clana(clan, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podanega člana.
    Če ta oseba še ni član knjižnice, ga doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM clan WHERE ime = ?", [clan]).fetchone()
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO clan (ime) VALUES (?)", [clan]).lastrowid
    else:
        return None


def dodaj_knjigo(naslov, opis, avtor, zalozba, kraj): 
    """
    V bazo doda knjigo ter njen opis, IDavtorja in IDkzalozbe.
    """
    with conn:
        podatki = [naslov, opis, id_avtorja(avtor, True), id_zalozbe(zalozba, kraj, True)]
        print(podatki)
        return conn.execute("""
            INSERT INTO knjiga (naslov, opis, avtor, zalozba)
                            VALUES (?, ?, ?, ?)
        """, podatki).lastrowid

def poisci_avtorje(niz):
    """
    Funkcija, ki vrne IDje vseh clanov, katerih ime vsebuje dani niz.
    """
    poizvedba = """
        SELECT id
        FROM avtor
        WHERE ime LIKE ?
        ORDER BY ime
    """
    idji_avtorjev = []
    for (id_avtorja,) in conn.execute(poizvedba, ['%' + niz + '%']):
        idji_avtorjev.append(id_avtorja)
    return idji_avtorjev

def podatki_avtorjev(idji_avtorjev):
    """
    Vrne osnovne podatke vseh avtorjev z danimi IDji.
    """
    poizvedba = """
        SELECT id, ime
        FROM avtor
        WHERE id IN ({})
    """.format(', '.join(len(idji_avtorjev) * ['?']))
    return conn.execute(poizvedba, idji_avtorjev).fetchall()

def podatki_avtor(id_avtorja):  
    """
    Vrne podatke o avtorju z danim IDjem.
    """
    poizvedba = """
        SELECT ime
        FROM avtor
        WHERE id = ?
    """
    cur = conn.execute(poizvedba, [id_avtorja])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        ime,  = osnovni_podatki
        poizvedba_za_knjige = """
            SELECT knjiga.naslov
            FROM knjiga
            WHERE knjiga.avtor = ?
        """
        naslovi_knjig = []
        for (naslov,) in conn.execute(poizvedba_za_knjige, [id_avtorja]):
            naslovi_knjig.append(naslov)
        return ime, naslovi_knjig



def poisci_clane(niz):
    """
    Funkcija, ki vrne IDje vseh clanov, katerih ime vsebuje dani niz.
    """
    poizvedba = """
        SELECT id
        FROM clan
        WHERE ime LIKE ?
        ORDER BY ime
    """
    idji_clanov = []
    for (id_clana,) in conn.execute(poizvedba, ['%' + niz + '%']):
        idji_clanov.append(id_clana)
    return idji_clanov


def podatki_clanov(idji_clanov):
    """
    Vrne osnovne podatke vseh clanov z danimi IDji.
    """
    poizvedba = """
        SELECT id, ime, dolg
        FROM clan
        WHERE id IN ({})
    """.format(', '.join(len(idji_clanov) * ['?']))
    return conn.execute(poizvedba, idji_clanov).fetchall()



def podatki_clana(id_clan):
    """
    Vrne podatke o članu z danim IDjem.
    """
    poizvedba = """
        SELECT ime, dolg 
        FROM clan 
        WHERE id = ?
    """
    cur = conn.execute(poizvedba, [id_clan])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        ime, dolg, = osnovni_podatki
        poizvedba_za_knjige = """
            SELECT knjiga
            FROM izposoja
            JOIN clan ON izposoja.clan = clan.id
            WHERE clan.id = ?
        """
        idji_knjig = []
        for (id_knjige,) in conn.execute(poizvedba_za_knjige, [id_clan]):
            idji_knjig.append(id_knjige)
        return ime, dolg, idji_knjig

def dodaj_clana(ime_clana): 
    poizvedba = """
        INSERT INTO clan
        (ime, dolg)
        VALUES (?, 0)
    """
    with conn:
        return conn.execute(poizvedba, [ime_clana]).lastrowid


def dodaj_izposojo(id_clan, id_knjiga): 
    poizvedba = """
        INSERT INTO izposoja
        (datum_izposoje, rok_vracila, clan, knjiga)
        VALUES (date('now'), date('now', '+21 days'), ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_clan, id_knjiga]).lastrowid
        return id_knjiga

def dodaj_vracilo(id_knjige): 
    poizvedba = """
        UPDATE izposoja SET datum_vracila = date('now') WHERE knjiga = ?
    """
    conn.execute(poizvedba, [id_knjige])
    poizvedba_rok = """
        SELECT rok_vracila, datum_vracila, clan FROM izposoja WHERE knjiga = ?
    """
    rok, datum, clan = conn.execute(poizvedba_rok, [id_knjige]).fetchone()
    if datum > rok:
        poizvedba = """
            UPDATE clan SET dolg = dolg + julianday(?) - julianday(?)
            WHERE id = ?
            """
        with conn:
            conn.execute(poizvedba, [datum, rok, clan])

def poravnava_dolga(id_clana):
    poizvedba = """
        UPDATE clan
        SET dolg = 0
        WHERE clan.id = ?
        """
    with conn:
        return conn.execute(poizvedba, [id_clana]).lastrowid

def podatki_izposoje(id_knjiga):
    poizvedba = """
        SELECT knjiga, clan, datum_izposoje, datum_vracila, rok_vracila
        FROM izposoja
        WHERE knjiga = ?
        """
    with conn:
        return conn.execute(poizvedba, [id_knjiga]).fetchone()

def podatki_vracila(id_knjige):
    poizvedba = """
        SELECT dolg
        FROM clan JOIN izposoja ON clan.id = izposoja.clan
        WHERE izposoja.knjiga = ?
    """
    with conn:
        return conn.execute(poizvedba, [id_knjige]).fetchone()

def seznam_zalozb():
    poizvedba = """
        SELECT id, naziv FROM zalozba
        ORDER BY naziv
    """
    return conn.execute(poizvedba).fetchall()

def seznam_krajev():
    poizvedba = """
        SELECT id, kraj FROM zalozba
        ORDER BY kraj
    """
    return conn.execute(poizvedba).fetchall()

def seznam_clanov():
    poizvedba = """
        SELECT id, ime FROM clan
        ORDER BY ime
    """
    return conn.execute(poizvedba).fetchall()

def seznam_knjig():
    poizvedba = """
        SELECT id, naslov FROM knjiga
        ORDER BY naslov
    """
    return conn.execute(poizvedba).fetchall()



def zakodiraj(geslo, sol=None):
    if sol is None:
        sol = ''.join(chr(random.randint(65, 122)) for _ in range(16))
    posoljeno_geslo = geslo + '$' + sol
    zakodirano_geslo = hashlib.sha512(posoljeno_geslo.encode()).hexdigest()
    return zakodirano_geslo, sol


def preveri_geslo(uporabnisko_ime, geslo):
    poizvedba = """
        SELECT geslo, sol FROM uporabniki
        WHERE uporabnisko_ime = ?
    """
    uporabnik = conn.execute(poizvedba, [uporabnisko_ime]).fetchone()
    if uporabnik is None:
        return False
    shranjeno_geslo, sol = uporabnik
    zakodirano_geslo, _ = zakodiraj(geslo, sol)
    return shranjeno_geslo == zakodirano_geslo


def ustvari_uporabnika(uporabnisko_ime, geslo):
    poizvedba = """
        INSERT INTO uporabniki
        (uporabnisko_ime, geslo, sol)
        VALUES (?, ?, ?)
    """
    with conn:
        zakodirano_geslo, sol = zakodiraj(geslo)
        conn.execute(poizvedba, [uporabnisko_ime, zakodirano_geslo, sol]).fetchone()
        return True
        