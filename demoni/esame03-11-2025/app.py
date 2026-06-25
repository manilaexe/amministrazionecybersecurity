#ESAME 03-11-2025
# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: $HOME/old-file-detector/app.py

import argparse
from datetime import datetime
import os
import sys
import time
 
#funzione che esplora una directory, elimina i file vecchi e li logga
def walk(basepath, threshold, log_file_path): #basebath = directory da analizzare
                                              #threshold = tempo limite (se sono piu' vecchi vanno eliminati)
                                              #log_file_path = file di log
    for filename in os.listdir(basepath): #prende tutti i nomi dentro la directory
        path=os.path.join(basepath, filename) #costruisce il path completo
        #se e' un file: 
        if os.path.isfile(path): #chide se e' un file normale
            last_modified = os.path.getmtime(path) #prende l' ultima data di modifica del file (numero di secondi dal 1970)
            if last_modified < threshold: #lo confronta col tempo limite
                print(f"{path} (last modified: {time.ctime(last_modified)})") #stampa il percorso e la data leggibile grazie a ctime
                with open(log_file_path, "a") as f: #apre un file di log in append
                    f.write(f"{path}\n") #scrive il percorso del file nel log
                os.remove(path) #elimina il file dal filesystem
        #se e' una directory:
        elif os.path.isdir(path): #chiede se e' una directory
            walk(path, threshold, log_file_path) #chiamata ricorsiva

def main():
    parser = argparse.ArgumentParser(description="old file detector") #crea parser per leggere target, days, interval ,log

    #gli argomenti da analizzare
    parser.add_argument(
        "--target", type=str, required=True, help="directory to scan for old files."
    )
    parser.add_argument(
        "--days", type=str, required=True, help="number to consider a file old."
    )
    parser.add_argument(
        "--interval", type=int, required=True, help="interval in seconds between checks."
    )
    parser.add_argument(
        "--log", type=str, required=True, help="directory to save the log file."
    )
    args=parser.parse_args() #legge effettivamente i valori da terminale

    #VALIDAZIONE DELL'INPUT
    #controlli sul target
    if not os.path.isabs(args.target):
        print("error --target must be an absolute path.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print("error: --target path doesn't exists.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print("error: --target path must be a directory", file=sys.stderr)
        sys.exit(1)

    #controlli sui numeri
    if args.days<=0:
        print("error: --days must be a positive integer", file=sys.stderr)
        sys.exit(1)
    if args.interval<=0:
        print("error: --interval must be a positive integer", file=sys.stderr)
        sys.exit(1)
    
    #validazione del log
    if not os.path.exists(args.log):
        print("error: --target path doesn't exists.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print("error: --target path must be a directory", file=sys.stderr)
        sys.exit(1)
 
    #creazione del file di log
    log_file_path=os.path.join(args.log, "old-file-detector.log")
    #loop infinito -> demone
    while True:
        threshold = time.time() - (args.days * 86400) #calcola la soglia
        walk(args.target, threshold, log_file_path) #scansione 
        time.sleep(args.interval) #aspetta n secondi prima di rifare tutto



if __name__ == "__main__":
    main()
