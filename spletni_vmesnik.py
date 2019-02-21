import bottle
from bottle import get, post, run, template, request, redirect
import modeli
import hashlib

SKRIVNOST = 'moja skrivnost'

def prijavljen_uporabnik():
    return request.get_cookie('prijavljen', secret=SKRIVNOST) == 'da'


def url_knjiznice(id):
    return '/knjiznica/{}/'.format(id)


@get('/')
def glavna_stran():
    st_knjig = modeli.stevilo_knjig()
    st_clanov = modeli.stevilo_clanov()
    return template('Glavna_stran',
                    st_knjig = st_knjig,
                    st_clanov = st_clanov,
                    prijavljen=prijavljen_uporabnik()
                    )

#dodaj iskanje založbe

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
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    niz = request.query.ime
    idji_clanov = modeli.poisci_clane(niz)
    clani = [(id,ime, dolg, '/clani/{}/'.format(id)) for (id, ime, dolg) in modeli.podatki_clanov(idji_clanov)]
    return template(
        'rezultati_iskanja_clanov',
        niz=niz,
        clani=clani,
 )

@get('/iskanje_avtorjev/')
def iskanje_avtorjev():
    niz = request.query.ime
    idji_avtorjev = modeli.poisci_avtorje(niz)
    avtorji = [(id,ime, '/avtorji/{}/'.format(id)) for (id, ime,) in modeli.podatki_avtorjev(idji_avtorjev)]
    return template(
        'rezultati_iskanja_avtorjev',
        niz=niz,
        avtorji=avtorji,
    )


@get('/avtorji/<id_avtorja:int>/')
def podatki_avtorja(id_avtorja):
    ime, naslovi_knjig = modeli.podatki_avtor(id_avtorja)
    return template(
        'podatki_avtor',
        ime = ime, 
        naslovi_knjig = naslovi_knjig,
        )

@get('/izposoja/<id_knjiga:int>/')
def podatki_izposoje(id_knjiga):
    knjiga, clan, datum_izposoje, datum_vracila, rok_vracila = modeli.podatki_izposoje(id_knjiga)
    return template(
        'podatki_izposoje',
        knjiga = knjiga,
        clan = clan,
        datum_izposoje = datum_izposoje, 
        datum_vracila = datum_vracila, 
        rok_vracila = rok_vracila,
)


@get('/knjiznica/<id_knjige:int>/')
def podatki_knjige(id_knjige):
    naslov, opis, avtor, zalozba = modeli.podatki_knjige(id_knjige)
    return template(
        'podatki_knjige',
        naslov=naslov,
        opis=opis,
        avtor=avtor,
        zalozba=zalozba,
)

@get('/clani/<id_clan:int>/')
def podatki_clana(id_clan):
    ime, dolg, idji_knjig = modeli.podatki_clana(id_clan)
    if len(idji_knjig) > 0:
        naslovi = [
            naslov
            for _ , naslov, _, _
            in modeli.podatki_knjig([id_knjige for id_knjige in idji_knjig])
        ]
    else:
        naslovi = "Nobena knjiga ni izposojena."
    return template(
        'podatki_clana',
        ime=ime,
        dolg = dolg,
        naslov = naslovi,    
)

#ko dodaš založbo boma nardili seznam da izbereš med unimo ko so ker itak v primeru 
#da je še ni pač najprej dodaš založbo pa pol ne ....
@get('/dodaj_knjigo/')    
def dodaj_knjigo():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
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
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    try:
        id = modeli.dodaj_knjigo(naslov=request.forms.naslov,  
                                opis=request.forms.opis,
                                avtor=request.forms.avtor,
                                zalozba=request.forms.zalozba,
                                kraj=request.forms.kraj)
    except: 
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
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    return template('dodaj_clana',
                    ime_clana="",
                    #dolg = "",
                    napaka=False)

