# BUT_FIT_IPK_1

autor: Lukáš Plevač (xpleva07)

date: 30.3.2021


Implementovat klienta pro read-only (GET) distribuovaný souborový systém. Tento systém používá URL pro identifikaci souborů a jejich umístění. Systém používá File Service Protocol (FSP). Systém podporuje symbolická jména, které jsou překládány na IP adresy a porty pomocí protokolu Name Service Protocol (NSP).

## Soubory
* src/fileget.py - hlavní soubor spujuje a využívá soubory níže
* src/fsp.py - obsahuje implementaci protokolu FSP
* src/nsp.py - obsahuje implementaci protokolu NSP

## Dodatečné soubory
* test/* - obsahuje základní testy
* spec.pdf - obsahuje zadání
* Makefile
* obsahuje tragetety:
-> src.zip - vytvoří zip src složky a vytvoří kopii src/fileget.py kterou pojmenuje fileget a přidá toto readme
-> serv - spustí testovací server na 127.0.0.1:3333
-> self-test - provede self-test podle zadání výstup uloží do out.zip
-> clean - provede clean repozitáře od build files