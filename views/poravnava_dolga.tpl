% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Član: <input type="text" name="id_clana" value="{{id_clana}}" /><br />   

<input type="submit" value="Poravnava dolga">
</form>