% rebase('osnova')


<h1 class="title is-3 is-spaced"">Dobrodošli v knjižnici Katje in Zale </h1>
<p>
V najini knjižnici vam je na voljo {{ st_knjig }} knjig z raznoliko tematiko, med katerimi lahko izbirate. 
Vedno znova posodabljamo vsebine in smo s knjigami 'on track' za vse vrste knjižnih moljev.
</p>
<p>
Vabimo vas, da se včlanite v našo knjižnico, ki ima do sedaj že {{ st_clanov }} članov in postanete del nas. 
Veselo brskanje in branje.
</p>
Knjižnica K&Z.
</p>

&nbsp

<p>
Iskanje knjig po naslovu:
</p>
<form action="iskanje_knjig/" method="get">
<input type="text" name="naslov" value="" />
<input type="submit" value="Išči">
</form>


<p>
Iskanje knjig, glede na avtorja:
<form action="iskanje_avtorjev/" method="get">
<input type="text" name="ime" value="" />
<input type="submit" value="Išči">
</form>
</p>


&nbsp

<ul>
    % if get('prijavljen', False):
    <li>
        <p>
        Na voljo vam je iskanje članov, kjer lahko preverite vaše stanje in katere knjige imaste izposojene:
        <form action="iskanje_clanov/" method="get">
        <input type="text" name="ime" value="" />
        <input type="submit" value="Išči">
        </form>
        </p>

        &nbsp

    </li>
    <li>
        <a href="dodaj_clana/">Dodaj clana - skrbnik</a>
    </li>
     <li>
        <a href="dodaj_knjigo/">Dodaj knjigo - skrbnik</a>
    </li>
     <li>
        <a href="dodaj_izposojo/">Izposoja - skrbnik</a>
    </li>
      <li>
        <a href="dodaj_vracilo/">Vracilo - skrbnik</a>
    </li>
      <li>
        <a href="poravnava_dolga/">Poravnava dolga - skrbnik</a>
    </li>
    &nbsp
    <li>
        <a href="odjava/">Odjavi se</a>
    </li>
    % end
</ul>

&nbsp

% if not get('prijavljen', False):
<form action="prijava/" method="post">

<p>
Za pregled vašega stanja se morate prijaviti.
</p>

&nbsp

<p>
Prijavite se tukaj:
</p>
<p>
Uporabniško ime:
<input type="text" name="uporabnisko_ime" value="" />
Geslo:
<input type="password" name="geslo" value="" />
<input type="submit" value="Prijavi se">
</p>
</form>
<form action="registracija/" method="post">

&nbsp

<p>
Če še niste registrirani se najprej registrirajte!
</p>
<p>
Uporabniško ime:
<input type="text" name="uporabnisko_ime" value="" />
Geslo:
<input type="password" name="geslo" value="" />
<input type="submit" value="Registriraj se">
</p>
</form>
% end