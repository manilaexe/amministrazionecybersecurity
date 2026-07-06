# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: $HOME/large-file-detector/app.py

import argparse
import os
import sys
import time

def walk(target, log_path, size):
    for filename in os.listdir(target):
        path=os.path.join(target, filename)
        if os.path.isdir(path):
            walk(target, path, size)
        elif os.path.isfile(path):
            dim=os.path.getsize(path)
            if dim>=size:
                print(f"trovato un grande file: {path} ({dim} bytes)")
                with open (log_path, "a") as f:
                    f.write(f"{path}\n")    

def main():
    parser=argparse.ArgumentParser(description="large file detector")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="percorso assoluto del direttorio da controllare"
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="dimensione minima in byte dei file da segnalare"
    )
    parser.add_argument(
        "--interval",
        type=str,
        required=True,
        help="intervallo in secondi tra ogni contorllo"
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="dove salvare il file di log"
    )
    args=parser.parse_args()
    
    target=args.target
    size=args.size 
    interval=args.interval
    log=args.log

    #---VALIDAZIONE DELL'INPUT---

    #taget deve essere un percorso assoluto
    if not os.path.isabs(target):
        print(f"{target} deve essere un percorso assoluto", file=sys.stderr)
        sys.exit(1)
    #target deve esistere
    if not os.path.exists(target):
        print(f"{target} deve esistere", file=sys.stderr)
        sys.exit(1)
    #target deve essere un direttorio
    if not os.path.isdir(target):
        print(f"{target} deve essere un direttorio", file=sys.stderr)
        sys.exit(1)
    #size deve essere un intero positivo
    if size<=0:
        print(f"size deve essere un intero positivo", file=sys.stderr)
        sys.exit(1)
    #interval deve essere un intero positivo
    if interval<=0:
        print(f"interval deve essere un intero positivo", file=sys.stderr)
        sys.exit(1)
    #log deve esistere
    if not os.path.exists(log):
        print(f"{log} deve esistere", file=sys.stderr)
        sys.exit(1)
    #log deve essere un direttorio
    if not os.path.isdir(log):
        print(f"{log} deve essere un direttorio", file=sys.stderr)
        sys.exit(1)
        
    logfile=os.path.join(log, "large-file-detector.log")
    while True:
        walk(target, logfile, size)
        time.sleep(interval)

if __name__ == "__main__":
    main()
