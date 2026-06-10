# Rechnernetze 2026-SS - Übungsblatt 04

`#19D9DA - s4joregn`

## Aufgabe 1: Protokoll-Header

In der Vorlesung wurden die Kategorien der IPv4-Header vorgestellt. Finden Sie in Wireshark ein beliebiges IPv4-Paket. Ordnen Sie Elemente des gefundenen Paketes den Kategorien des Headers zu (Version, Header Length, Type of Service, etc.). Finden Sie anschließend jeweils ein UDP- und TCP-Paket und ordnen Sie auch dort die Elemente des Pakets den Kategorien zu. Beachten Sie, dass die Header dieser beiden Protokolle anders aufgebaut sind als der IPv4-Header.

### Internet Protocol Version 4

```ts
Version: 4 // Internet Protocol Version 4 (IPv4)
Header Length: 20 bytes // Mindestgröße eines IPv4-Headers ohne zusätzliche Optionen
DSCP: CS0 // riorität des Pakets - CS0 ist Standard-Priorität
ECN: Not-ECT // Geräte unterstützen keine automatische Benachrichtigung bei Netzwerk-Stau unterstützen
Total Length: 48 // Paket ist 48 Bytes groß (20 Bytes Header + 28 Bytes Daten)
Identification: 0x1a21 (6689) // Nummer um zusammengehörende Paket-Teile wiederzuerkennen
Flags: 0x0 // mögliche Aufteilung des Pakets
Fragment Offset: 0 // Paket wurde nicht zerteilt
TTL: 128 // Paket darf noch durch 128 Router reisen, bevor es gelöscht wird
Protocol: UDP (17) // UDP-Protokoll
Header Checksum: 0x229a // Prüfsumme, um Fehler im Header zu entdecken
Src: 127.0.0.1 // Quelladresse
Dst: 127.0.0.1 // Zieladresse
```

### UDP

```ts
Source Port: 54550 // Quellport / zufälliger Absendeport des Clients
Destination Port: 8008 // Zielport
length: 48 // Paket ist 48 Bytes groß (20 Bytes Header + 28 Bytes)
checksum: 0x2779 [unverified] // Prüfsumme
UDP payload (20 bytes) // Paketinhalt
```

### TCP

```ts
Source Port: 43659 // Quellport des Absenders
Destination Port: 3032 // Zielport des Empfängers
Sequence Number: 1 (relative sequence number) // Relative Sequenznummer
Sequence Number (raw): 160457935 // Echte Sequenznummer im TCP-Header
Acknowledgment Number: 1    (relative ack number) // Relative Bestätigungsnummer
Acknowledgment number (raw): 682474781 // Echte Bestätigungsnummer im TCP-Header
Header Length: 20 bytes (5) // Länge des TCP-Headers ohne Optionen
flags: 0x010 (ACK)  // TCP-Flag
    Reserved: Not set // Reservierte Bits sind ungenutzt
    Accurate ECN: Not set  // Überlastungsanzeige ist deaktiviert
    Congestion Window Reduced: Not set // Keine Reduzierung des Sendefensters
    ECN-Echo: Not set // Kein ECN-Echo-Signal vorhanden
    Urgent: Not set // Keine dringenden Daten enthalten
    Acknowledgment: Set  // ACK-Bit ist gesetzt / Paket bestätigt Daten
    Push: Not set // Daten werden normal gepuffert
    Reset: Not set // Verbindung wird nicht abgebrochen
    Syn: Not set // Kein Verbindungsaufbau
    Fin: Not set // Kein Verbindungsabbau
    window: 246 // Größe des Empfangsfensters beim Absender
checksum: 0xf238 [unverified] // Prüfsumme vom Tool nicht überprüft
Urgent Pointer: 0 // Zeiger für dringende Daten ist null
TCP payload (1 byte) // Inhalt umfasst genau ein Byte Nutzdaten
TCP keep-alive garbage octet // Dummy-Byte zur Aufrechterhaltung der Verbindung

```

## Aufgabe 2: CIDR

### a) 
Beschreiben Sie 103.161.122.83/18. Was ist bedeuten jeweils die 103.161.122.83 und die 18? Erklären Sie kurz, wie man daraus Subnetzmaske, Broadcastadresse und Netzwerkadresse ermitteln kann.
```ts
"103.161.122.83" ist "IP-Adresse"
"/18" ist "Subnetzpräfix" -> 18 Bits sind fest restliche 14 sind frei


Subnetzmaske: 255.255.192.0
1111111.1111111.11000000.00000000

Broadcastadresse: 103.161.127.255 
(letzte Adresse im Netz)

Netzwerkadresse: 103.161.64.0
(erste Adresse im Netz)
```

### b) 
Geben Sie für die folgenden IP-Adressen jeweils Subnetzmaske, Broadcastadresse und Netzwerkadresse an:

#### (i) 
```ts
172.16.45.200/20
Subnetzmaske: 255.255.240.0
Netzwerkadresse: 172.16.32.0
Broadcastadresse: 172.16.47.255
```

#### (ii) 
```ts
192.168.14.77/26
Subnetzmaske: 255.255.255.192
Netzwerkadresse: 192.168.14.64
Broadcastadresse: 192.168.14.127
```

#### (iii) 
```ts
10.55.201.19/13
Subnetzmaske: 255.248.0.0
Netzwerkadresse: 10.48.0.0
Broadcastadresse: 10.55.255.255 
```

### c) 
Liegt die 103.161.122.83/18 im selben Netz wie 103.161.193.83/18? Begründen Sie Ihre Einschätzung.
```ts
103.161.122.83/18
Netzwerkadresse: 103.161.64.0

103.161.193.83/18
Netzwerkadresse: 103.161.192.0
```
Die beiden Adresse liegen in unterschiedlichen Netzen.

## Aufgabe 3: Programmierung

## Aufgabe 4: Kommunikation zwischen Implementationen

