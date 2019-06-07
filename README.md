# graphBot: by Roger Almató

El projecte GraphBot per GEI-LP (edició 2019), realitzat per roger.almato.
Email: roger.almato@est.fib.upc.edu
BotName: **graphBotLP**

### Prerequisits

Per l'execució del bot es encessita **python3** i **pip3** per la instal·lació d'extencions i llibreries. 

```
python3
```
```
pip3
```

### Instal·lació

Per instal·lar descomprimim el fitxer **.zip**. Un cop a dins la carpeta:

```
pip3 install -r requirements.txt
```

Un cop finalitzat, ja es podrà executar.

### Execució

Per executar:

```
python3 main.py
```

## Running the tests

Al executar el bot comença amb l'execució, altrament s'inicia amb **/start**:

![image|40%](https://i.ibb.co/WfCt1Pq/photo6039739447685263308.jpg)

La comanda **/help** mostra totes les opcions del bot:

![image|40%](https://i.ibb.co/WFRyZwy/photo6039739447685263307.jpg)

Per realitzar un exemple, generem un graf amb les ciutats amb més de 50.000 habitans i unim les que estiguin a menys de 300 km. Ho realtzem amb **/graph 300 50000**:

![image|40%](https://i.ibb.co/sRzFVfh/photo6039739447685263306.jpg)

Un cop generat, amb un **/plotpop 1000** podem observar totes les ciutats a 1000km de la posicio de l'usari:

![image|40%](https://i.ibb.co/vxgwDWm/photo6039739447685263305.jpg)

Per veure el graph total, amb **/plotgraph 1000*** ens treura per pantalla el graph amb totes les ciutats a menys de 1000km de l'usari:

![image|40%](https://i.ibb.co/ynNXs3R/photo6039739447685263304.jpg)

També podem trobar la ruta més curta entre dos ciutats. Per exemple **route "Barcelona,es "Amsterdam, pb"** obtenim:

![image|40%](https://i.ibb.co/GvSv958/photo6039739447685263303.jpg)

*Atenció, les dues ciutats han de tenir més habitants que el número indicat alhora de generar el graph*

### Eficiencia en la generació del graf

Per l'eficiencia del programa, hem dividit el món en 72 zones (dividint per 30ª la latitud i la longitud) de la manera següent:

![Image](https://i.ibb.co/prttS9s/world.gif)

La funció CiutatMapa(latitud, longitud), ens retorna a quina de les 72 posicions coorresponen les coordenades. D'aquesta manera quan creem tots els nodes del graf, cada ciutat (forma part de la classe ciutatMapa) es guarda en la zona correponent del vector **MAPA[72]**:
```
def crearNodes(self, poblacio):
        i = 1
        while i <= 72:
            self.MAPA.append([])
            i += 1
        self.FILE["Population"] = self.FILE["Population"].fillna(0)
        df = self.FILE.loc[self.FILE["Population"] >= poblacio]
        for row in df.itertuples(index=True, name='Pandas'):
            cm = CiutatMapa(getattr(row, "City"), getattr(row, "Latitude"), getattr(row, "Longitude"), getattr(row, "Population"), getattr(row, "Country"))
            self.MAPA[posicioMapa(getattr(row, "Latitude"), getattr(row, "Longitude"))].append(cm)
            self.G.add_node(cm)
```

Aquest factor fa que sigui realment eficient quan hem de construïr les arestes del graf. Per cada node del graf només es comproven les ciutats de la mateiza zona, i de les zones del voltant que es pot arribar des de la ciutat actual suman-t'hi la distancia màxima de l'aresta. Per calcular la longitud i la latitud a partir de quilòmetres, s'ha utiitzat el factor de conversió a l'ecuador:
```
    ltC = int(dist / 110.57) + (dist % 110.57 > 0)
    lgC = int(dist / 111.32) + (dist % 111.32 > 0)
```
Quan no ens trobe ma l'ecuador evidentment hi haurà un petit error. Això pot fer que quan siguem als pols potser es comprovi alguna zona que no s'hauria de comprovar (donat que un grau als pols són menys quilòmetres que a l'ecuador), però tot i així mai deixarem de comprovor cap zona necessària. 

```
def addEdges(self, ciutat, distancia):
        ltC = int(distancia / 110.57) + (distancia % 110.57 > 0)
        lgC = int(distancia / 111.32) + (distancia % 111.32 > 0)
        ltI = ciutat.latitude
        lgI = ciutat.longitude
        zonesAMirar = (posicioMapa(ltI, lgI), posicioMapa(ltI + ltC, lgI), posicioMapa(ltI + ltC, lgI), posicioMapa(ltI, lgI + lgC), posicioMapa(ltI, lgI - lgC), posicioMapa(ltI + ltC, lgI - lgC), posicioMapa(ltI - ltC, lgI - lgC), posicioMapa(ltI + ltC, lgI + lgC), posicioMapa(ltI - ltC, lgI + lgC))
        zAM = list(set(zonesAMirar))
        for i in zAM:
            for cm in self.MAPA[i]:
                if ciutat != cm:
                    dist = haversine((ciutat.latitude, ciutat.longitude), (cm.latitude, cm.longitude))
                    if (dist <= distancia):
                        self.G.add_edge(ciutat, cm, weight=dist)
```

## Authors

* **Roger Almató Baucells** - *Initial work* - [GraphBot GEI-LP](https://github.com/jordi-petit/lp-graphbot-2019)




