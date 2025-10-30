from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"id": 1, "name": "Mahfuz", "Track": "AI Engineer"},
    {"id": 2, "name": "Olawale", "Track": "AI Developer"},
    {"id": 3, "name": "Rofiat", "Track": "DevOp"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

       
    def do_PUT(self):
        content_size = int(self.headers.get('Content-Length', 0))
        update_data = self.rfile.read(content_size)
        put_data = json.loads(update_data)
        id = put_data.get("id")

        if id is None:
            self.send_data({"error": "Missing 'id' in request body"}, status=400)
            return

        for record in data:
            if record["id"] == id:
                record.update(put_data)
                self.send_data({
                    "message": "Data updated successfully",
                    "updated_data": record
                })
                return

        self.send_data({"error": f"Record {id} not found"}, status=404)


def run():
    HTTPServer(('localhost', 8008), BasicAPI).serve_forever()


print("Application running")
run()