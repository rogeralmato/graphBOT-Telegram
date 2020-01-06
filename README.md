# QUIZBOT  - Pràctica LP 2019/20 Q1 

Pràctica de compiladors i bot de Telegram per l'assignatura de llenguatges de programació de la UPC. Per realitzar la part de compiladors s'ha utilitzat ANTLR4 i Python3 per la part del bot de Telegram. La pràctica consisteix en compilar una enquesta (en un format establert i guardada en format .txt) de manera que se'n extreu tota la informació necessària per tal de que els usuaris la pugin respondre a través de un bot de Telegram. Les característiques del compilador i del bot s'estudiaran en detall a continuació. 


## Instal·lació

Aquestes instruccions et baixaran una còpia del projecte apunt per córrer a la teva màquina local. 

### Prerequisits

Per l'execució del bot es encessita **python3** i **pip3** per la instal·lació d'extencions i llibreries. En cas de no tenir-ho instal·lat, el següent [enllaç](https://realpython.com/installing-python/) explica detalladement com instal·lar-ho. Per la part de compiladors es necessita **ANTLR4**, que es pot instal·lar [aquí](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md). 

```
python3
```
```
pip3
```
```
antlr4
```
### Instal·lació del Bot

Per instal·lar descomprimim el fitxer **.zip**. Un cop a dins la carpeta:

```
pip3 install -r requirements.txt
```
Per la part de compiladors, amb ANTLR4 instal·lat a la màquina és suficient. Un cop finalitzat, ja es podrà executar.

### Execució del Bot

Per executar el bot:

```
python3 bot.py
```

## Tests
_* Remarcar que aquests tests de a continuació del bot s'han realitzat amb l'enquesta facilitada en la presentació de la pràctica. En el següent apartat s'estudia a fons el funcionament del compilador d'enquestes i del bot en si._

Un cop ja tenim el bot funcionant, des de Telegram podrem executar-lo fent click a **start**. El que observarem serà el següent:

<p align="center">
  <img width="400" src="https://i.ibb.co/k1B2cjK/Screenshot-2020-01-06-at-14-59-48.png">
</p>

Amb la opció **/help** observem totes les funcionalitats del bot:
<p align="center">
  <img width="400" src="https://i.ibb.co/pKryzD2/Screenshot-2020-01-06-at-15-10-39.png">
</p>

La primera funcionalitat és **/author** per veure les dades de l'autor del projecte:
<p align="center">
  <img width="400" src="https://i.ibb.co/0XwjkXN/Screenshot-2020-01-06-at-15-14-26.png">
</p>

La segona funcionalitat seria realitzar alguna de les enquestes compilades amb el compilador. Aqui és important posar bé el nom de l'enquesta compilada ja que de l'altre manera no podrem realitzar l'enquesta ni veure els resultats. En aquesta part s'ha intentat desenvolupar el bot per tal de ser escalable pel que fa el nombre d'usuaris que responen l'enquesta i també pel que fa el nombre d'enquestes. És a dir, mitjançant el bot usuaris diferents podrien estar realitzant enquestes diferents. Cada enquesta està identificada amb un **idEnquesta** definida al compilar l'enquesta.

Si posem malament el nom de l'enquesta, podem obserar com se'ns mostren el nom de les enquestes disponibles:
<p align="center">
  <img width="400" src="https://i.ibb.co/HxPX1cm/Screenshot-2020-01-06-at-15-23-00.png">
</p>

Observem doncs com se'ns informa que hi ha l'enquesta amb nom _E_ per respondre:


<p align="center">
  <img src="https://i.ibb.co/VQFkCRq/Screenshot-2020-01-06-at-15-25-27.png" width="350" />
  <img src="https://i.ibb.co/2gsK8z8/Screenshot-2020-01-06-at-15-38-22.png" width="350" /> 
</p>

Un cop finalitzada l'enquesta, podem seguir amb les diferents funcionalitats del bot per veure les respostes dels usuaris. 

La primera és mostrar un report amb **/report** de les respostes de tots els usuaris sobre les preguntes.

<p align="center">
  <img width="400" src="https://i.ibb.co/PQd3LsC/Screenshot-2020-01-06-at-16-29-53.png">
</p>

Finalment també es pot mostrar una gràfica en format _pie_ amb **\pie idpregunta** o en format _gràfic de barres_ amb **\bar idPregunta**.
<p align="center">
  <img src="https://i.ibb.co/Wyr04qn/Screenshot-2020-01-06-at-16-44-21.png" width="350" />
  <img src="https://i.ibb.co/7N5TRL9/Screenshot-2020-01-06-at-16-44-35.png" width="350" /> 
</p>


## Explicació teòrica

### COMPILADOR

La part de compiladors està realitzada amb `antlr4`i `python3`. En el fitxer **Enquestes.g** hi ha tota la gramatica definida. Està pensada per ser escalabla a nivell de preguntes. 
Observem la part lèxica:

```
COMA: ','  ;
INICLAU: '[' ;
FICLAU: ']' ;
INIPAR: '(' ;
FIPAR: ')' ;
SEMICOLON: ';' ;
TWODOTS : ':' ;
NAME: [A-Z]+ ;
FRASE: WORD (SPACE WORD)* ;
WORD: [A-Za-zéèàáíìòóùúüï'́ı]+ ;
INT: [0-9]+ ;
SPACE: ' ' ;
WS : [\t\r\n]+ -> skip ;
```
I el parser:
```
grammar Enquestes;
root : expr?  'END' EOF;
expr : (pregunta | resposta | item | alternativa)*  infoEnquesta ;

pregunta: idPregunta TWODOTS SPACE 'PREGUNTA'  frasePregunta ;
frasePregunta: FRASE '?'; 
idPregunta: 'P' INT ;

resposta: idResposta TWODOTS SPACE 'RESPOSTA' llistaRespostes+ ;
idResposta: 'R' INT ;
llistaRespostes: INT TWODOTS contingutResposta ;
contingutResposta: SPACE FRASE SPACE SEMICOLON;

item: idItem TWODOTS SPACE 'ITEM' relacioItem ;
relacioItem: idPregunta SPACE '->' SPACE idResposta ;
idItem: 'I' INT ;

alternativa: idalternativa TWODOTS SPACE 'ALTERNATIVA' contingutAlternativa ;
idalternativa: 'A' INT ;
contingutAlternativa: idItem SPACE INICLAU contingutClaus* FICLAU ;
contingutClaus: COMA? INIPAR INT COMA 'I' INT FIPAR ;

infoEnquesta: NAME TWODOTS SPACE 'ENQUESTA' contingutEnquesta? ;
contingutEnquesta: idItem (SPACE idItem)* ;
```
Observem que s'ha realitzat `->` skip dels tabs i enters, mentre que s'han tingut en compte els espais ja que alhora de persejar els espais facilita la feina al compilador. Remarcar també que totes les imatges i dades es guarden amb nom finalitzat __idEnquesta_. Per exemple, l'enquesta facilitada per l'assignatura un cop compilada crearà els fitxers `imgGraph_E.png` amb una imatge del graf de l'enquesta i `graph_E`amb les dades del graf.

Observem el resultat de `imgGraph_E.png`:

<p align="center">
  <img width="400" src="https://i.ibb.co/Zc22Zyy/Figure-1.png">
</p>

Els arcs negres indiquen la seqüència de preguntes, els arcs blaus relacionen les preguntes amb les respostes que s'ha d'utilitzar per respondre la pregunta i finalment els arcs verds indiquen un extensió de l'enquesta si es respon una pregunta en concret.

Un altre exemple de graph seria per una enquesta buida:
```
B: ENQUESTA
END
```
<p align="center">
  <img width="400" src="https://i.ibb.co/MM9zdMy/img-Graph-B.png">
</p>

#### Compilar gramàtica i executar-la amb fitxers .txt
Per compilar la gramàtica s'ha utlitzat:  
```
antlr4 -Dlanguage=Python3 -no-listener -visitor Enquestes.g
```
Per utilitzar el compilador per compilar una enquesta guardada per exemple en un fitxer `input.txt`:
```
python3 test.llegirEnquesta.py input.txt
```
El fitxer `test.llegirEnquesta.py` llegeix el fitxer d'entrada i utilitza el compilador per extreure la informació mitjançant `EnquestesVisitor.py` (veure codi fitxer) i després generar els fitxer `imgGraph_<idEnquesta>.png` i `graph<idEnquesta>` (fitxer de dades de l'enquesta) .



