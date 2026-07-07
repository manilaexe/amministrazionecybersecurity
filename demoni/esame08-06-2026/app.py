# nome e cognome: Manila Mingozzi
# matricola: 196050
#
# path:$HOME/prefix-cleaner/app.py

import argparse
from datetime import datetime
import os
import sys
import time

def  walk(target, log, pref):
	for filename in os.listdir(target):
		path=os.path.join(target,filename)
		if os.path.isdir(path):
			walk(path, log, pref)
		if os.path.isfile(path):
			if filename.startswith(pref):
				with open (log, "a") as f:
					f.write(f"{datetime.now()} {path}\n")
				os.remove(path)

def main():
	#parser
	parser=argparse.ArgumentParser(description="prefix cleaner")
	parser.add_argument(
		"--target",
		type=str,
		required=True,
		help="indica il percorso assoluto del direttorio da ripulire"
	)
	parser.add_argument(
		"--prefix",
		type=str,
		required=True,
		help="il prefisso del nome dei file da rimuovere"
	)
	parser.add_argument(
		"--interval",
		type=int,
		required=True,
		help="intervallo in secondi tra ogni controllo"	
	)
	parser.add_argument(
		"--log",
		type=str,
		required=True,
		help="percorso assoluto o relativo del direttorio dove salvare il file di log"
	)
	args=parser.parse_args()

	#nome variabili
	target=args.target
	prefix=args.prefix
	interval=args.interval
	log=args.log

	#---VALIDADZIONE DELL'INPUT
	#target deve essere un percorso assoluto, deve esistere ed essere un direttorio
	if not os.path.isabs(target):
		print(f"{target} deve essere un percorso assoluto", file=sys.stderr)
		sys.exit(1)
	if not os.path.exists(target):
		print(f"{target} deve esistere", file=sys.stderr)
		sys.exit(1)
	if not os.path.isdir(target):
		print(f"{target} deve essere un direttorio", file=sys.stderr)
		sys.exit(1)
	#prefix non deve essere vuoto
	if not prefix:
		print(f"prefix non deve essere nullo", file=sys.stderr)
		sys.exit(1)
	#interval deve essere un intero positivo
	if interval<=0:
		print(f"interval deve essere un intero positivo", file=sys.stderr)
		sys.exit(1)
	#log deve esistere ed essere un direttorio
	if not os.path.exists(log):
		print(f"{log} deve esistere", file=sys.stderr)
		sys.exit(1)
	if not os.path.isdir(log):
		print(f"{log} deve essere un direttorio", file=sys.stderr)
		sys.exit(1)

	log_file=os.path.join(log, "prefix-cleaner.log")
	
	while True:
		walk(target, log_file, prefix)
		time.sleep(interval)
	
if __name__ == "__main__":
    main()
