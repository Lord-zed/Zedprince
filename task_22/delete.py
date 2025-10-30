from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"id": 1, "name": "Abdulmalik", "Track": "AI Engineer"},
    {"id": 2, "name": "Ope", "Track": "AI Developer"},
    {"id": 3, "name": "Fatimah", "Track": "DevOp"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):
        content_size = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_size)
       
        try:
            delete_data = json.loads(put_data)
        except json.JSONDecodeError:
            self.send_data({"error": "Invalid JSON format"}, status=400)
            return

        id = delete_data.get("id")
        if id is None:
            self.send_data({"error": "Missing 'id' in request body"}, status=400)
            return

        for record in data:
            if record["id"] == id:
                data.remove(record)
                self.send_data({
                    "message": f"Record {id} deleted successfully",
                    "remaining_data": data
                })
                return
            
        self.send_data({"error": f"Record with id {id} not found"}, status=404)

def run():
    HTTPServer(('localhost', 8008), BasicAPI).serve_forever()

print("Application Running")
run()