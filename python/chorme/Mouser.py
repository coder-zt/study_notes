import pyautogui

class Mouser:
    
    def click(self, x, y):
        self.x = x
        self.y = y
        pyautogui.click(x, y,  duration=1)
        
    def clickRelative(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        pyautogui.click(self.x, self.y, duration=1)