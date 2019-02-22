% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, naslov, opis, avtor, url) in knjige:
    <li><a href="{{ url }}">{{ naslov }} ({{ opis }}) </a></li>
% end
</ul>



<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>

  

 