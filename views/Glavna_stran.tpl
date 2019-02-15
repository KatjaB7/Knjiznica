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

