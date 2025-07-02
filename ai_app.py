import tkinter as tk
from tkinter import scrolledtext
import threading

from main import graph, ChatState


class AIApp:
    def __init__(self, root):
        self.state: ChatState = {"messages": []}

        root.title("Local AI Assistant")
        root.geometry("500x600")
        root.configure(bg="#1e1e2e")

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), bg="#121212", fg="#ffffff")
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, font=("Courier", 12), bg="#1f1f1f", fg="white")
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(root, text="Send", command=self.send_message, bg="#7E3A3A", fg="white", relief=tk.FLAT)
        self.send_btn.pack(padx=10, pady=(0, 10))

        self.log(" LocalAI Ready. Type a question or request:")

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.log(f" You: {user_input}")
        self.entry.delete(0, tk.END)
        self.state['messages'].append({'role': 'user', 'content': user_input})

        threading.Thread(target=self.process_message).start()

    def process_message(self):
        try:
            self.state = graph.invoke(self.state)
            last_msg = self.state['messages'][-1]

            if isinstance(last_msg, dict):
                assistant_msg = last_msg.get('content', '')
            else:
                assistant_msg = getattr(last_msg, 'content', '')

            self.log(f"AI: {assistant_msg}")
        except Exception as e:
            self.log(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()