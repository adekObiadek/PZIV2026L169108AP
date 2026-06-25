import pickle
import random
import socket
import struct
import threading
import time

from storage import create_initial_data, get_objects_by_class


HOST = "localhost"
PORT = 5000
MAX_CLIENTS = 3
BUFFER_SIZE = 1024
SLEEP_RANGE = (0.5, 2.0)

_active_clients = 0
_active_clients_lock = threading.Lock()


def send_pickle(client_socket, data):
    serialized_data = pickle.dumps(data)
    message_size = struct.pack("!I", len(serialized_data))
    client_socket.sendall(message_size + serialized_data)


def _delayed_response():
    time.sleep(random.uniform(*SLEEP_RANGE))


def handle_client(client_socket, client_address, data):
    global _active_clients

    client_id = "unknown"
    try:
        client_id = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        print(f"Obsluga klienta {client_id} z adresu {client_address}")
        client_socket.sendall(b"OK")

        while True:
            class_name = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
            if not class_name:
                break

            _delayed_response()

            if class_name in {"Plant", "Sensor", "WateringSchedule"}:
                objects = get_objects_by_class(data, class_name)
                print(f"Klient {client_id}: wysylam {class_name}: {objects}")
                send_pickle(client_socket, objects)
            else:
                wrong_type_object = {
                    "error": "Niepoprawna klasa",
                    "requested_class": class_name,
                }
                print(
                    f"Klient {client_id}: wysylam bledny typ dla {class_name}: "
                    f"{wrong_type_object}"
                )
                send_pickle(client_socket, wrong_type_object)
    except (ConnectionError, OSError) as error:
        print(f"Blad polaczenia z klientem {client_id}: {error}")
    finally:
        client_socket.close()
        with _active_clients_lock:
            _active_clients -= 1
        print(f"Zakonczono obsluge klienta {client_id}")


def run_server(host=HOST, port=PORT, max_clients=MAX_CLIENTS, stop_event=None):
    global _active_clients

    data = create_initial_data()
    _active_clients = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        server_socket.settimeout(0.2)
        print(f"Serwer dziala na {host}:{port}")

        while stop_event is None or not stop_event.is_set():
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue

            with _active_clients_lock:
                if _active_clients >= max_clients:
                    client_socket.sendall(b"REFUSED")
                    client_socket.close()
                    print(f"Odmowa polaczenia dla {client_address}")
                    continue
                _active_clients += 1

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, data),
                daemon=True,
            )
            client_thread.start()


if __name__ == "__main__":
    run_server()
