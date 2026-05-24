import socket
import threading
from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog
from textual.containers import Vertical

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.13", 8080))


class ChatApp(App):

    def compose(self) -> ComposeResult:
        yield Vertical(
            RichLog(id="log"),
            Input(placeholder="Type message...", id="input"),
        )

    def on_mount(self):
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while True:
            try:
                msg = client.recv(1024).decode()
                if msg:
                    self.call_from_thread(
                        self.query_one("#log", RichLog).write,
                        f"Server: {msg}"
                    )
            except:
                break

    def on_input_submitted(self, event: Input.Submitted):
        msg = event.value.strip()
        if not msg:
            return

        client.send(msg.encode())

        self.query_one("#log", RichLog).write(f"You: {msg}")
        self.query_one("#input", Input).value = ""


if __name__ == "__main__":
    ChatApp().run()
