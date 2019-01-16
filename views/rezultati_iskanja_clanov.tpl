% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, ime, dolg, url) in clani:
    <li><a href="{{ url }}">{{ ime }} ({{ dolg }})</a></li>
% end
</ul>