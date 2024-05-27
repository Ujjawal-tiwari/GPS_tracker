import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

def initialize_json_file():
    initial_data = []
    with open("received_data.json", "a") as json_file:
        json.dump(initial_data, json_file, indent=4)
        json_file.flush()
        os.fsync(json_file.fileno())  # Force data to be written to disk
    print("JSON file initialized.")

# HTTP server request handler class
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        # Log the received data
        print("Received data:", data)

        # Write new data to the JSON file, overwriting existing content
        with open("received_data.json", "w") as json_file:
            json.dump([data], json_file, indent=4)
            json_file.flush()  # Explicit flush
            os.fsync(json_file.fileno())  # Force flush to disk

        # Send a success response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

# Run the HTTP server
def run_server():
    server_address = ('172.16.0.133', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    initialize_json_file()  # Create the JSON file at the beginning
    print("Starting HTTP server on port 8000...")
    httpd.serve_forever()

# Start the server if the script is run as the main program
if __name__ == '__main__':
    run_server()


# INCASE YOU WANT TO MAINTAIN A RECORD OF TRACED LOCATION

# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
#
# # Initialize an empty list to store received data
# received_data = []
#
# class RequestHandler(BaseHTTPRequestHandler):
#     # Handle POST requests
#     def do_POST(self):
#         global received_data
#
#         content_length = int(self.headers['Content-Length'])
#
#         # Read the POST data
#         post_data = self.rfile.read(content_length)
#         try:
#             data = json.loads(post_data)
#         except json.JSONDecodeError:
#             self.send_response(400)
#             self.end_headers()
#             self.wfile.write(b"Invalid JSON")
#             return
#
#         # Log the received data
#         print("Received data:", data)
#
#         # Append the new data to the list
#         received_data.append(data)
#
#         # Save the updated data to a JSON file
#         with open("received_data.json", "a") as json_file:
#             json.dump(received_data, json_file, indent=4)
#
#         # Send a success response
#         self.send_response(200)
#         self.send_header("Content-Type", "application/json")
#         self.end_headers()
#         self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
#
# def run_server():
#     server_address = ('172.16.0.207', 8000)
#     httpd = HTTPServer(server_address, RequestHandler)  # Create HTTP server
#     print("Starting HTTP server on port 8000...")
#     httpd.serve_forever()
#
# # Run the server
# if __name__ == '__main__':
#     run_server()