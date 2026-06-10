import socket
import threading
import sys

def receive(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
            print("> ", end="", flush=True)
    except:
        print("\nVerbindung verloren")

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <serverIp> <serverPort>")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    print("Verbunden")
    print("Befehle:")
    print("  send <name> <message>                - Nachricht an einen Client")
    print("  clientlist                           - Alle Clients anzeigen")
    print("  sendall <message>                    - An alle Clients senden")
    print("  dice invite <client>                 - Würfelspiel Einladung")
    print("  dice join                            - Würfelspiel Einladung annehmen")
    print("  dice decline                         - Würfelspiel Einladung ablehnen")
    print("  exit                                 - Beenden")
    print()

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        try:
            msg = input("> ")
            if msg.strip():
                sock.sendall((msg + "\n").encode())
        except KeyboardInterrupt:
            print("\nBis bald!")
            break
        except:
            break

if __name__ == "__main__":
    main()