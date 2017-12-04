# README

## Environnement

_presuppose Ubuntu 17.10 -- la preparation des bases de donnees change pour d'autres environements_

Clone / download le repertoire
```
git clone ~/projet_BDA https://github.com/eolecvk/documentDB_analysis.git
```

Installer les dépendance listée dans `requirements.txt`:
```
pip install -r ~/projet_BDA/requirements.txt
```

## Collecte des donnees

1. Creer un compte Twitter ou utiliser un compte existant
2. Enregistrer une [nouvelle application Twitter](https://apps.twitter.com/)
3. Enregistrer les tokens d'authentification dans un nouveau fichier:
4. `~/projet_BDA/source/credentials.py`
```
app_key = 'uwU6y41VPVsZipwqXa3YMT1PC'
app_secret = 'OeVCgEhGJJs4dcHCsJF4bFkjBHu2mWtkuwdw242242gCsUFZA73PRm3'
```
_adapter les valeurs en fonction des tokens d'authentification recu en (2)_
5. Executer la recherche de tweets:
```
python3 ~/projet_BDA/source/search.py {keyword} {save_dir}
```
La valeur de `keyword` determine le mot clef utilise dans la recherche de tweets. La valeur de `savedir` determine le chemin du dossier ou sont enregistres les `.json` tweets.


## Bases de donnees (sur Ubuntu 17.10)

Installer les bases de donnees
```
sudo bash ~/projet_BDA/mymongodb/setup.sh;
sudo bash ~/projet_BDA/mycouchdb/setup_couchdb.sh;
```

Demarrer les bases de donnees
```
sudo bash ~/projet_BDA/mymongodb/start_mongodb.sh;
sudo bash ~/projet_BDA/mymongodb/start_couchdb.sh;
```


## Runtime testing (main)

Executer le programmme de test des bases de donnees:
```
python3 ~/projet_BDA/main.py {save_dir}
```
La valeur de `savedir` doit indiquer le chemin du dossier ou sont enregistres les `.json` tweets.

## Sample output

```
{
  "mongodb": {
    "create": {
      "10000": 1.3170632674999978,
      "20000": 2.4028837405000103,
      "50000": 6.275010825599997,
      "70000": 8.1673237211,
      "90000": 10.737976402799973
    },
    "retrieve": {
      "10000": 0.3924127672000054,
      "20000": 0.8381911315000365,
      "50000": 1.9734007373999929,
      "70000": 2.2166742306000744,
      "90000": 2.845205988800012
    },
    "update": {
      "10000": 0.2292069305999803,
      "20000": 0.46248832390000416,
      "50000": 1.029549795300022,
      "70000": 1.5355352308999728,
      "90000": 1.8713928380999505
    },
    "delete": {
      "10000": 0.05750133139998752,
      "20000": 0.08569198170000618,
      "50000": 0.24955861039999264,
      "70000": 0.27640671549993384,
      "90000": 0.3410740344999567
    }
  },
  "couchdb": {
    "create": {
      "10000": 4.750772356599964,
      "20000": 12.67306841479999,
      "50000": 34.717924828499875,
      "70000": 48.68356543790014,
      "90000": 75.54986584200014
    },
    "create_view": {
      "10000": 0.005271056199944724,
      "20000": 0.058147187799977476,
      "50000": 0.03402844499987623,
      "70000": 0.009186377000150969,
      "90000": 0.0074849033002465145
    },
    "query": {
      "10000": 6.478856433300029,
      "20000": 18.67054554720007,
      "50000": 48.31748290260002,
      "70000": 63.49018442459992,
      "90000": 79.32879154790007
    },
    "update": {
      "10000": 3.0128769274999287,
      "20000": 10.14986742908467,
      "50000": 20.1237516582999,
      "70000": 28.0551049425002,
      "90000": 34.78665568159977
    },
    "delete": {
      "10000": 5.628491597099969,
      "20000": 19.348930056100016,
      "50000": 37.8313908247002,
      "70000": 568.4546992089998,
      "90000": 75.23109177970018
    }
  }
}
