import http.server
import socket
import urllib.parse


# Define a simple handler to capture the code
class _SimpleCallbackHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging to keep the console clean
        return

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        code = None

        if "code" in query_params:
            code = query_params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization code received. You can close this window.")
            # Store code on the server instance
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Error: Authorization code not found.")

        # Signal the server to stop serving after this request
        self.server.authorization_code = code
        self.server.shutdown_signal = True


# Function to run the server, capture the code, and stop
def get_auth_code_via_server(port: int, timeout: int = 30) -> str:
    server_address = ("localhost", port)
    httpd = http.server.HTTPServer(server_address, _SimpleCallbackHandler)
    httpd.authorization_code = None  # Custom attribute to store the code
    httpd.shutdown_signal = False  # Custom attribute to signal completion

    # Set socket timeout to handle cases where the callback never happens
    httpd.timeout = timeout

    # Loop until the handler signals completion or timeout occurs
    while not httpd.shutdown_signal:
        try:
            httpd.handle_request()  # Process one request (blocking until one arrives or timeout)
        except socket.timeout:
            httpd.server_close()  # Ensure the socket is closed
            raise TimeoutError(
                f"Timeout: No callback received within {timeout} seconds."
            )
        except Exception as e:
            httpd.server_close()
            raise RuntimeError(f"Server error: {e}")

    # Server loop finished, close the server socket
    httpd.server_close()

    if httpd.authorization_code:
        return httpd.authorization_code
    else:
        raise ValueError("No authorization code received.")
