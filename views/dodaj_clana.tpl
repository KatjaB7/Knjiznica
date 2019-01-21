% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Ime: <input type="text" name="ime" value="{{ime}}" /><br />


<input type="submit" value="dodaj clana">
</form>