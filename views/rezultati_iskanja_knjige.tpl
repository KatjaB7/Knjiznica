% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, naslov, opis, url) in knjige:
    <li><a href="{{ url }}">{{ naslov }} ({{ opis }})</a></li>
% end
</ul>