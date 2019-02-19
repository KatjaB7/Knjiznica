% rebase('osnova')


<h1 class="title is-3 is-spaced"">Dobrodošli v knjižnici Katje in Zale </h1>
<p>
V najini knjižnici vam je na voljo {{ st_knjig }}knjig z raznoliko tematiko, med katerimi lahko izbirate. 
Vedno znova posodabljamo vsebine in smo z knjigami 'on track' za vse vrste knjižnih moljev.
</p>
<p>
Vabimo vas da se včlanite v našo knjižnico, ki ima do sedaj že {{ st_clanov }} članov in postanete del nas. 
Veselo brskanje in branje.
</p>
Knjižnica K&Z.
</p>

<p>
Na voljo vam je tudi iskanje knjig po naslovu:
</p>
<form action="iskanje_knjig/" method="get">
<input type="text" name="naslov" value="" />
<input type="submit" value="Išči">
</form>


<p>
Na voljo vam je tudi iskanje knjig, glede na avtorja:
</p>
<form action="iskanje_avtorjev/" method="get">
<input type="text" name="ime" value="" />
<input type="submit" value="Išči">
</form>

<p>
Na voljo vam je tudi iskanje članov, kjer lahko preverite vaše stanje:
</p>
<form action="iskanje_clanov/" method="get">
<input type="text" name="ime" value="" />
<input type="submit" value="Išči">
</form>

<p>
<a href="dodaj_knjigo/">Dodaj knjigo</a>
</p>

<p>
<a href="dodaj_clana/">Dodaj clana</a>
</p>

<p>
<a href="dodaj_zalozbo/">Dodaj zalozbo</a>
</p>

<ul>
    % if get('prijavljen', False):
    <li>
        <a href="dodaj_clana/">Dodaj clana v knjižnico -včlanitev</a>
    </li>
     <li>
        <a href="dodaj_knjigo/">Dodaj knjigo v knjižnico</a>
    </li>
     <li>
        <a href="dodaj_zalozbo/">Dodaj zalozbo</a>
    </li>
    <li>
        <a href="odjava/">Odjavi se</a>
    </li>
    % end
</ul>

<p>
</p>

% if not get('prijavljen', False):
<form action="prijava/" method="post">
<p>
Uporabniško ime:
<input type="text" name="uporabnisko_ime" value="" />
</p>
<p>
Geslo:
<input type="password" name="geslo" value="" />
<input type="submit" value="Prijavi se">
</p>
</form>

<form action="registracija/" method="post">
<p>
Če še niste registrirani se najprej registriraj!
</p>
<p>
Uporabniško ime:
<input type="text" name="uporabnisko_ime" value="" />
<p>
Geslo:
<input type="password" name="geslo" value="" />
<input type="submit" value="Registriraj se">
</p>
</form>
% end