% rebase('osnova')

% if napaka:
<p>Knjiga ni izposojena!</p>
% end

<form method="post">
Knjiga: <select multiple name="id_knjige">
% for id, naslov in vse_knjige:
    <option value="{{id}}" {{'selected' if str(id) in id_knjige else ''}}>{{naslov}}</option>
% end
</select>
<br />

<input type="submit" value="Dodaj vracilo">
</form>


<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>