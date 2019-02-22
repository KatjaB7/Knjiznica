% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Član: <select multiple name="id_clan">
% for id, ime in vsi_clani:
    <option value="{{id}}" {{'selected' if str(id) in id_clan else ''}}>{{ime}}</option>
% end
</select>
<br />

Knjiga: <select multiple name="id_knjiga">
% for id, naslov in vse_knjige:
    <option value="{{id}}" {{'selected' if str(id) in id_knjiga else ''}}>{{naslov}}</option>
% end
</select>
<br />



<input type="submit" value="Dodaj izposojo">
</form>

<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>