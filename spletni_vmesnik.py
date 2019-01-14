import bottle
from bottle import get, post, run, template, request, redirect
import modeli
import hashlib

def url_knjiznice(id):
    return '/knjiznica/{}/'.format(id)

@get('/')
def glavna_stran():
    st_knjig = modeli.stevilo_knjig()
    st_clanov = modeli.stevilo_clanov()
    return template('Glavna_stran',
                    st_knjig = st_knjig,
                    st_clanov = st_clanov
                    )



@get('/iskanje_knjig/')
def iskanje_knjig():
    niz = request.query.naslov
    idji_knjig = modeli.poisci_knjige(niz)
    knjige = [(id, naslov, opis, '/knjiznica/{}/'.format(id)) for (id, naslov, opis) in modeli.podatki_knjig(idji_knjig)]
    return template(
        'rezultati_iskanja_knjige',
        niz=niz,
        knjige=knjige,
)

@get('/knjiznica/<id_knjige:int>/')
def podatki_knjige(id_knjige):
    naslov, opis, avtor, zalozba = modeli.podatki_knjige(id_knjige)
    return template(
        'podatki_knjige',
        naslov=naslov,
        opis=opis,
        avtorji=avtor,
        zalozbe=zalozba,
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

@get('/dodaj_knjigo/')    
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
    redirect('/knjiznica/{}/'.format(id)) 



bottle.run(reloader=True)
                               