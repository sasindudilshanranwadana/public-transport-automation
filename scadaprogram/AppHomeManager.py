

class AppHomeManager:
    def __init__(self, homes, canvas):
        self.homes = homes
        self.canvas = canvas

    def draw_homes(self):
        for i, (x, y) in enumerate(self.homes):
            self.canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25, outline="red", width=2, fill="blue")
            self.canvas.create_text(x, y + 15, text=f"HOME {i+1}", font=("Arial", 9), fill="white")
