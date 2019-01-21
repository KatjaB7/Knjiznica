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

#dodaj iskanje po avtorju

@get('/iskanje_knjig/')
def iskanje_knjig():
    niz = request.query.naslov
    idji_knjig = modeli.poisci_knjige(niz)
    knjige = [(id, naslov, opis, avtor, '/knjiznica/{}/'.format(id)) for (id, naslov, opis, avtor) in modeli.podatki_knjig(idji_knjig)]
    return template(
        'rezultati_iskanja_knjige',
        niz=niz,
        knjige=knjige,
)

@get('/iskanje_clanov/')
def iskanje_clanov():
    niz = request.query.ime
    idji_clanov = modeli.poisci_clane(niz)
    clani = [(id,ime, dolg, '/knjiznica/{}/'.format(id)) for (id, ime, dolg) in modeli.podatki_clanov(idji_clanov)]
    return template(
        'rezultati_iskanja_clanov',
        niz=niz,
        clani=clani,
 )

@get('/iskanje_avtorjev/')
def iskanje_avtorjev():
    niz = request.query.ime
    idji_avtorjev = modeli.poisci_avtorje(niz)
    avtorji = [(id,ime, '/avtorji/{}/'.format(id)) for (id, ime) in modeli.podatki_avtorjev(idji_avtorjev)]
    return template(
        'rezultati_iskanja_avtorjev',
        niz=niz,
        avtorji=avtorji,
 )

@get('/avtorji/<id_avtorja:int>/')
def podatki_avtorja(id_avtorja):
    naslov, opis, avtor, zalozba = modeli.podatki_avtor(id_avtorja)
    return template(
        'podatki_knjige',
        naslov=naslov,
        opis=opis,
        avtorji=avtor,
        zalozbe=zalozba,
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

@get('/clani/<id_clan:int>/')
def podatki_clana(id_clan):
    ime = modeli.podatki_clana(id_clan)
    return template(
        'podatki_clana',
        ime=ime,
    
)


#ko dodaš založbo boma nardili seznam da izbereš med unimo ko so ker itak v primeru 
#da je še ni pač najprej dodaš založbo pa pol ne ....
@get('/dodaj_knjigo/')    
def dodaj_knjigo():
    zalozba = modeli.seznam_zalozb()
    kraj = modeli.seznam_krajev()
    return template('dodaj_knjigo',
                    naslov="",
                    opis="",
                    avtor="",
                    zalozba = "",
                    kraj = "",
                    napaka=False)

@post('/dodaj_knjigo/')
def dodajanje_knjige():
    try:
        id = modeli.dodaj_knjigo(naslov=request.forms.naslov,  
                                opis=request.forms.opis,
                                avtor=request.forms.avtor,
                                zalozba=request.forms.zalozba,
                                kraj=request.forms.kraj)
    except Exception as ex: 
        zalozba = modeli.seznam_zalozb()
        kraj = modeli.seznam_krajev()
        return template('dodaj_knjigo',
                            naslov=request.forms.naslov,
                            opis=request.forms.opis,
                            avtor=request.forms.avtor,
                            zalozba=request.forms.zalozba,
                            kraj=request.forms.kraj,
                            napaka=True)
    redirect('/knjiznica/{}/'.format(id)) 



@get('/dodaj_clana/')    
def dodaj_clana():
    return template('dodaj_clana',
                    ime="",
                    dolg = "",
                    napaka=False)

@post('/dodaj_clana/')
def dodajanje_clana():
    try:
        id = modeli.dodaj_clana(request.forms.ime)
    except Exception as ex: 
        return template('dodaj_clana',
                            ime=request.forms.ime,
                            #dolg = request.forms.dolg,
                            napaka=True)
    redirect('/clani/{}/'.format(id)) 

run( reloader = True, debug= True)


                               