% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, ime, url) in avtorji:
    <li><a href="{{ url }}">{{ ime }} </a></li>
% end
</ul>


<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>