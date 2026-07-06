# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: $HOME/log-extractor/app.py

import argparse
import os
import sys

def find(filename, pattern): #filename: nome del file di log da analizzare
    risultato=[] #creo una lista vuota
    with open(filename, "r") as f: #apro il file in modalita` lettura
        lines = f.readlines() #legge tutte le righe del file e le salva in una lista.
    for line in lines: #scorre una riga alla volta della lista lines
        if pattern in line: #controlla se la stringa contenuta in pattern è presente nella riga corrente.
            risultato.append(line) #se la riga contiene il pattern, la aggiunge alla lista risultato
    return risultato 

def wrt(filename, lines): #funzione che scrive in un file
                          #filename: il file da creare
                          #line: lista di righe da scrivere
    with open(filename, "w") as f:  #apre (o crea) il file in modalità scrittura ("w")
        f.writelines(lines) #scrive nel file tutte le righe presenti nella lista.

def walk(target, backup, pattern):
    for filename in os.listdir(target):
        path=os.path.join(target, filename)
        if os.path.isdir(path):
            walk(path, backup, pattern)
        elif os.path.isfile(path):
            if filename.endswith(".log"):
                lines = find(path, pattern)
                if lines:
                    print(f"trovato {len(lines)} righe in {path}")
                    backup_file=os.path.join(backup, filename)
                    wrt(backup_file, lines)
                    print(f"scritte {len(lines)} righe in {backup_file}")


def main():
    #parser
    parser=argparse.ArgumentParser(description="log-extractor")
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="percorso assoluto della directory da analizzare"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        required=True,
        help="specifica il pattern da cercare all'interno dei file di log"
    )
    args=parser.parse_args()
    path=args.path 
    pattern=args.pattern 

    #---validazione dell'input---

    #path deve essere un percorso assoluto
    if not os.path.isdir(path):
        print(f"{path} deve essere un percorso assoluto", file=sys.stderr)
        sys.exit(1)
    #path deve esistere
    if not os.path.exists(path):
        print(f"{path} deve esistere", file=sys.stderr)
        sys.exit(1)
    #path deve essere una directory 
    if not os.path.isdir(path):
        print(f"{path} deve essere un direttorio", file=sys.stderr)
        sys.exit(1)
    #pattern deve essere una stringa non vota
    if pattern == "":
        print(f"pattern deve essere una stringa non vuota", file=sys.stderr)
        sys.exit(1)

    backup_path=os.path.expanduser("~/backup")
    os.makedirs(backup_path, exist_ok=True)
    walk(path, backup_path, pattern)

if __name__ == "__main__":
    main()