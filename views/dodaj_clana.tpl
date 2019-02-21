% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Ime in priimek: <input type="text" name="ime_clana" value="{{ime_clana}}" /><br />


<input type="submit" value="Dodaj clana">
</form>