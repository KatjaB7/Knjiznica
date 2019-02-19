% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, naslov, opis, avtor, url) in knjige:
    <li><a href="{{ url }}">{{ naslov }} ({{ opis }}) ({{ avtor }})</a></li>
% end
</ul>

 <!-- Add icon library -->
<link rel="stylesheet" href="http://127.0.0.1:8080/">

<!-- Add font awesome icons to buttons  -->
<button class="btn"><i class="fa fa-home"></i></button>


