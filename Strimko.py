import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
import tkinter.messagebox

def popup(msg):
    """"Otevre popup tutorial"""
    window = tkinter.Tk()
    window.wm_withdraw()
    tkinter.messagebox.showinfo(title="Tutorial", message=msg)
    window.destroy()
    return None
popup("Drž levý shift a levým tlačítkem vyber kolečka(pole) které budou v jednom řetězci pak pusť shift a řetězec se zvýrazní. Samotným kliknutím levého tlačítka lze zapisovat čísla. Pak klikni na doplnit čísla a je to")

class CircleGridApp:
    def __init__(self, master, size=6):
        self.master = master
        self.master.title("Interaktivní mřížka kruhů")
        self.size = size
        self.canvas = None  # canvas bude inicializován později
        self.radius = 20
        self.spacing = 600 // self.size  # Dynamické nastavení rozestupů podle velikosti
        self.circles = {}
        self.circle_number = {}  # Mapování kruhů na jejich čísla
        self.selected_circle = None
        self.selected_circles = []  # Seznam spojených kruhů
        self.shift_held = False  # Kontrola, zda je stisknutý L Shift
        self.lines = []  # Seznam čar mezi spojenými kruhy
        self.connected_sets = []  # Seznam všech spojených kruhů (řetězců)

        self.create_canvas()  # Vytvoříme plátno
        self.draw_grid()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<KeyPress-Shift_L>", self.on_shift_press)
        self.canvas.bind("<KeyRelease-Shift_L>", self.on_shift_release)

        self.canvas.focus_set()

        self.fill_button = tk.Button(master, text="Doplnit čísla", command=self.fill_numbers)
        self.fill_button.pack()

        # Přidání tlačítka Reset
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.pack(pady=5)

        # Přidání tlačítka pro změnu velikosti mřížky
        self.change_size_button = tk.Button(master, text="Změnit velikost mřížky", command=self.change_grid_size)
        self.change_size_button.pack(pady=5)

    def create_canvas(self):
        """Vytvoří nové plátno (canvas)."""
        if self.canvas:
            self.canvas.destroy()  # Odstraní starý canvas, pokud existuje
        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="white")
        self.canvas.pack()



    def reset_grid(self):
        """Resetuje mřížku do původního stavu."""
        # Odstraní všechna čísla
        for circle_id in self.circle_number.keys():
            self.canvas.delete(f"text_{circle_id}")
        self.circle_number.clear()

        # Resetuje barvy kruhů
        for circle_id in self.circles:
            self.canvas.itemconfig(circle_id, fill="white")

        # Vyprázdní seznamy a resetuje stav
        self.selected_circles.clear()
        self.connected_sets.clear()
        self.clear_lines()

        self.draw_grid()  # Znovu vykreslí mřížku po resetu

    def change_grid_size(self):
        """Změní velikost mřížky podle uživatelského vstupu."""
        new_size = askinteger("Nová velikost mřížky", "Zadejte novou velikost mřížky (např. 7):", minvalue=2, maxvalue=20)
        if new_size and new_size != self.size:
            self.size = new_size
            self.spacing = 600 // self.size  # Aktualizace rozestupů podle nové velikosti
            self.master.destroy()  # Zavře staré okno
            self.open_new_window()  # Otevře nové okno s novou velikostí

    def open_new_window(self):
        """Otevře nové okno s novou mřížkou."""
        new_root = tk.Tk()  # Vytvoří nové okno
        app = CircleGridApp(new_root, self.size)  # Vytvoří novou instanci aplikace
        new_root.mainloop()  # Spustí hlavní smyčku nového okna

    def highlight_circle(self, event):
        """Zvýrazní kruh při najetí myší."""
        circle_id = self.canvas.find_withtag("current")
        if circle_id and circle_id[0] in self.circles:
            self.original_fill = self.canvas.itemcget(circle_id[0], "fill")
            self.canvas.itemconfig(circle_id[0], fill="yellow")

    def unhighlight_circle(self, event):
        """Zruší zvýraznění kruhu při opuštění myši."""
        circle_id = self.canvas.find_withtag("current")
        if circle_id and circle_id[0] in self.circles:
            self.canvas.itemconfig(circle_id[0], fill=self.original_fill)

    def draw_grid(self):
        """Vykreslí mřížku kruhů."""
        self.circles.clear()  # Vyprázdní seznam starých kruhů
        for row in range(self.size):
            for col in range(self.size):
                x = col * self.spacing + self.spacing // 2
                y = row * self.spacing + self.spacing // 2
                circle_id = self.canvas.create_oval(
                    x - self.radius, y - self.radius, x + self.radius, y + self.radius,
                    fill="white", outline="black", width=2
                )
                self.circles[circle_id] = (row, col)
                self.canvas.tag_bind(circle_id, "<Enter>", self.highlight_circle)
                self.canvas.tag_bind(circle_id, "<Leave>", self.unhighlight_circle)

    def on_click(self, event):
        """Zpracuje kliknutí uživatele."""
        clicked_items = self.canvas.find_withtag("current")
        if not clicked_items:
            return

        clicked_circle = clicked_items[0]
        if clicked_circle not in self.circles:
            return

        if self.shift_held:
            if clicked_circle not in self.selected_circles:
                self.selected_circles.append(clicked_circle)
                self.draw_lines()
        else:
            if clicked_circle not in self.circle_number:
                self.enter_number(clicked_circle)

    def on_shift_press(self, event):
        """Detekuje stisknutí L Shift."""
        self.shift_held = True

    def on_shift_release(self, event):
        """Detekuje uvolnění L Shift."""
        self.shift_held = False
        if len(self.selected_circles) > 1:
            self.create_chain(self.selected_circles)
        self.selected_circles = []

    def enter_number(self, circle_id):
        """Zobrazí dialog pro zadání čísla pro konkrétní kruh."""
        number = askstring("Zadejte číslo", "Zadejte číslo pro tento kruh:")
        if number and number.isdigit():
            number = int(number)
            if self.is_valid_number(circle_id, number):
                self.circle_number[circle_id] = number
                self.update_number_in_circle(circle_id, number)
            else:
                self.show_error("Číslo není platné (duplicitní ve sloupci, řádku nebo řetězci).")
        else:
            self.show_error("Zadejte platné číslo.")

    def update_number_in_circle(self, circle_id, number):
        """Aktualizuje zobrazené číslo u kruhu."""
        x1, y1, x2, y2 = self.canvas.coords(circle_id)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        self.canvas.delete(f"text_{circle_id}")
        self.canvas.create_text(cx, cy, text=str(number), font=("Arial", 12, "bold"), tag=f"text_{circle_id}")

    def show_error(self, message):
        """Zobrazí chybovou zprávu."""
        print(f"Chyba: {message}")

    def draw_lines(self):
        """Kreslí čáry mezi spojenými kruhy."""
        for i in range(len(self.selected_circles) - 1):
            circle_id1 = self.selected_circles[i]
            circle_id2 = self.selected_circles[i + 1]

            x1, y1, x2, y2 = self.canvas.coords(circle_id1)
            x1_c, y1_c = (x1 + x2) / 2, (y1 + y2) / 2

            x1, y1, x2, y2 = self.canvas.coords(circle_id2)
            x2_c, y2_c = (x1 + x2) / 2, (y1 + y2) / 2

            self.lines.append(self.canvas.create_line(x1_c, y1_c, x2_c, y2_c, fill="blue", width=2))

    def clear_lines(self):
        """Odstraní všechny čáry."""
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()

    def create_chain(self, circles):
        """Vytvoří nový řetězec z vybraných kruhů."""
        chain = set(circles)
        self.connected_sets.append(chain)
        for circle_id in circles:
            self.canvas.itemconfig(circle_id, fill="lightblue")

    def is_valid_number(self, circle_id, number):
        """Zkontroluje, zda je číslo platné pro daný kruh."""
        row, col = self.circles[circle_id]
        for other_circle_id, (r, c) in self.circles.items():
            if self.circle_number.get(other_circle_id) == number:
                if r == row or c == col:
                    return False
        for chain in self.connected_sets:
            if circle_id in chain and number in {self.circle_number.get(cid) for cid in chain}:
                return False
        return True

    def fill_numbers(self):
        """Doplní čísla do celé mřížky pomocí backtracking algoritmu."""
        all_circles = list(self.circles.keys())
        if self.solve(all_circles, 0):
            print("Mřížka byla úspěšně vyplněna.")
        else:
            print("Mřížku se nepodařilo vyplnit.")

    def solve(self, all_circles, index):
        """Backtracking algoritmus pro vyplnění mřížky."""
        if index == len(all_circles):
            return True

        circle_id = all_circles[index]
        if circle_id in self.circle_number:
            return self.solve(all_circles, index + 1)

        for number in range(1, self.size + 1):
            if self.is_valid_number(circle_id, number):
                self.circle_number[circle_id] = number
                self.update_number_in_circle(circle_id, number)

                if self.solve(all_circles, index + 1):
                    return True

                del self.circle_number[circle_id]
                self.canvas.delete(f"text_{circle_id}")

        return False


def main():
    root = tk.Tk()
    size = askinteger("Velikost mřížky", "Zadejte velikost mřížky (např. 6 pro 6x6):", minvalue=2, maxvalue=20)
    if size:
        app = CircleGridApp(root, size)
        root.mainloop()


if __name__ == "__main__":
    main()
