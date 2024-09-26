import socket
import logging
from abc import ABC, abstractmethod

# Server-side logger setup
logging.basicConfig(filename="server.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Operation(ABC):
    @abstractmethod
    def execute(self, num1, num2):
        pass

class Addition(Operation):
    def execute(self, num1, num2):
        return num1 + num2

class Subtraction(Operation):
    def execute(self, num1, num2):
        return num1 - num2

class Multiplication(Operation):
    def execute(self, num1, num2):
        return num1 * num2

class Division(Operation):
    def execute(self, num1, num2):
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2

class Server:
    def __init__(self):
        self.server_address = ('localhost', 65432)

    def perform_operation(self, num1, num2, operation):
        logging.info("---- Function perform_operation Enter ----")
        operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division()
        }
        if operation in operations:
            result = operations[operation].execute(num1, num2)
        else:
            result = "Invalid operation"
        logging.info(f"---- Function perform_operation Exit with Result: {result} ----")
        return result

    def handle_client(self, connection):
        data = connection.recv(1024).decode('utf-8')
        logging.info(f"---- Function handle_client Enter with the data: {data} ----")
        num1, num2, operation = data.split(',')
        result = self.perform_operation(float(num1), float(num2), operation)
        connection.sendall(str(result).encode('utf-8'))
        logging.info(f"---- Function handle_client Exit with the result: {result} ----")

    def run(self):
        logging.info("---- Function run Enter ----")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.server_address)
            s.listen()
            print("Server is listening, can you sing?...")
            while True:
                connection, client_address = s.accept()
                with connection:
                    logging.info(f"Connected to {client_address}")
                    self.handle_client(connection)
        logging.info("---- Function run Exit ----")


if __name__ == "__main__":
    server = Server()
    server.run()
