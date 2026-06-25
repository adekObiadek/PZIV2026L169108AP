import pickle
import socket
import struct
import sys

from models import Plant, Sensor, WateringSchedule
from server import HOST, PORT


QUERY_CLASSES = ["Plant", "Sensor", "WateringSchedule", "Animal"]
CLASS_MAP = {
    "Plant": Plant,
    "Sensor": Sensor,
    "WateringSchedule": WateringSchedule,
}


def _receive_exact(client_socket, size):
    data = b""
    while len(data) < size:
        packet = client_socket.recv(size - len(data))
        if not packet:
            raise ConnectionError("Polaczenie zostalo przerwane")
        data += packet
    return data


def receive_pickle(client_socket):
    raw_size = _receive_exact(client_socket, 4)
    message_size = struct.unpack("!I", raw_size)[0]
    serialized_data = _receive_exact(client_socket, message_size)
    return pickle.loads(serialized_data)


def validate_response(data, class_name):
    expected_class = CLASS_MAP.get(class_name)
    if expected_class is None:
        raise TypeError(f"Nieznana klasa odpowiedzi: {class_name}")

    if not isinstance(data, list):
        raise TypeError("Odebrane dane nie sa lista obiektow")

    for item in data:
        if not isinstance(item, expected_class):
            raise TypeError(
                f"Niepoprawny typ obiektu: oczekiwano "
                f"{expected_class.__name__}, otrzymano {type(item).__name__}"
            )

    return data


def run_client(client_id, host=HOST, port=PORT, query_classes=None):
    queries = query_classes or QUERY_CLASSES

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(str(client_id).encode("utf-8"))

        status = client_socket.recv(1024).decode("utf-8")
        if status == "REFUSED":
            print(f"Klient {client_id}: polaczenie odrzucone przez serwer")
            return {"status": "REFUSED", "responses": {}}

        if status != "OK":
            raise ConnectionError(f"Nieoczekiwana odpowiedz serwera: {status}")

        responses = {}
        for class_name in queries:
            client_socket.sendall(class_name.encode("utf-8"))
            received_data = receive_pickle(client_socket)
            responses[class_name] = received_data

            try:
                objects = validate_response(received_data, class_name)
                print(f"Klient {client_id}: odebrano {class_name}")
                for item in objects:
                    print(f"Klient {client_id}: {item}")
            except TypeError as error:
                print(
                    f"Klient {client_id}: blad rzutowania/niepoprawny typ "
                    f"danych dla {class_name}: {error}"
                )

        return {"status": "OK", "responses": responses}


def main():
    if len(sys.argv) != 2:
        print("Uzycie: python client.py <id_klienta>")
        sys.exit(1)

    run_client(sys.argv[1])


if __name__ == "__main__":
    main()
