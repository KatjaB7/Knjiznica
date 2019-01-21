% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, naslov, opis, avtor, url) in knjige:
    <li><a href="{{ url }}">{{ naslov }} ({{ opis }}) ({{ avtor }})</a></li>
% end
</ul>