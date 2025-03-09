import curses
import threading
from queue import Queue

class Terminal:
    def __init__(self, title, height, width, y, x):
        self.title = title
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.messages = Queue()
        self.window = None
        
    def setup(self):
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.window.box()
        self.window.addstr(0, 2, f" {self.title} ")
        self.window.refresh()
        
    def add_message(self, message):
        self.messages.put(message)
        if self.window:
            self._display_messages()
            
    def _display_messages(self):
        y = 1
        messages = []
        while not self.messages.empty() and y < self.height - 1:
            msg = self.messages.get()
            self.window.addstr(y, 1, msg[:self.width-2])
            y += 1
        self.window.refresh() 