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
    expected_result = 8.0  # Use float to ensure consistency
    result = send_request_to_server(data)

    # Convert the result to float for comparison
    assert float(result) == expected_result


def test_subtraction_operation():
    data = "10,4,-"
    expected_result = 6.0
    result = send_request_to_server(data)

    # Convert the result to float for comparison
    assert float(result) == expected_result


def test_multiplication_operation():
    data = "6,7,*"
    expected_result = 42.0
    result = send_request_to_server(data)

    # Convert the result to float for comparison
    assert float(result) == expected_result


def test_division_operation():
    data = "20,5,/"
    expected_result = 4.0
    result = send_request_to_server(data)

    # Convert the result to float for comparison
    assert float(result) == expected_result

def run_client(num1, num2, operator):
    """Helper function to run the client process and capture its output."""
    client_process = subprocess.run(
        ['python', 'client.py', str(num1), str(num2), operator],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Return the result (formatted output like 'Result: 42')
    return client_process.stdout.decode('utf-8').strip()

def test_multiplication_operation():
    result = run_client(6, 7, '*')
    assert "Result: 42" in result
