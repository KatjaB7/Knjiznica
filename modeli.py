<<<<<<< HEAD
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
    return st_clanoc


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
                 JOIN knjiga ON avtor.id = knjiga.id_avtorja
            WHERE knjiga.id_avtorja = ?
        """
        cur.execute(poizvedba_za_avtorja, [id_knjige])
        avtorji = [vrstica[0] for vrstica in cur.fetchall()]
        poizvedba_za_zalozbo = """
            SELECT zalozba.ime
            FROM zalozba
                 JOIN knjiga ON zalozba.id = knjiga.id_zalozbe
            WHERE knjiga.id_zalozbe = ?
        """
        cur.execute(poizvedba_za_vloge, [id_knjige])
        zalozbe = cur.fetchall()
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


def id_zalozbe(zalozba, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podane založbe.
    Če založba še ne obstaja, jo doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM zalozba WHERE ime = ?", [zalozba]).fetchone() 
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO zalozba (ime, kraj) VALUES (?, ?)", [zalozba]).lastrowid #popravit []
    else:
        return None


def dodaj_knjigo(naslov, opis, id_avtorja, id_zalozbe):
    """
    V bazo doda knjigo ter njen opis, IDavtorja in IDknjige.
    """
    with conn:
        id = conn.execute("""
            INSERT INTO knjiga (naslov, opis, id_avtorja, id_zalozbe)
                            VALUES (?, ?, ?, ?)
        """, [naslov, opis, id_avtorja(avtor, True), id_zalozbe(zalozba, True)]).lastrowid

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


def podatki_clana(id_clana):#dodaj še seznam izposojenih knjig
    """
    Vrne podatke o članu z danim IDjem.
    """
    poizvedba = """
        SELECT ime, dolg FROM clan WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_clana])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        ime, dolg = osnovni_podatki
        return ime, dolg
    poizvedba_za_KNJIGE = """
            SELECT knjiga.ime
            FROM knjiga
                 JOIN izposoja ON izposoja.id_knjige = knjiga.id
            WHERE knjiga.id_zalozbe = ?
        """
    cur.execute(poizvedba_za_vloge, [id_knjige])
    zalozbe = cur.fetchall()

def dodaj_clana(id_clana, ime_clana, dolg_clana = 0 ): #bo to 0
    poizvedba = """
        INSERT INTO clan
        (id, ime, dolg)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_clana, ime_clana, dolg_clana])


def dodaj_izposojo(id_clan, id_knjiga): #je ok?
    poizvedba = """
        INSERT INTO izposoja
        (datum_izposoje, rok_vracila, id_clana, id_knjige)
        VALUES (date('now'), date('now', '+21 days'), ?, ?)
    """
    with conn:
        return conn.execute(poizvedba, [id_clan, id_knjiga]).lastrowid

def dodaj_vracilo(id_izposoje, id_clan, id_knjiga): # ?????
    poizvedba = """
        UPDATE izposoja
        SET datum_vracila = date('now')
        WHERE id = ?


        """

=======
import baza
import sqlite3

conn = sqlite3.connect('filmi.db')
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
    return st_clanoc


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
                 JOIN knjiga ON avtor.id = knjiga.id_avtorja
            WHERE knjiga.id_avtorja = ?
        """
        cur.execute(poizvedba_za_avtorja, [id_knjige])
        avtorji = [vrstica[0] for vrstica in cur.fetchall()]
        poizvedba_za_zalozbo = """
            SELECT zalozba.ime
            FROM zalozba
                 JOIN knjiga ON zalozba.id = knjiga.id_zalozbe
            WHERE knjiga.id_zalozbe = ?
        """
        cur.execute(poizvedba_za_vloge, [id_knjige])
        zalozbe = cur.fetchall()
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


def id_zalozbe(zalozba, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podane založbe.
    Če založba še ne obstaja, jo doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM zalozba WHERE ime = ?", [zalozba).fetchone() 
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO zalozba (ime, kraj) VALUES (?, ?)", [zalozba]).lastrowid #popravit []
    else:
        return None


def dodaj_knjigo(naslov, opis, id_avtorja, id_zalozbe):
    """
    V bazo doda knjigo ter njen opis, IDavtorja in IDknjige.
    """
    with conn:
        id = conn.execute("""
            INSERT INTO knjiga (naslov, opis, id_avtorja, id_zalozbe)
                            VALUES (?, ?, ?, ?)
        """, [naslov, opis, id_avtorja(avtor, True), id_zalozbe(zalozba, True)]).lastrowid

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


def podatki_clana(id_clana):#dodaj še seznam izposojenih knjig
    """
    Vrne podatke o članu z danim IDjem.
    """
    poizvedba = """
        SELECT ime, dolg FROM clan WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_clana])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        ime, dolg = osnovni_podatki
        return ime, dolg


def dodaj_clana(id_clana, ime_clana, dolg_clana = 0 ):
    poizvedba = """
        INSERT INTO clan
        (id, ime, dolg)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_clana, ime_clana, dolg_clana])


def dodaj_izposojo(id_izposoje, id_clan, id_knjiga): #je ok?
    poizvedba = """
        INSERT INTO izposoja
        (id, datum_izposoje, rok_vracila, id_clana, id_knjige)
        WHERE datum_izposoje = datetime.datetime.today() 
        AND rok_vracila = datetime.datetime.today() + datetime.timedelta(days=21)
        VALUES (?, datum_izposoje, rok_vracila, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_izposoje, id_clan, id_knjiga])

def dodaj_vracilo(id_izposoje, id_clan, id_knjiga): # ?????
    poizvedba = """
        INSERT INTO izposoja
        """
>>>>>>> 510ebc593fedd40dff3fe5f3dd68e0e18711f142
