# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path: ~/disk-usage-monitor/app.py

import argparse
from datetime import datetime
import os
import shutil
import sys

def main():
    parser = argparse.ArgumentParser(description="disk usage monitor") #creo un ogetto che analizza gli argomenti della riga di comando
    #aggiunta dei parametri (partizione e soglia)
    parser.add_argument(
        "--partition",
        type=str,
        required=True,
        help="path assoluto della partizione da monitorare"
	)
    parser.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="Soglia di uso espressa in percentuale"        
	)
    
    args=parser.parse_args() #legge gli argomenti realmente inseriti
    #do dei nomi umani
    partition=args.partition
    threshold=args.threshold
    #controlli per path: deve essere assoluto ed esistere
    if not os.path.isabs(partition):
        print(f"errore: {partition} non e' un path assoluto", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(partition):
        print(f"errore: il path non esiste", file=sys.stderr)
        sys.exit(1)
    
	#controlli per threshold 
    if threshold<0 or threshold>100:
        print(f"errore: la soglia deve essere compresa tra 0 e 100", file=sys.stderr)
        exit(1)
    
    #calcolo dello spazio disco
    total, used, _ = shutil.disk_usage(partition) 
                     #la funzione shutil.disk_usage restituisce 3 valori: spazio totale, usato e libero tutti espressi in byte
                     #come parametro ha il percorso
                     #i valori returnati vengono messi nelle variabili dichiarate prima dell '=' e se la variabile e` '_' vuol dire che non interessa
    percentuale=used/total * 100 #calcolo della percentuale
    print(f"percentuale del disco usata per {partition}: {percentuale:.2f}%")
    
    if percentuale>=threshold:
        log_dir=os.path.expanduser("~/disk-usage-monitor") #converte '~' nella home dell'utente
        os.makedirs(log_dir, exist_ok=True) #crea la directory se necessario
                                            #grazie a exists_ok se esiste gia` non fa nulla
        log_path=os.path.join(log_dir, "disk-usage-monitor.log") #devo ricostruire l'indirizzo della consegna (~/disk-usage-monitor/disk-usage-monitor.log)

        #apertura del file
        with open(log_path, "a") as log_file: #apre il file
            now=datetime.now() #stampa data e ora
            log_file.write(f"{now} {percentuale:.2f}%\n") #crea la stringa che chiede
        

if __name__ == "__main__":
    main()
