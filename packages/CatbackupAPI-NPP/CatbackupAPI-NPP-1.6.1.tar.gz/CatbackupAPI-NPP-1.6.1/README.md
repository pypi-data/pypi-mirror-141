# Catbackup API-NPP
- Per executar el programa s'a de tenir instal·lat python v3 o mes. I instal·lar el tesseract (ja hi ha el .exe a la carpeta) en la carpeta tesseract
- Requeriments a "requirements.txt".
- Configuració de la base de dades a `config/config.yaml`
- Logs de errors a `errorLogs/*txt`
- Executar amb opcio -h per veure mes opcions i funcionalitats.


## Estructura de la base de dades
En una Base de dades que es digui "catbackup" un taula anomenada "credencials":
```
"usuari" Usuari amb permisos d'administrador del CatBackup

"contrassenya" Contrassenya del usuari

"host" URL de la interfaç web + /Admin/Login.aspx Per exemple https://catbackup.net/Admin/Login.aspx

"clau" Clau de OPT de CatBackup
```
## Instal·lació

- Utilitzant pip:

  ```pip install CatbackupAPI-NPP```

- Clonar el repositori
```gh repo clone NilPujolPorta/CatbackupAPI-NPP```

## Ús
### Maneres d'execució del programa (ordenades per recomenades)
- A la linea de commandes `catbackupAPI [opcions]`
- ```python -m CatBackupAPI [opcions]```
- ```./CatbackupAPI_NPP-runner [opcions] ```
- Executar el fitxer `CatbackupAPI_NPP.py` o `CatbackupAPI_NPP.cpython-39.pyc` amb les opcions adients. Llavors les dades es guardaran a `dadesCatBackup.json`


### Opcions
```
usage: CatbackupAPI_NPP.cpython-39.pyc [-h] [-q] [-tr RUTA] [-g] [-v] [-w URL]

Una API per a recullir informacio de la web de CatBackup.

optional arguments:
  -h, --help                      show this help message and exit
  -q, --quiet                     Nomes mostra els errors i el missatge de acabada per pantalla.
  --json-file RUTA                La ruta(fitxer inclos) a on es guardara el fitxer de dades json. Per defecte es: dadesCatBackup.json
  -tr RUTA, --tesseractpath RUTA  La ruta fins al fitxer tesseract.exe
  -g, --graphicUI                 Mostra el navegador graficament.
  -v, --versio                    Mostra la versio
  -w URL, --web URL               Especificar la web de Catbackup a on accedir. Per defecte es l'aconsegueix de la basa de dades
```


### Proximament:
2. Afegir support per altres bases de dades a part de mysql
