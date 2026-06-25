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
    parser = argparse.ArgumentParser(description="old file detector")
    parser.add_argument(
        "--target", type=str, required=True, help="directory to scan for old files."
    )
    parser.add_argument(
        "--days", type=int, required=True, help="number of days to consider a file old."
    )
    parser.add_argument(
        "--interval",
        type=int,
        required=True,
        help="interval in seconds between checks.",
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="directory to save the log file.",
    )
    args = parser.parse_args()

    if not os.path.isabs(args.target):
        print("error: --target must be an absolute path.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print("error: --target path does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print("error: --target path is not a directory.", file=sys.stderr)
        sys.exit(1)

    if args.days <= 0:
        print("error: --days must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    if args.interval <= 0:
        print("error: --interval must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.log):
        print("error: --log path does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print("error: --log path is not a directory.", file=sys.stderr)
        sys.exit(1)

    log_file_path = os.path.join(args.log, "old-file-detector.log")
    while True:
        threshold = time.time() - (args.days * 86400)
        walk(args.target, threshold, log_file_path)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
