% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Knjiga: <input type="text" name="id_izposoje" value="{{id_izposoje}}" /><br />   


<input type="submit" value="Dodaj vracilo">
</form>