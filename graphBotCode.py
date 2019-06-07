import requests
import io
import gzip
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
import pandas as pd
from fuzzywuzzy import fuzz, process

URL = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/worldcitiespop.csv.gz?raw=true'


class CiutatMapa:
    def __init__(self, nom, lat, long, pb, country):
        self.nom = nom
        self.poblacio = pb
        self.latitude = lat
        self.longitude = long
        self.country = country


class graphBot:

    def __init__(self):
        self.FILE = []
        self.MAPA = []
        self.G = nx.Graph()

    def inicialitzarDades(self):
        r = requests.get(URL)
        bytes_io = io.BytesIO(r.content)
        with gzip.open(bytes_io, 'rt') as read_file:
            self.FILE = pd.read_csv(read_file, usecols=['City', 'Population', 'Latitude', 'Longitude', 'Country'])

    def numNodesGraph(self):
        return self.G.number_of_nodes()

    def numEdgesGraph(self):
        return self.G.number_of_edges()

    def numComponentsGraph(self):
        return nx.number_connected_components(self.G)

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

    def crearGraph(self, distancia):
        for zona in self.MAPA:
            for ciutat in zona:
                self.addEdges(ciutat, distancia)

    def plotPOP(self, dist, latO, longO):
        id = posicioMapa(latO, longO)
        ltC = int(dist / 110.57) + (dist % 110.57 > 0)
        lgC = int(dist / 111.32) + (dist % 111.32 > 0)
        zonesAMirar = (id, posicioMapa(latO + ltC, longO), posicioMapa(latO + ltC, longO), posicioMapa(latO, longO + lgC), posicioMapa(latO, longO - lgC), posicioMapa(latO + ltC, longO - lgC), posicioMapa(latO - ltC, longO - lgC), posicioMapa(latO + ltC, longO + lgC), posicioMapa(latO - ltC, longO + lgC))
        zAM = list(set(zonesAMirar))
        mapa = StaticMap(600, 600)
        for z in zAM:
            for ciutat in self.MAPA[z]:
                if (haversine((ciutat.latitude, ciutat.longitude), (latO, longO)) <= dist):
                    color = 'red'
                    pop = ciutat.poblacio
                    if pop > 2500000:
                        marker = CircleMarker((ciutat.longitude, ciutat.latitude), color, 25)
                    if pop > 1000000:
                        marker = CircleMarker((ciutat.longitude, ciutat.latitude), color, 20)
                    elif pop > 500000:
                        marker = CircleMarker((ciutat.longitude, ciutat.latitude), color, 13)
                    elif pop > 100000:
                        marker = CircleMarker((ciutat.longitude, ciutat.latitude), color, 7)
                    else:
                        marker = CircleMarker((ciutat.longitude, ciutat.latitude), color, 4)
                    mapa.add_marker(marker)

        image = mapa.render()
        image.save('plotpop.png')

    def plotGraph(self, dist, latO, longO):
        id = posicioMapa(latO, longO)
        ltC = int(dist / 110.57) + (dist % 110.57 > 0)
        lgC = int(dist / 111.32) + (dist % 111.32 > 0)
        zonesAMirar = (id, posicioMapa(latO + ltC, longO), posicioMapa(latO + ltC, longO), posicioMapa(latO, longO + lgC), posicioMapa(latO, longO - lgC), posicioMapa(latO + ltC, longO - lgC), posicioMapa(latO - ltC, longO - lgC), posicioMapa(latO + ltC, longO + lgC), posicioMapa(latO - ltC, longO + lgC))
        zAM = list(set(zonesAMirar))
        mapa = StaticMap(600, 600)
        for z in zAM:
            for ciutat in self.MAPA[z]:
                if (haversine((ciutat.latitude, ciutat.longitude), (latO, longO)) <= dist):
                    llistaCities = list(self.G.adj[ciutat])
                    for x in llistaCities:
                        if (haversine((x.latitude, x.longitude), (latO, longO)) <= dist):
                            mapa.add_marker(CircleMarker((ciutat.longitude, ciutat.latitude), 'red', 3))
                            mapa.add_marker(CircleMarker((x.longitude, x.latitude), 'red', 3))
                            mapa.add_line(Line(((x.longitude, x.latitude), (ciutat.longitude, ciutat.latitude)), 'blue', 2))

        image = mapa.render()
        image.save('plotGraph.png')

    def plotRoute(self, src, dst):
        isSRC = False
        isDST = False
        fctSRC = 0
        fctDST = 0
        for zona in self.MAPA:
            for ciutat in zona:
                stringCiutat = str(ciutat.nom) + ", " + str(ciutat.country)
                factor = fuzz.partial_ratio(stringCiutat, src.lower())
                if factor > fctSRC:
                    ciutatSRC = ciutat
                    isSRC = True
                    fctSRC = factor
                factor = fuzz.partial_ratio(stringCiutat, dst.lower())
                if factor >= fctDST:
                    ciutatDST = ciutat
                    isDST = True
                    fctDST = factor

        if (not isSRC) | (not isDST):
            print ("NO")
        else:
            distancia = haversine((ciutatSRC.latitude, ciutatSRC.longitude), (ciutatDST.latitude, ciutatDST.longitude))
            cami = nx.dijkstra_path(self.G, ciutatSRC, ciutatDST)
            mapa = StaticMap(600, 600)
            i = 0
            if len(cami) == 1:
                mapa.add_marker(CircleMarker((cami[i].longitude, cami[i].latitude), 'red', 3))
            else:
                while i < (len(cami)-1):
                    ciutatO = cami[i]
                    ciutatD = cami[i+1]
                    mapa.add_marker(CircleMarker((ciutatO.longitude, ciutatO.latitude), 'red', 3))
                    mapa.add_marker(CircleMarker((ciutatD.longitude, ciutatD.latitude), 'red', 3))
                    mapa.add_line(Line(((ciutatO.longitude, ciutatO.latitude), (ciutatD.longitude, ciutatD.latitude)), 'blue', 2))
                    i += 1
            image = mapa.render()
            image.save('route.png')


def posicioMapa(lt, lg):
    if lt < -90:
        lt += 180
    if lg < -180:
        lg += 360
    if lt > 90:
        lt -= 180
    if lg > 180:
        lg -= 360
    if(lg <= -150):
        Vlg = 0
    elif(lg <= -120):
        Vlg = 1
    elif(lg <= -90):
        Vlg = 2
    elif(lg <= -60):
        Vlg = 3
    elif(lg <= -30):
        Vlg = 4
    elif(lg <= 0):
        Vlg = 5
    elif(lg <= 30):
        Vlg = 6
    elif(lg <= 60):
        Vlg = 7
    elif(lg <= 90):
        Vlg = 8
    elif(lg <= 120):
        Vlg = 9
    elif(lg <= 150):
        Vlg = 10
    else:
        Vlg = 11

    if(lt <= -60):
        Vlt = 5
    elif(lt <= -30):
        Vlt = 4
    elif(lt <= 0):
        Vlt = 3
    elif(lt <= 30):
        Vlt = 2
    elif(lt <= 60):
        Vlt = 1
    else:
        Vlt = 0

    return (Vlt*12 + Vlg)
