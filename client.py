import socket
import logging

# Client-side logger setup
logging.basicConfig(filename="client.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Client:
    def __init__(self):
        self.server_address = ('localhost', 65432)

    def send_data_to_server(self, data):
        logging.info("---- Function send_data_to_server Enter ----")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
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
    client = Client()
    client.run()
