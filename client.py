import socket
import logging
import sys

# Client-side logger setup
logging.basicConfig(filename="client.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
SERVER_HOST = 'localhost'
SERVER_PORT = 65432

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_data_to_server(self, data):
        logging.info("---- Function send_data_to_server Enter ----")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host,self.port))
            s.sendall(data.encode('utf-8'))
            result = s.recv(1024).decode('utf-8')
            logging.info(f"---- Function send_data_to_server Exit with the result {result} ----")
            return result

    def get_user_input(self):
        logging.info("---- Function get_user_input Enter ----")
        num1 = input("Enter the first number: ")
        num2 = input("Enter the second number: ")
        operation = input("Enter the operation (+, -, *, /): ")
        data = f"{num1},{num2},{operation}"
        logging.info(f"---- Function get_user_input Exit with data: {data} ----")
        return data

    def run(self):
        logging.info("---- Function run Enter ----")
        data = self.get_user_input()
        result = self.send_data_to_server(data)
        print(f"Result: {result}")
        logging.info(f"---- Function run Exit with result {result} ----")


if __name__ == "__main__":
    # Ensure command-line arguments are used correctly
    if len(sys.argv) != 4:
        print("Usage: client.py <num1> <num2> <operation>")
        sys.exit(1)

    num1 = sys.argv[1]
    num2 = sys.argv[2]
    operation = sys.argv[3]

    client = Client(SERVER_HOST, SERVER_PORT)
    operation_string = f"{num1},{num2},{operation}"
    result = client.send_data_to_server(operation_string)

    # Print the result in the expected format for tests
    print(f"Result: {result}")