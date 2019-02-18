% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Zalozba: <input type="text" name="zalozba" value="{{zalozba}}" /><br />  
Kraj zalozbe: <input type="text" name="kraj" value="{{kraj}}" /><br />   


<input type="submit" value="Dodaj zalozbo">
</form>