### TELEGRAM BOT

Per la part del Bot de Telegram, s'ha registrat el bot en @BotFather, seguint les instruccions de l'assignatura del [enllaç](https://lliçons.jutge.org/python/telegram.html). Observant el _main_ del `bot.py` podem observar el seu conjunt de dispatchers (\key per la qual s'executa una funció definida del bot). També podem observar l'ús de _ConversationHandler_ per tal de gestionar els inputs dels usuaris alhora de respondre les preguntes de l'enquesta.

```
if __name__ == '__main__':

    # declara una constant amb el access token que llegeix de token.txt
    TOKEN = open('.token.txt').read().strip()

    # crea objectes per treballar amb Telegram
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    #  funcions que es poden executar des del telegram
    dispatcher.add_handler(CommandHandler('start', start,pass_user_data=True))
    dispatcher.add_handler(CommandHandler('author', author))
    dispatcher.add_handler(CommandHandler('pie', pie,pass_user_data=True))
    dispatcher.add_handler(CommandHandler('bar', bar,pass_user_data=True))
    dispatcher.add_handler(CommandHandler('report', report,pass_user_data=True))
    dispatcher.add_handler(CommandHandler('help', help))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('quiz', quiz,pass_user_data=True)],

        states={ 

            PREGUNTA: [MessageHandler(Filters.text, pregunta,pass_user_data=True)]

        },

        fallbacks=[CommandHandler('cancel', quiz)]
    )

    dispatcher.add_handler(conv_handler)

    # engega el bot
    updater.start_polling()

    updater.idle()
```

Remarcar que en el fitxer `bot.py` només hi ha les funcions que pot executar l'usuari mitjançant l'execució del bot. En el fitxer `funcionsBot.py`es troben la resta de funcions utilitzades pel bot, d'aquesta manera si mai s'han d'ampliar les funcionalitats del bot, es podrà fer de manera senzilla i neta. 

Quan es crida des del bot `/quiz <idEnquesta>` el procediment és el següent:
1. Es comprova que existeixi un fitxer `graph_<idEnquesta>` , en cas contrari es mostra a l'usuari les enquestes disponibles.
2. Es llegeix el fitxer `graph_<idEnquesta>` i es guarda en un altre `data_<idEnquesta>.pickle`. En cas de que ja s'hagi llegit i creat el fitxer `data<idEnquesta>.pickle` previament, no es tornar a llegir per millorar l'eficiencia. Es realitza mitjançant la funció _readData_ de `funcionsBot.py`.
```
def readData(nomFitxer, nomGraph):
    G = nx.read_gpickle(nomGraph)
    preguntes = llegirPreguntes(G)
    try:
        with open(nomFitxer, 'rb') as handle:
            data = pickle.load(handle)
    except Exception:
        data = {}
        for p in preguntes:
            data[p] = llegirPreguntaEspecifica(G,p)
        with open(nomFitxer, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return data

```
3. Es començar a realitzar l'enquesta a l'usuari amb les dades llegides de `data_<idEnquesta>.pickle`

#### Fitxer de dades
Per tal de mantenir la coherència de les dades, mentre l'usuari va responent les preguntes es van guardant les respostes en una còpia del fitxer a `user_data['data']` i quan finalitza l'enquesta s'actualitzen al fitxer `data_<idEnquesta>.pickle`. D'aquesta manera un altre usuari podria està realitzant una altra enquesta o visualitzant les respostes sense cap mena de problema. 

Aquest fitxer de dades es crea quan es llegeix la informació del graf per primer cop comentada abans `graph_<idEnquesta>`. L'estructura del fitxer és en forma de diccionari. Per cadascuna de les preguntes de l'enquesta trobem una entrada en forma de llista. 

Cada entrada del diccionari té una llista amb 3 elements de la forma següent:

<p align="center">
  <img width="600" src="https://i.ibb.co/DgPfrpk/Screenshot-2020-01-06-at-20-31-51.png">
</p>

* El primer element conté una tupla amb:
	* `Px`Com identificador de la pregunta actual.
	* `'Text pregunta Px'` conté la pregunta en format `string`.
* El segon element conté una tupla amb quatre elements:
	* `'Rx'` Com identificador de la resposta.
	* `[llista amb les respostes]` Llista de les respostes de _Rx_.  	 
	* `[llista respostes usuaris]` Llista amb les respostes dels usuaris sobre la resosta _Rx_.
	* `[Llisa identificadors resposta]` Una llista amb els identificadors que identifiquen cadascuna de les respostes possibles de _Rx_. És a dir, una resposta amb possibles respostes: 1: Si, 2: No , tindria [1,2] en aquest apartat. 
* El tercer element conté una llista de tuples amb les següents preguntes i les respostes de la resposta _Rx_ acutal que et porten a la pregunta corresponent. 
	* `Py` Pregunta amb identificador `Py`
	* `Intenger` que identifica la resposta per anar a la pregunta `Py`. En cas de que qualsevol resposta porti a la pregunta `Py`hi haurà _-1_ en aquest camp. 

D'aquesta manera, un cop ja s'hagi respos unes quantes vegades l'enquesta proposada com exemple de la pràctica, el fitxer `data_E.pickle` tindrà l'aspecte següent:

```
{'P1': [('P1', 'Quants adults viuen a casa teva?'), ('R1', [' zero', ' un', ' dos', ' més de dos'], [5, 4, 0, 4], [0, 1, 2, 3]), [('P2', -1)]], 
'P2': [('P2', 'Quants menors vien a casa teva?'), ('R1', [' zero', ' un', ' dos', ' més de dos'], [2, 6, 2, 3], [0, 1, 2, 3]), [('P3', -1)]], 
'P3': [('P3', 'Com vas a la feina majoritàriament?'), ('R3', [' caminant', ' en cotxe', ' en transport públic'], [8, 3, 2], [1, 2, 3]), [('P4', '2'), ('P5', '3'), ('END', -1)]], 
'P4': [('P4', 'Utilitzes car sharing?'), ('R4', [' Sı́', ' No'], [1, 2], [1, 2]), []],
'P5': [('P5', 'Quin mitja de transport utilitzes majoritàriament?'), ('R5', [' Tren', ' Bus', ' Metro', ' Altres'], [0, 1, 1, 0], [1, 2, 3, 4]), []]}
```

Com que per cada pregunta tenim una llista de les següents preguntes a executar pel bot, en funció de les respostes de cada usuari, per cada usuari definim una cua `user_data['queue]` on s'hi afegeix aquesta llista de possibles següents preguntes. Això permet una manera eficient d'implementar una estructura de dades amb totes les preguntes que li queden per respondre a l'usuari que es va actualitzant a mesura que l'usuari respon les preguntes. 
## Built With

* [Python3](https://www.python.org/download/releases/3.0/) - Python3 Official Site
* [ANTLR4](https://www.antlr.org/) - Compiler
* [Telegram](https://core.telegram.org/bots/api) - Telegram Bot API


## Authors

* **Roger Almató Baucells** - *Initial work* - [GraphBot](https://gebakx.github.io/QuizBot/)





