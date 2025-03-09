import subprocess
import os
import sys
import tempfile
from queue import Queue
from threading import Thread
import shutil

class TerminalWindow:
    def __init__(self, title):
        self.title = title
        self.message_queue = Queue()
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.process = None
        
    def start(self):
        terminal_cmd = self._get_terminal_command()
        if not terminal_cmd:
            print(f"Debug: No suitable terminal emulator found")
            return False
        
        try:
            if sys.platform == 'darwin':
                # Create a shell script file for the Python command
                script_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.sh')
                script_file.write(f'''#!/bin/bash
python3 -c 'import time; f=open("{self.temp_file.name}", "r")
while True:
    line = f.readline()
    if line:
        print(line.strip())
        time.sleep(0.1)
    else:
        time.sleep(0.5)
'
''')
                script_file.close()
                os.chmod(script_file.name, 0o755)
                
                # AppleScript to open new terminal
                script = (
                    'tell application "Terminal"\n'
                    f'    do script "{script_file.name}"\n'
                    f'    set custom title of front window to "{self.title}"\n'
                    '    activate\n'
                    'end tell'
                )
                cmd = ['osascript', '-e', script]
                self.process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
            elif sys.platform == 'win32':
                cmd = f'start "Python Poker - {self.title}" python -c "import time; f=open(\'{self.temp_file.name}\', \'r\'); print(\'{self.title}\'); [print(line.strip()) or time.sleep(0.1) for line in f]"'
                self.process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
            else:
                # Linux/Unix command construction
                python_cmd = f"python3 -c 'import time; f=open(\\\"{self.temp_file.name}\\\", \\\"r\\\"); print(\\\"{self.title}\\\"); [print(line.strip()) or time.sleep(0.1) for line in f]'"
                cmd = [terminal_cmd.split()[0]] + terminal_cmd.split()[1:] + [python_cmd]
                self.process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
            
            error = self.process.stderr.readline()
            if error:
                print(f"Debug: Terminal launch error: {error.decode()}")
                return False
            
            return True
        
        except Exception as e:
            print(f"Debug: Failed to start terminal: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
            
    def _get_terminal_command(self):
        print(f"Debug: Platform is {sys.platform}")
        
        if sys.platform == 'win32':
            return 'start'
        elif sys.platform == 'darwin':
            # macOS specific command
            return 'open -a Terminal.app'
        
        # Check if we're in a terminal
        if not os.environ.get('TERM'):
            print("Debug: No TERM environment variable found")
            return None
        
        # Check for various terminal emulators on Unix
        terminals = [
            ('x-terminal-emulator', 'x-terminal-emulator -e'),  # Debian/Ubuntu default
            ('xterm', 'xterm -T'),
            ('gnome-terminal', 'gnome-terminal --'),
            ('konsole', 'konsole -e'),
            ('terminator', 'terminator -x'),
            ('urxvt', 'urxvt -e'),
            ('xfce4-terminal', 'xfce4-terminal -x'),
            ('mate-terminal', 'mate-terminal -x')
        ]
        
        for term, cmd in terminals:
            term_path = shutil.which(term)
            if term_path:
                print(f"Debug: Found terminal emulator: {term} at {term_path}")
                return cmd
                
        print("Debug: No terminal emulators found in PATH")
        return None
        
    def write(self, message):
        self.temp_file.write(f"{message}\n")
        self.temp_file.flush()
        
    def close(self):
        if self.process:
            try:
                if sys.platform == 'darwin':
                    # Get the terminal window ID and quit it via AppleScript
                    script = '''
                        tell application "Terminal"
                            quit
                        end tell
                    '''
                    subprocess.run(['osascript', '-e', script])
                else:
                    self.process.terminate()
            except:
                pass
        self.temp_file.close()
        try:
            os.unlink(self.temp_file.name)
            if hasattr(self, 'script_file'):
                os.unlink(self.script_file.name)
        except:
            pass

class TerminalManager:
    def __init__(self):
        self.chat_window = TerminalWindow("Main Chat")
        self.game_display = TerminalWindow("Game Display")  # Add game display window
        self.thought_windows = {}
        self.fallback_mode = False
        
    def start_terminals(self, players):
        # Try to start game display window first
        if not self.game_display.start():
            self.fallback_mode = True
            print("\n=== Game Display ===")
            
        # Try to start chat window
        if not self.chat_window.start():
            self.fallback_mode = True
            print("\n=== Main Chat ===")
            
        # Start thought windows for each player
        for player in players:
            thought_window = TerminalWindow(f"{player.name}'s Thoughts")
            self.thought_windows[player.name] = thought_window
            
            if not self.fallback_mode and not thought_window.start():
                self.fallback_mode = True
                print(f"\n=== {player.name}'s Thoughts ===")
                
    def write_game_display(self, message):
        if self.fallback_mode:
            print(f"\n[Game Display] {message}")
        else:
            self.game_display.write(message)
            
    def write_chat(self, message):
        if self.fallback_mode:
            print(f"[Chat] {message}")
        else:
            self.chat_window.write(message)
            
    def write_thought(self, player_name, message):
        if self.fallback_mode:
            print(f"[{player_name} thinks] {message}")
        elif player_name in self.thought_windows:
            self.thought_windows[player_name].write(message)
            
    def close_all(self):
        if not self.fallback_mode:
            self.game_display.close()  # Add game display window cleanup
            self.chat_window.close()
            for window in self.thought_windows.values():
                window.close() 