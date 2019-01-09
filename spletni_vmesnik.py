import bottle
from bottle import get, post, run, template, request, redirect
import modeli
import hashlib

def url_knjiznice(id):
    return '/knjiznica/{}/'.format(id)

moznosti = ['iskanje', 'prikazi podatke knjige', 'dodaj clana', 'dodaj knjigo', 'dodaj izposojo', 
            'dodaj vracilo']

@get('/')
def glavna_stran():
    izbire = [
        (izbira, '/{}/'.format(izbira)) 
        for izbira in moznosti
    ]
    return template(
        'glavna_stran',
        izbire = izbire
    )




@get('/iskanje_knjig/')
def iskanje_knjig():
    niz = request.query.naslov
    idji_knjig = modeli.poisci_knjige(niz)
    knjige = [(id, naslov, opis, '/film/{}/'.format(id)) for (id, naslov, opis) in modeli.podatki_knjig(idji_knjig)]
    return template(
        'rezultati_iskanja',
        niz=niz,
        knjige=knjige,
)


@get('/knjiznica/<id_knjige:int>/')
def podatki_knjige(id_knjige):
    naslov, opis, avtorji, zalozbe = modeli.podatki_knjige(id_knjige)
    return template(
        'podatki_filma',
        naslov=naslov,
        opis=opis,
        avtorji=avtorji,
        zalozbe=zalozbe,
)


@get('/knjiznica/<id_knjige:int>/')
def podatki_clana(id_clan):
    ime, dolg, idji_knjig = modeli.podatki_clana(id_clan)
    return template(
        'podatki_clana',
        naslov=ime,
        dolg=dolg,
        idji_knjig=idji_knjig,
)

@get('/dodaj_knjigo/')    #zakaj rabimo dve ? nisem fix ce rabimo dve 
def dodaj_knjigo():
    return template('dodaj_knjigo',
                    naslov="",
                    opis="",
                    avtor="",)

@post('/dodaj_knjigo/')
def dodajanje_knjige():
    modeli.dodaj_knjigo(naslov=request.forms.naslov,  #preveri
                            opis=request.forms.opis,
                            avtor=request.forms.avtor)
    return template('dodaj_knjigo',
                            naslov=request.forms.naslov,
                            opis=request.forms.opis,
                            avtor=request.forms.avtor)
     redirect('/knjiznica/{}/'.format(id))  #izpis? 



                               