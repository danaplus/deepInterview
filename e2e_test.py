import subprocess
import socket
import time
import pytest

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 65432


@pytest.fixture(scope="module", autouse=True)
def start_server():
    # Start the server as a subprocess and allow it some time to initialize
    server_process = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Allow some time for the server to start
    time.sleep(1)

    # Yield to the test case and then clean up
    yield
    server_process.terminate()


def send_request_to_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(data.encode('utf-8'))
        result = s.recv(1024).decode('utf-8')
        return result


def test_addition_operation():
    data = "5,3,+"
    expected_result = "8"
    result = send_request_to_server(data)
    assert result == expected_result


def test_subtraction_operation():
    data = "10,4,-"
    expected_result = "6"
    result = send_request_to_server(data)
    assert result == expected_result


def test_multiplication_operation():
    data = "6,7,*"
    expected_result = "42"
    result = send_request_to_server(data)
    assert result == expected_result


def test_division_operation():
    data = "20,5,/"
    expected_result = "4.0"
    result = send_request_to_server(data)
    assert result == expected_result


def test_division_by_zero():
    data = "5,0,/"
    expected_result = "Error: Division by zero"
    result = send_request_to_server(data)
    assert result == expected_result


def test_invalid_operation():
    data = "5,3,^"
    expected_result = "Invalid operation"
    result = send_request_to_server(data)
    assert result == expected_result
