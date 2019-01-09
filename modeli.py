import baza
import sqlite3

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
        SELECT id, naslov, opis
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
            WHERE knjiga.avtor = ?
        """
        cur.execute(poizvedba_za_avtorja, [id_knjige]).lastrowid
        avtorji = [vrstica[0] for vrstica in cur.fetchall()]
        poizvedba_za_zalozbo = """
            SELECT zalozba.naziv
            FROM zalozba
                 JOIN knjiga ON zalozba.id = knjiga.zalozba
            WHERE knjiga.zalozba = ?
        """
        cur.execute(poizvedba_za_zalozbo, [id_knjige])
        zalozbe = [vrsta[0] for vrsta in cur.fetchall()]
        return naslov, opis, avtorji, zalozbe


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
        conn.execute("""
            INSERT INTO knjiga (naslov, opis, avtor, zalozba)
                            VALUES (?, ?, ?, ?)
        """, [naslov, opis, id_avtorja(avtor, True), id_zalozbe(zalozba, kraj, True)]).lastrowid

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
            SELECT izposoja.id
            FROM izposoja
            JOIN clan ON izposoja.clan = clan.id
            WHERE izposoja.clan = ?
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
        conn.execute(poizvedba, [id_clana(ime_clana, True)])


def dodaj_izposojo(id_clan, id_knjiga): 
    poizvedba = """
        INSERT INTO izposoja
        (datum_izposoje, rok_vracila, clan, id)
        VALUES (date('now'), date('now', '+21 days'), ?, ?)
    """
    with conn:
        return conn.execute(poizvedba, [id_clan, id_knjiga]).lastrowid

def dodaj_vracilo(id_izposoje): #ne dela
    poizvedba = """
        UPDATE izposoja, clan
        SELECT izposoja.clan
        SET iposoja.datum_vracila = date('now')
        WHERE izposoja.id = ?
        CASE 
            WHEN datum_vracila > rok_vracila
            THEN SET clan.dolg += (((datum_vracila - rok_vracila)* 0.5) AS INTEGER)
        END
        """
    with conn:
        return conn.execute(poizvedba, [id_izposoje]).lastrowid

def poravnava_dolga(id_clana):
    poizvedba = """
        UPDATE clan
        SET dolg = 0
        WHERE clan.id = ?
        """
    with conn:
        return conn.execute(poizvedba, [id_clana]).lastrowid
