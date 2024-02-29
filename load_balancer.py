import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format=("%(asctime)s %(levelname)s %(message)s"))


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, server_address):
        super().__init__()
        self.client_socket = client_socket

        self.server_address = server_address

    def run(self):
        try:
            logging.info("2")
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            socket_server.connect(self.server_address)
            logging.info("1")
            request = self.build_request()
            logging.info(f"{request.decode()}")
            socket_server.sendall(request)
            logging.info("2")
            response = b""
            while True:
                data = socket_server.recv(1024)  # Receive data from the server
                if not data:
                    break  # Break the loop if no more data is received
                response += data
            logging.info("3")
            # Log the received response
            logging.info("Received from server: %s", response.decode())

            # Send the response back to the client
            self.client_socket.sendall(response)

            self.client_socket.sendall(response)
        except Exception as e:
            logging.info(f"error occured {e}")

        finally:
            self.client_socket.close()
            socket_server.close()

    def build_request(self):
        method = "GET"
        path = "/"
        http_version = "HTTP/1.1"
        host = self.server_address[0]

        request = f"{method} {path} {http_version}\r\n"
        request += f"Host: {host}\r\n"
        request += "\r\n"

        return request.encode()


class LoadBalancer:
    def __init__(self, self_address, backend_server_addresses):
        self.self_address = self_address
        self.backend_server_addresses = backend_server_addresses
        self.round_robin_index = 0

    def run(self):
        try:
            # socket.AF_INET for Address Family INET which is for IpV4
            # socket.SOCK_STREAM is for TCP
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind(self.self_address)
            socket_server.listen(5)

            # Log a message indicating that the load balancer is listening
            logging.info("Load balancer is listening on port %s...", self.self_address[1])
            while True:
                client_socket, _ = socket_server.accept()
                logging.info("Accepting connection from %s:%s", *_)

                # choose a backend server address
                routing_to_this_server = self.backend_server_addresses[self.round_robin_index]

                self.round_robin_index = (self.round_robin_index + 1) % len(self.backend_server_addresses)

                backend_server_domain = routing_to_this_server[0]
                backend_server_port = routing_to_this_server[1]
                logging.info(f"Request served by backend_server -> {backend_server_domain}:{backend_server_port}")

                client_handler = ClientHandler(client_socket, routing_to_this_server)
                client_handler.start()
        except Exception as e:
            logging.info(f"error occurred {e}")

        finally:
            socket_server.close()


if __name__ == "__main__":
    lb_address = ("127.0.0.1", 9000)
    backend_servers = [("127.0.0.1", 8000), ("127.0.0.1", 8001), ("127.0.0.1", 8002), ("127.0.0.1", 8003)]
    lb = LoadBalancer(lb_address, backend_servers)

    lb.run()
