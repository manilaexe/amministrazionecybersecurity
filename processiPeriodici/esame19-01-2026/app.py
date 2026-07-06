# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: $HOME/file-compressor/app.py

import argparse
import os
import sys
import zipfile
import time

def walk(target, size, archivio):
    for filename in os.listdir(target):
        path=os.path.join(target,filename)
        if os.path.isdir(path):
            walk(path, size, archivio)
        elif os.path.isfile(path):
            csize=os.path.getsize(path)
            if csize>=size:
                with zipfile.ZipFile(archivio, "a") as zf:
                    zf.write(path, arcname=filename)
                os.remove(path)
                print(f"compresso {path} ({csize} bytes) in {archivio}")

def main():

    #parser
    parser=argparse.ArgumentParser("file compressor")
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="path e` il percorso assoluto della directory da scansionare"
    )

    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="size e` la soglia di dimensione oltre la quale i file devono essere compressi"
    )
    args=parser.parse_args()

    path=args.path
    size=args.size

    #validazione degli input
    
    #path deve essere un perorso assoluto
    if not os.path.isabs(path):
        print(f"{path} deve essere un percorso assoluto ", file=sys.stderr)
        sys.exit(1)
    #path deve esistere
    if not os.path.exists(path):
        print(f"{path} deve esistere ", file=sys.stderr)
        sys.exit(1)
    #path deve essere una direcotry
    if not os.path.isdir(path):
        print(f"{path} deve essere una directory ", file=sys.stderr)
        sys.exit(1)
    #size deve essere un intero positivo
    if size<=0:
        print(f"size deve essere un intero positivo ", file=sys.stderr)
        sys.exit(1)
    
    archivio=os.path.expanduser("~/archives") #crea la cartella degli archivi
    os.makedirs(archivio, exist_ok=True) #Crea la cartella archives se non esiste già
    pathArchivio=os.path.join(archivio, f"{int(time.time())}.zip") #il percorso COMPLETO del file zip che verrà creato
                                                                   #time.time(): restituisce il tempo attuale in secondi
                                                                   #int: taglia i decimali
                                                                   #f"{}.zip": crea il nome del file
                                                                   #os.path.join(...): Unisce cartella + file:
    walk(path, size, pathArchivio) #chiamata alla funzione ricorsiva    


if __name__ == "__main__":
    main()
