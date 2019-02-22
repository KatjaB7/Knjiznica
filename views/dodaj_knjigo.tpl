% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Naslov: <input type="text" name="naslov" value="{{naslov}}" /><br />
Avtor: <input type="text" name="avtor" value="{{avtor}}" /><br />
Opis: <textarea name="opis">{{opis}}</textarea><br />
Zalozba: <input type="text" name="zalozba" value="{{zalozba}}" /><br />  
Kraj zalozbe: <input type="text" name="kraj" value="{{kraj}}" /><br />   


<input type="submit" value="Dodaj knjigo">

</form>


<form method="get" action="/">
    <button class="btn"><i class="fa fa-home"></i></button>
</form>