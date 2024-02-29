from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world!')


def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    ports = [8000, 8001, 8002, 8003]

    for port in ports:
        server_thread = threading.Thread(target=run_server, args=(port,))
        server_thread.start()