@post('/dodaj_clana/')
def dodajanje_clana():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    try:
        id = modeli.dodaj_clana(ime_clana =request.forms.ime_clana)
    except: 
        return template('dodaj_clana',
                            ime_clana=request.forms.ime_clana,
                            #dolg = request.forms.dolg,
                            napaka=True)
    redirect('/clani/{}/'.format(id)) 

@get('/dodaj_izposojo/')    
def dodaj_izposojo():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    id_clan = modeli.seznam_clanov()
    id_knjiga = modeli.seznam_knjig()
    return template('dodaj_izposojo',
                    id_clan =[],
                    id_knjiga = [],
                    vsi_clani = id_clan,
                    vse_knjige = id_knjiga,
                    napaka=False)

@post('/dodaj_izposojo/')
def dodajanje_izposoje():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    try:
        id = modeli.dodaj_izposojo(id_clan = request.forms.getall('id_clan'),
                                   id_knjiga = request.forms.getall('id_knjiga'))
    except: #Exception as ex: 
        id_clan = modeli.seznam_clanov()
        id_knjiga= modeli.seznam_knjig()
        return template('dodaj_izposojo',
                        id_clan = request.forms.getall('id_clan'),
                        id_knjiga = request.forms.getall('id_knjiga'),
                        vsi_clani = id_clan,
                        vse_knjige = id_knjiga,
                        napaka=True)
    redirect('/izposoja/{}/'.format(id)) 

get('/dodaj_vracilo/')    
def dodaj_vracilo():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    knjige = modeli.seznam_knjig()
    return template('dodaj_vracilo',
                    id_izposoje = [],
                    vse_knjige = knjige,
                    napaka=False)

@post('/dodaj_vracilo/')
def dodajanje_vracila():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    try:
        modeli.dodaj_vracilo(id_izposoje = request.forms.getall('id_izposoje'))
    except: #Exception as ex: 
        knjige = modeli.seznam_knjig()
        return template('dodaj_vracilo',
                        id_izposoje = request.forms.getall('id_izposoje'),
                        vse_knjige = knjige,
                        napaka=True)
    redirect('/zalozbe/{}/'.format(id)) 

get('/poravnava_dolga/')    
def poravnava_dolga():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    clani = modeli.seznam_clanov()
    return template('poravnavo_dolga',
                    id_clana = request.forms.getall('id_clana'),
                    vsi_clani = clani,
                    napaka=False)

@post('/poravnava_dolga/')
def poravnavanje_dolga():
    if not prijavljen_uporabnik():
        raise bottle.HTTPError(401)
    try:
        id = modeli.poravnava_dolga(id_clana = request.forms.getall('clan'))
    except: #Exception as ex: 
        clani = modeli.seznam_clanov()
        return template('poravnava_dolga',
                        id_clana = request.forms.getall('id_clana'),
                        vsi_clani = clani,
                        napaka=True)
    redirect('/zalozbe/{}/'.format(id))


#prijavaa

@post('/prijava/')
def prijava():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    if modeli.preveri_geslo(uporabnisko_ime, geslo):
        bottle.response.set_cookie(
            'prijavljen', 'da', secret=SKRIVNOST, path='/')
        redirect('/')
    else:
        raise bottle.HTTPError(403, "Niste še registrirani, najprej se registrirajte.")

@get('/odjava/')
def odjava():
    bottle.response.set_cookie('prijavljen', '', path='/')
    redirect('/')

@post('/registracija/')
def registracija():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    if modeli.ustvari_uporabnika(uporabnisko_ime, geslo):
        bottle.response.set_cookie(
            'prijavljen', 'da', secret=SKRIVNOST, path='/')
        redirect('/')
    else:
        raise bottle.HTTPError(
            403, "Uporabnik s tem uporabniškim imenom že obstaja!")

@get('/static/<filename>')
def staticna_datoteka(filename):
    return bottle.static_file(filename, root='static')



run( reloader = True, debug= True)


                               