import modeli


MAX_REZULTATOV_ISKANJA = 15


def izberi_moznost(moznosti):
    """
    Funkcija, ki izpiše seznam možnosti in vrne indeks izbrane možnosti.
    Če na voljo ni nobene možnosti, izpiše opozorilo in vrne None.
    Če je na voljo samo ena možnost, vrne 0.
    >>> izberi_moznost(['jabolko', 'hruška', 'stol'])
    1) jabolko
    2) hruška
    3) stol
    Vnesite izbiro > 2
    1
    >>> izberi_moznost([])
    >>> izberi_moznost(['jabolko'])
    0
    """

    if len(moznosti) == 0:
        return
    elif len(moznosti) == 1:
        return 0
    else:
        for i, moznost in enumerate(moznosti, 1):
            print('{}) {}'.format(i, moznost))

        st_moznosti = len(moznosti)
        while True:
            izbira = input('Vnesite izbiro > ')
            if not izbira.isdigit():
                print('NAPAKA: vnesti morate število')
            else:
                n = int(izbira)
                if 1 <= n <= st_moznosti:
                    return n - 1
                else:
                    print('NAPAKA: vnesti morate število med 1 in {}!'.format(
                        st_moznosti))


def izberi_knjigo():
    niz = input('Vnesite del naslova knjige > ')
    idji_knjig = modeli.poisci_knjige(niz)
    moznosti = [
        '{} ({})'.format(naslov, opis) for _, naslov, leto in modeli.podatki_knjig(idji_knjig)
    ]
    izbira = izberi_moznost(moznosti)
    return None if izbira is None else idji_knjig[izbira]


def izberi_clana():
    niz = input('Vnesite del imena clana > ')
    idji_clanov = modeli.poisci_clane(niz)
    moznosti = [
        ime for ime, _, _ in modeli.podatki_clana(ideji_clanov)
    ]
    izbira = izberi_moznost(moznosti)
    return None if izbira is None else idji_clanov[izbira]


def prikazi_podatke_knjige():
    id_knjige = izberi_knjigo()
    if id_knjige is None:
        print('Nobena knjiga ne ustreza iskalnemu nizu.')
    else:
        naslov, opis, avtorji, zalozbe = modeli.podatki_knjige(id_knjige)

        print('{} ({})'.format(naslov))
        print('  je napisal: {} min'.format(avtorji))
        print('  izdala: {}/10'.format(zalozbe))
        print(' kratek opis: {}'.format(opis))

def prikazi_podatke_clana():
    id_clana = izberi_clana()
    if id_clana is None:
        print('Noben član ne ustreza iskalnemu nizu.')
    else:
        ime, dolg, idji_knjig = modeli.podatki_clana(id_clana)
        dolg += modeli.dodaj_dolg(id_clana)
        naslovi_knjig = {
            id_knjige: '{}'.format(naslov)
            for _ , naslov, _
            in modeli.podatki_knjig([id_knjige for id_knjige in idji_knjig])
        }
        print(ime)
        if dolg != 0:
            print('dolg: {}'.format(dolg))
        for id_knjige in idji_knjig:
            print(' izposojene knjige: {}'.format(naslovi_knjig[id_knjige]))


def dodaj_clana():
    id_clana = izberi_clana()
    ime = input('Vnesite ime člana > ')
    modeli.dodaj_clana(id_clana, ime)
    print('Član je uspešno dodan.')

def dodaj_knjigo():
    naslov = input('Vnesite naslov knjige > ')
    opis = input('Vnesite opis knjige > ')
    avtor = input('Vnesite avtorja knjige > ')
    zalozba = input('Vnesite založbo, ki je izdala knjigo > ')
    modeli.dodaj_knjigo(naslov, opis, avtor, zalozba)

def dodaj_izposojo():
    id_clana = izberi_clana()
    id_knjige = izberi_knjigo()
    modeli.dodaj_izposojo(id_clana, id_knjige)

def dodaj_vracilo():
    id_izposoje = izberi_knjigo()
    modeli.dodaj_vracilo(id_izposoje)


def pokazi_moznosti():
    print(50 * '-')
    izbira = izberi_moznost([
        'prikaži podatke knjige',
        'prikaži podatke člana',
        'dodaj člana',
        'dodaj knjigo',
        'vnesi izposojo knjige',
        'vnesi vračilo knjige'
        'izhod',
    ])
    if izbira == 0:
        prikazi_podatke_knjige()
    elif izbira == 1:
        prikazi_podatke_clana()
    elif izbira == 2:
        dodaj_clana()
    elif izbira == 3:
        dodaj_knjigo()
    elif izbira == 4:
        dodaj_izposojo()
    elif izbira == 5:
        dodaj_vracilo()
    else:
        print('Nasvidenje!')
        exit()
        

def main():
    print('Pozdravljeni v bazi knjižnice!')
    while True:
        pokazi_moznosti()


main()