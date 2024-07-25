# Meiro preview project
## Uvod
Dobry den, dlouho jsem uvazoval, ktery projekt Vam zaslat  na ukazku, programator se v case vyviji a meni sve postupy.
Nakonec jsem dospel k ukazce projektu Evidenta.

O co jde?

Bude to liteweight CRM pro ucetni kancelare. Z praxe jsem zazil, ze mensi ucetni firmy maji potize s organizaci dat,
uschovou pristupovych udaju, notifikaci zakazniku atd atd atd. Tak proc nepouzit nejake CRM? No jo, ale vetsina reseni 
je velice draha a zbytecne komplikovana - proto Evidenta. Radi bychom poskytli nastroj, ktery ucetni nezruinuje a 
pomuze ji s jeji denni rutinou.

Dovolil jsem si Vam zaslat cast tohoto projektu.

Proc jenom cast?

Protoze nektere modely jsem nepsal ja a nektere nejsou hotove. I v teto casti jsem poslal kod, ktery neni na 100% hotov,
ale verim, ze z nej pujde dostatecne videt, jestli za neco stojim, ci nikoliv.

Co teda je a co neni?

User - model, servisa hotova, aktualne se upravuje api, ale query cast je hotova
Company - v zakladu done, ale musi se jeste dost upravit servisa, manager atd. Pridal jsem ji jenom kvuli kompletnosti


Bohuzel stale tam jeste existuji ruzne exceptiony atd, jako pozustatek byvaleho kodu. Aktualne kvuli zpetne kompatibilite
jsem je tam musel ponechat. Nicmene v User app asi uvidite, jakym smerem se budou dalsi apps ubirat.


## Co chci timto projektem ukazat?
Pevne verim, ze na tomto mikroprojektu dokazu predvest nejenom sve programatorske schopnosti, ale take me schopnosti v
devops a vecech okolo vyvoje.

## Filosofie
1. keep it simple - to se snazime ukazat hlavne v User app
2. pokud kod potrebuje docstring, je to spatne srozumitelny kod a je lepsi ho prepsat
3. pokud existuje radek, ktery se nepokryva testy, tak je otazka, jestli by takovy radek mel existovat

## Co pouzivam a jak to funguje?
1. cely projekt je vyvijen za pomoci frameworku Django + graphql api
2. vse se snazime pokryt testy psane pomoc pytest s obcasnim vyuzitim funkcionalit z unittest.mock
3. requirements generuji pomoci piptools, ale planuji prechod na Rye a UV
4. code style kontroluju pomoci isort, black a ruff. Vse zabalene v pre-commit hooku
5. cely projekt se snazim definovat v pyproject.toml
6. cela pipeline je nasledne definovana v GitHub actions - testy, code style,...
7. za beznych okolnost jedeme na postgresql, ale v ramci zjednoduseni jsem to prenastavil na sqlite3

## Jak to pustim?
1. vytvorit a aktivovat .venv
2. pip install -r requirements.txt
3. pip install -r requirements-dev.txt
4. python3 manage.py migrate
5. python3 manage.py runserver
6. bude si potreba v konzoli vyrobit superusera - zatim jsem nestihl dat do initial data

