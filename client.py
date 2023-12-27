class Client:
    def __init__(self, client_id, thread, status='active'):
        self.client_id = client_id
        self.thread = thread
        self.status = status

    def __str__(self):
        return f"Client {self.client_id} - Status: {self.status}"
