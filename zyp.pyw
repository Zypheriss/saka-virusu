import tkinter as tk
import time
import sys
import platform

class ScreenLocker:
    def __init__(self, lock_time=120):
        self.root = tk.Tk()
        self.lock_time = lock_time
        self.start_time = time.time()
        self.setup_ui()
        self.block_shortcuts()
        self.update_timer()
        
    def setup_ui(self):
        self.root.title("Kilitli Ekran")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.config(cursor='none') 
        self.root.configure(bg='black')
        self.label = tk.Label(
            self.root, 
            text=self.get_remaining_text(self.lock_time),
            font=("Arial", 24), 
            fg="red",
            bg='black'
        )
        self.label.pack(expand=True)
        info_text = "hahah bilgisayarın Gitti Github : zypheriss"
        self.info_label = tk.Label(
            self.root,
            text=info_text,
            font=("Arial", 12),
            fg="white",
            bg='black'
        )
        self.info_label.pack(side='bottom', pady=20)
        sys_info = f"Sistem: {platform.system()} {platform.release()}"
        self.sys_label = tk.Label(
            self.root,
            text=sys_info,
            font=("Arial", 10),
            fg="gray",
            bg='black'
        )
        self.sys_label.pack(side='bottom')
    
    def get_remaining_text(self, remaining):
        minutes, seconds = divmod(remaining, 60)
        return f"Ekran {minutes:02d}:{seconds:02d}  Hay da bilgisayara birşey oldu"
    
    def block_shortcuts(self):
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)
        for key in ['<Alt-F4>', '<Control-q>', '<Control-w>', '<Control-Alt-Delete>', 
                    '<Alt-Tab>', '<Win_L>', '<Win_R>', '<F11>', '<Escape>']:
            self.root.bind(key, self.do_nothing)
        if platform.system() == 'Darwin':
            for key in ['<Command-q>', '<Command-w>']:
                self.root.bind(key, self.do_nothing)
    
    def do_nothing(self, event=None):
        return "break"
    
    def update_timer(self):
        elapsed = time.time() - self.start_time
        remaining = max(0, self.lock_time - int(elapsed))
        
        if remaining > 0:
            self.label.config(text=self.get_remaining_text(remaining))
            self.root.after(1000, self.update_timer)
        else:
            self.unlock_screen()
    
    def unlock_screen(self):
        self.label.config(text="bu sadece bir şakaydı ya Esc bas ya da tab at çıkmak için Github : zypheriss")
        self.info_label.config(text="")
        self.root.unbind('<Escape>')
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.block_shortcuts()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    lock_time = 5
    if len(sys.argv) > 1:
        try:
            lock_time = int(sys.argv[1])
        except ValueError:
            print("Geçersiz süre varsayılan 5 süresi kullanılıyor")
    
    app = ScreenLocker(lock_time)
    app.run()
