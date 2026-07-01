# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: $HOME/dir-size-monitor/app.py

import argparse
from datetime import datetime
import os
import sys
import time

#funzione che somma le dimensioni
def dimTotale(cartella):
    somma=0
    for filename in os.listdir(cartella): #prende tutto quello che c'e` dentro alla direcotry
        path=os.path.join(cartella, filename) #crea il percoso 
        if os.path.isfile(path): #se e` un file fa la somma
            somma += os.path.getsize(path) 
        elif os.path.isdir(path): #se non e` un file fa la chiamata ricorsiva
            somma += dimTotale(path)
    return somma


def main():
    #argomenti da analizzare da riga di comando: target, threshold, interval, log

    #creazione del parser
    parser = argparse.ArgumentParser(description="dir size monitor")

    #argomenti da analizzare 
    parser.add_argument(
        "--target", type=str, required=True, help="percorso assoluto della directory da monitorare"
    )
    parser.add_argument(
        "--threshold", type=int, required=True, help="soglia per l'avviso"
    )
    parser.add_argument(
        "--interval", type=int, required=True, help="intervallo in secondi tra ogni controllo"
    )
    parser.add_argument(
        "--log", type=str, required=True, help="percorso assoluto della directory dove salvare il file di log"
    )
    #lettura effettiva
    args=parser.parse_args()
    target=args.target
    threshold=args.threshold
    interval=args.interval
    log=args.log

    #VALIDAZIONE DELL'INPUT
    #controlli sul target (cartella+assoluto)
    if not os.path.isabs(target):
        print(f"errore: {target} deve essere un percorso assoluto", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(target):
        print(f"il percorso {target} non esiste", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(target):
        print(f"{target} deve essere una cartella", file=sys.stderr)
        sys.exit(1)
    
    #controlli sulla soglia
    if threshold<=0:
        print(f"La soglia deve essere un valore positivo intero", file=sys.stderr)
        sys.exit(1)
    
    #controlli sui secondi
    if interval<=0:
        print(f"L'intervallo deve essere un valore positivo intero", file=sys.stderr)
        sys.exit(1)      
    
    #controlli su log (cartella+assoluto)
    if not os.path.isabs(log):
        print(f"errore: {log} deve essere un percorso assoluto", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(log):
        print(f"il percorso {log} non esiste", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(log):
        print(f"{log} deve essere una cartella", file=sys.stderr)
        sys.exit(1)

    log_dir=os.path.join(log, "dir-size-monitor.log")

    while True:
        somma=dimTotale(target)
        if somma>threshold:
            with open(log_dir, "a") as log_file:
                log_file.write(f"{datetime.now()} {somma}\n")
            print(f"la dimensione totale: {somma} sfora la soglia di {threshold}")
        time.sleep(interval) #aspetta n secondi prima di ricontrollare

if __name__ == "__main__":
    main()
