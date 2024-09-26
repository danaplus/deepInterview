import subprocess
import time
import pytest

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 65432


@pytest.fixture(scope="module", autouse=True)
def start_server():
    # Start the server as a subprocess
    server_process = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Allow time for the server to start
    time.sleep(1)

    # Yield to the test case and terminate the server after tests
    yield
    server_process.terminate()


def run_client(num1, num2, operator):
    """Helper function to run the client process and capture its output."""
    client_process = subprocess.run(
        ['python', 'client.py', str(num1), str(num2), operator],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Return the result (formatted output like 'Result: 8')
    return client_process.stdout.decode('utf-8').strip()


def test_addition_operation():
    result = run_client(5, 3, '+')
    assert "Result: 8" in result


def test_subtraction_operation():
    result = run_client(10, 4, '-')
    assert "Result: 6" in result


def test_multiplication_operation():
    result = run_client(6, 7, '*')
    assert "Result: 42" in result


def test_division_operation():
    result = run_client(20, 5, '/')
    assert "Result: 4.0" in result


def test_division_by_zero():
    result = run_client(5, 0, '/')
    assert "Error: Division by zero" in result


def test_invalid_operation():
    result = run_client(5, 3, '^')
    assert "Invalid operation" in result
