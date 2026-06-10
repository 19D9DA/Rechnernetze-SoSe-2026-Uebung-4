import socket
import threading
import random

# =========================================================
# CLIENT HANDLER
# =========================================================

class ClientHandler:

    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.dice_invitation = None  # pendende Einladung


# =========================================================
# CLIENT MAP & DICE GAMES
# =========================================================

clients = {}
dice_games = {}  # {client1_name: {client2_name, invite_pending}}
games_lock = threading.Lock()


# =========================================================
# BROADCAST MESSAGE
# =========================================================

def broadcast_message(message, exclude_name=None):
    """Sendet eine Nachricht an alle Clients außer exclude_name"""
    for name, handler in clients.items():
        if exclude_name is None or name != exclude_name:
            try:
                handler.conn.sendall((message + "\n").encode())
            except:
                pass


# =========================================================
# CLIENT THREAD
# =========================================================

def handle_client(conn):

    name = None

    try:

        # =====================================================
        # REGISTRIERUNG
        # =====================================================

        while True:

            conn.sendall(b"register <name>\n")

            reg = conn.recv(1024).decode().strip()

            if not reg:
                conn.close()
                return

            parts = reg.split(" ")

            # ===== FORMAT PRUEFEN =====

            if len(parts) != 2 or parts[0].lower() != "register":

                conn.sendall(
                    b"Erwartet: register <name>\n"
                )

                continue

            name = parts[1]

            # ===== NAME SCHON VERGEBEN =====

            if name in clients:

                conn.sendall(
                    b"Name bereits vergeben!\n"
                )

                continue

            break

        # =====================================================
        # CLIENT REGISTRIEREN
        # =====================================================

        clients[name] = ClientHandler(name, conn)

        print(f"{name} connected")
        broadcast_message(f"[System] {name} ist verbunden", exclude_name=name)

        # =====================================================
        # MESSAGE LOOP
        # =====================================================

        while True:

            data = conn.recv(1024)

            if not data:
                break

            msg = data.decode().strip()

            print(f"{name}: {msg}")

            # =================================================
            # SEND <target> <message>
            # =================================================

            if msg.startswith("send "):

                parts = msg.split(" ", 2)

                if len(parts) == 3:

                    target = parts[1]
                    text = parts[2]

                    if target in clients:

                        clients[target].conn.sendall(
                            f"{name}: {text}\n".encode()
                        )

                continue

            # =================================================
            # CLIENTLIST
            # =================================================

            elif msg == "clientlist":

                client_list = "\n".join(
                    ["Verbundene Clients:"] +
                    [f"  - {c_name}" for c_name in clients.keys()]
                )
                conn.sendall((client_list + "\n").encode())

                continue

            # =================================================
            # SENDALL <message>
            # =================================================

            elif msg.startswith("sendall "):

                text = msg[8:].strip()

                for client_name, handler in clients.items():
                    if client_name != name:
                        handler.conn.sendall(
                            f"{name}: {text}\n".encode()
                        )

                conn.sendall(f"✓ Nachricht an alle gesendet\n".encode())

                continue

            # =================================================
            # DICE COMMANDS
            # =================================================

            elif msg.startswith("dice "):

                dice_cmd = msg[5:].strip()

                # ===== DICE INVITE <client> =====

                if dice_cmd.startswith("invite "):

                    target = dice_cmd[7:].strip()

                    if target not in clients:
                        conn.sendall(b"Client nicht gefunden\n")
                        continue

                    if target == name:
                        conn.sendall(b"Kannst dich nicht selbst einladen\n")
                        continue

                    # Einladung speichern
                    clients[target].dice_invitation = name

                    clients[target].conn.sendall(
                        f"[Dice] {name} möchte ein Würfelspiel spielen\n".encode()
                    )
                    clients[target].conn.sendall(
                        b"Antworte mit: dice join oder dice decline\n".encode()
                    )

                    conn.sendall(
                        f"✓ Einladung an {target} gesendet\n".encode()
                    )

                # ===== DICE JOIN =====

                elif dice_cmd == "join":

                    if clients[name].dice_invitation is None:
                        conn.sendall(b"Keine Einladung vorhanden\n")
                        continue

                    inviter = clients[name].dice_invitation
                    clients[name].dice_invitation = None

                    # Spieler mitteilen, dass Einladung angenommen wurde
                    if inviter in clients:
                        clients[inviter].conn.sendall(
                            f"✓ {name} hat die Einladung angenommen!\n".encode()
                        )

                    # WÜRFELSPIEL STARTEN
                    dice_rolls = [
                        random.randint(1, 6),
                        random.randint(1, 6)
                    ]
                    inviter_rolls = [
                        random.randint(1, 6),
                        random.randint(1, 6)
                    ]

                    inviter_sum = sum(inviter_rolls)
                    joiner_sum = sum(dice_rolls)

                    # Ergebnis bestimmen
                    if inviter_sum > joiner_sum:
                        inviter_result = "Gewonnen"
                        joiner_result = "Verloren"
                    elif joiner_sum > inviter_sum:
                        inviter_result = "Verloren"
                        joiner_result = "Gewonnen"
                    else:
                        inviter_result = "Unentschieden"
                        joiner_result = "Unentschieden"

                    # Ergebnisse senden
                    if inviter in clients:
                        clients[inviter].conn.sendall(
                            f"\n[Würfelspiel Ergebnis]\n".encode()
                        )
                        clients[inviter].conn.sendall(
                            f"Deine Würfel: {inviter_rolls[0]}, {inviter_rolls[1]} = {inviter_sum}\n".encode()
                        )
                        clients[inviter].conn.sendall(
                            f"{name} Würfel: {dice_rolls[0]}, {dice_rolls[1]} = {joiner_sum}\n".encode()
                        )
                        clients[inviter].conn.sendall(
                            f"Ergebnis: {inviter_result}\n\n".encode()
                        )

                    conn.sendall(
                        f"\n[Würfelspiel Ergebnis]\n".encode()
                    )
                    conn.sendall(
                        f"Deine Würfel: {dice_rolls[0]}, {dice_rolls[1]} = {joiner_sum}\n".encode()
                    )
                    conn.sendall(
                        f"{inviter} Würfel: {inviter_rolls[0]}, {inviter_rolls[1]} = {inviter_sum}\n".encode()
                    )
                    conn.sendall(
                        f"Ergebnis: {joiner_result}\n\n".encode()
                    )

                # ===== DICE DECLINE =====

                elif dice_cmd == "decline":

                    if clients[name].dice_invitation is None:
                        conn.sendall(b"Keine Einladung vorhanden\n")
                        continue

                    inviter = clients[name].dice_invitation
                    clients[name].dice_invitation = None

                    # Einladenden Spieler benachrichtigen
                    if inviter in clients:
                        clients[inviter].conn.sendall(
                            f"✗ {name} hat die Einladung abgelehnt\n".encode()
                        )

                    conn.sendall(b"✓ Einladung abgelehnt\n")

                else:
                    conn.sendall(
                        b"Unbekannter dice Befehl. Nutze: dice invite <client>, dice join, dice decline\n"
                    )

                continue

    except Exception as e:

        print(f"{name} error: {e}")

    finally:

        # =====================================================
        # DISCONNECT
        # =====================================================

        if name is not None:

            clients.pop(name, None)

            print(f"Removed: {name}")
            broadcast_message(f"[System] {name} ist verbunden")

        conn.close()


# =========================================================
# TCP SERVER
# =========================================================

def tcp_server(port=5000):

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind(("0.0.0.0", port))

    server.listen()

    print(f"TCP Server läuft auf Port {port}")

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn,)
        ).start()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    tcp_server()