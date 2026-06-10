import socket
import threading
import sys

# =========================================================
# REGISTERED RECIPIENTS
# =========================================================

recipients = {}  # {name: (ip, port)}


# =========================================================
# RECEIVE THREAD
# =========================================================

def receiver(sock):

    while True:

        try:

            data, addr = sock.recvfrom(4096)

            msg = data.decode("utf-8")

            print(f"\nEmpfangen von {addr[0]}:{addr[1]}")
            print(msg)

            print("> ", end="", flush=True)

        except:
            break


# =========================================================
# MAIN
# =========================================================

def main():

    if len(sys.argv) != 3:
        print("Usage: python udp_client.py <name> <port>")
        return

    own_name = sys.argv[1]
    own_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("0.0.0.0", own_port))

    print("UDP gestartet:")
    print("Name:", own_name)
    print("Port:", own_port)

    threading.Thread(
        target=receiver,
        args=(sock,),
        daemon=True
    ).start()

    while True:

        print("> ", end="")

        input_line = input().strip()

        # =====================================================
        # REGISTER <Name> <IP> <Port>
        # =====================================================

        if input_line.startswith("register "):

            parts = input_line.split(" ", 3)

            if len(parts) != 4:
                print("Usage: register <name> <ip> <port>")
                continue

            name = parts[1]
            ip = parts[2]
            port = int(parts[3])

            recipients[name] = (ip, port)
            print(f"✓ {name} ({ip}:{port}) registriert")

        # =====================================================
        # CLIENTLIST
        # =====================================================

        elif input_line == "clientlist":

            if not recipients:
                print("Keine Clients registriert")
            else:
                print("Registrierte Clients:")
                for name, (ip, port) in recipients.items():
                    print(f"  - {name}: {ip}:{port}")

        # =====================================================
        # SEND <IP> <Port> <Message>
        # =====================================================

        elif input_line.startswith("send "):

            parts = input_line.split(" ", 3)

            if len(parts) != 4:
                print("Usage: send <ip> <port> <message>")
                continue

            ip = parts[1]
            port = int(parts[2])
            message = parts[3]

            final_msg = (
                f"{own_name}: {message}"
            ).encode("utf-8")

            sock.sendto(final_msg, (ip, port))
            print(f"✓ Nachricht an {ip}:{port} gesendet")

        # =====================================================
        # SENDALL <Message>
        # =====================================================

        elif input_line.startswith("sendall "):

            message = input_line[8:].strip()

            if not recipients:
                print("Keine Clients registriert")
                continue

            for name, (ip, port) in recipients.items():
                final_msg = (
                    f"{own_name}: {message}"
                ).encode("utf-8")
                sock.sendto(final_msg, (ip, port))
                print(f"✓ Nachricht an {name} gesendet")

        # =====================================================
        # EXIT
        # =====================================================

        elif input_line == "exit":

            sock.close()
            break

        # =====================================================
        # HELP
        # =====================================================

        else:

            print("Befehle:")
            print("  register <name> <ip> <port>  - Empfänger registrieren")
            print("  clientlist                    - Alle Clients anzeigen")
            print("  send <ip> <port> <message>   - An einen Client senden")
            print("  sendall <message>             - An alle Clients senden")
            print("  exit                          - Beenden")


if __name__ == "__main__":
    main()