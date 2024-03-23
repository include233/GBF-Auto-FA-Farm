import tkinter as tk
import threading
import pyautogui
import time
import random
x = 105
y = 530
loc_x, loc_y = None, None
Glb_sleep = 3

def find_and_adjust(image, confidence=0.7):
    global loc_x, loc_y
    try:
        loc_x, loc_y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if loc_x is not None and loc_y is not None:
            loc_y += 100
            print(f"Found at ({loc_x}, {loc_y-100}). Adjusted to ({loc_x}, {loc_y}).")
    except pyautogui.ImageNotFoundException:
        print('Cannot find the location.')

def click(x, y):
    pyautogui.click(x, y)

def find_and_click(image, confidence=0.7):
    cnt=0
    while cnt<=20:
        cnt+=1
        if(image!='ok_button_3.png'):
                try:
                    px=None
                    py=None
                    px, py = pyautogui.locateCenterOnScreen('ok_button_3.png', confidence=0.7)
                    if px is not None and py is not None:
                        click(px, py)
                        print("ok")
                        print(f"Found at ({px}, {py}). Adjusted to ({px}, {py}).")
                        time.sleep(2)
                except pyautogui.ImageNotFoundException:
                    print("No ok")
                try:
                    px=None
                    py=None
                    px, py = pyautogui.locateCenterOnScreen('ok_res.png', confidence=0.99)
                    if px is not None and py is not None:
                        click(px, py)
                        print("special ok")
                        print(f"Found at ({px}, {py}). Adjusted to ({px}, {py}).")
                        time.sleep(2)
                except pyautogui.ImageNotFoundException:
                    print("No special ok")
        try:  
            x, y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            if x is not None and y is not None:
                click(x, y)
                print(f"see the location {image}")
                print(f"Found at ({x}, {y}). Adjusted to ({x}, {y}).")
                break
        except pyautogui.ImageNotFoundException:
            print(f'Cannot see the location {image}')
            click(loc_x+random.uniform(1,10),loc_y+random.uniform(1,10))
            time.sleep(2)
            if(image!='ok_button_3.png'):
                try:
                    px=None
                    py=None
                    px, py = pyautogui.locateCenterOnScreen('ok_button_3.png', confidence=0.65)
                    if px is not None and py is not None:
                        click(px, py)
                        print("ok")
                        print(f"Found at ({px}, {py}). Adjusted to ({px}, {py}).")
                except pyautogui.ImageNotFoundException:
                    print("No ok")
            time.sleep(3)

def lobby(de):
    time.sleep(de)
    if(loc_x==None):
            find_and_adjust('6s.png',0.5)
    found = False

    for i in range(1,11):
        try:
            px=None
            py=None
            px, py = pyautogui.locateCenterOnScreen('ok_button_3.png', confidence=0.65)
            if px is not None and py is not None:
                click(px, py)
                print("find ok")
                print(f"Found at ({px}, {py}). Adjusted to ({px}, {py}).")
                time.sleep(2)
        except pyautogui.ImageNotFoundException:
            print(f"try {i} times")
            time.sleep(0.3)

    for image, name in [('kaguya.png', 'kaguya')]:
        print(f"Looking for {name}")
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=0.9)
            if x is not None and y is not None:
                time.sleep(Glb_sleep)
                click(x, y)
                found = True
                break
        except pyautogui.ImageNotFoundException:
            print(f"Not found... Looking for {name}")
    if not found:
        print("Not found any. Clicking the topmost summon")
        if(loc_x==None):
            find_and_adjust('6s.png',0.5)
        time.sleep(Glb_sleep)
        click(loc_x,loc_y)

    time.sleep(2)
    find_and_click('ok_button_3.png',0.65)

def attack(de):
    time.sleep(de)
    find_and_click('fa.jpg')
    time.sleep(3)

def tryagain(de):
    time.sleep(de)
    find_and_click('ok_button_3.png',0.65)
    time.sleep(2)
    find_and_click('play_again.png',0.9)

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("auto farm")
        
        self.start_button = tk.Button(root, text="start", command=self.start_auto_clicker)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_reset_button = tk.Button(root, text="stop", command=self.stop_or_reset_auto_clicker)
        self.stop_reset_button.pack(side=tk.RIGHT, padx=10)
        
        self.auto_clicker_running = False
        self.auto_clicker_thread = None
        self.stopped = False

    def start_auto_clicker(self):
        if not self.auto_clicker_running:
            self.auto_clicker_running = True
            self.stopped = False
            self.auto_clicker_thread = threading.Thread(target=self.run_auto_clicker)
            self.auto_clicker_thread.start()
    
    def stop_or_reset_auto_clicker(self):
        if self.auto_clicker_running:
            self.stopped = True
            self.auto_clicker_running = False
        else:
            # Reset function if needed
            pass
    
    def run_auto_clicker(self):
        while self.auto_clicker_running:
            if self.stopped:
                break
            lobby(3)
            attack(1)
            tryagain(1)

    def on_closing(self):
        if self.auto_clicker_running:
            self.stopped = True
            self.auto_clicker_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
