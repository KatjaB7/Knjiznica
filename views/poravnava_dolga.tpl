% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Član: <select multiple name="id_clana">
% for id, ime in vsi_clani:
    <option value="{{id}}" {{'selected' if str(id) in id_clana else ''}}>{{ime}}</option>
% end
</select>
<br />  

<input type="submit" value="Poravnava dolga">
</form>

<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>