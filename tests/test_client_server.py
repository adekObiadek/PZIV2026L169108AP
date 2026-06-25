import socket
import threading
import time

import pytest

import server
from client import run_client
from models import Plant


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
        test_socket.bind(("localhost", 0))
        return test_socket.getsockname()[1]


@pytest.fixture
def running_server():
    port = get_free_port()
    stop_event = threading.Event()
    original_sleep_range = server.SLEEP_RANGE
    server.SLEEP_RANGE = (0.01, 0.02)

    server_thread = threading.Thread(
        target=server.run_server,
        kwargs={
            "host": "localhost",
            "port": port,
            "max_clients": server.MAX_CLIENTS,
            "stop_event": stop_event,
        },
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.1)

    yield port

    stop_event.set()
    server_thread.join(timeout=1)
    server.SLEEP_RANGE = original_sleep_range


def test_client_receives_objects_from_server(running_server):
    result = run_client("test-client", port=running_server, query_classes=["Plant"])

    assert result["status"] == "OK"
    assert len(result["responses"]["Plant"]) == 4
    assert all(isinstance(item, Plant) for item in result["responses"]["Plant"])


def test_server_refuses_client_after_max_clients(running_server):
    sockets = []
    try:
        for client_id in range(server.MAX_CLIENTS):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("localhost", running_server))
            client_socket.sendall(str(client_id).encode("utf-8"))
            assert client_socket.recv(1024).decode("utf-8") == "OK"
            sockets.append(client_socket)

        refused_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        refused_socket.connect(("localhost", running_server))
        refused_socket.sendall(b"4")

        assert refused_socket.recv(1024).decode("utf-8") == "REFUSED"
        refused_socket.close()
    finally:
        for client_socket in sockets:
            client_socket.close()


def test_server_sends_wrong_type_for_unknown_class(running_server):
    result = run_client("bad-type", port=running_server, query_classes=["Animal"])

    assert result["status"] == "OK"
    assert isinstance(result["responses"]["Animal"], dict)
