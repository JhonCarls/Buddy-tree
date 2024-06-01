import math
import tkinter as tk
from tkinter import simpledialog, messagebox

class BuddySystem:
    def __init__(self, size):
        self.size = size
        self.memory = [None] * size
        self.blocks_occupied = 0

    def allocate(self, request_size):
        block_size = 1
        while block_size < request_size:
            block_size *= 2

        start_index = self.find_free_block(block_size)
        if start_index is None:
            return None, None

        for i in range(start_index, start_index + block_size):
            self.memory[i] = block_size
        self.blocks_occupied += block_size
        return start_index, block_size

    def find_free_block(self, block_size):
        start_index = 0
        while start_index < self.size:
            if self.memory[start_index] is None:
                size = 1
                while start_index + size < self.size and self.memory[start_index + size] is None:
                    size *= 2
                if size >= block_size:
                    return start_index
                start_index += size
            else:
                start_index += max(self.memory[start_index], block_size)
        return None

    def free(self, request_size):
        if request_size <= 0:
            return

        size_freed = 0
        start_index = 0
        while start_index < self.size:
            if self.memory[start_index] is not None:
                block_size = self.memory[start_index]
                if block_size >= request_size:
                    for i in range(start_index, start_index + request_size):
                        self.memory[i] = None
                    self.blocks_occupied -= request_size
                    size_freed = request_size
                    break
                start_index += block_size
            else:
                start_index += 1
        
        if size_freed > 0:
            memory_freed = 2 ** math.ceil(math.log(size_freed, 2))
            messagebox.showinfo("Memoria Liberada", f"Se han liberado {memory_freed} unidades de memoria.")

class MemorySimulator:
    def __init__(self, root, buddy_system):
        self.root = root
        self.buddy_system = buddy_system
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        size = self.buddy_system.size
        cell_size = 25
        num_cells_per_row = 32
        for i in range(size):
            x0 = (i % num_cells_per_row) * cell_size
            y0 = (i // num_cells_per_row) * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            color = "white" if self.buddy_system.memory[i] is None else "black"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
            text_color = "black" if self.buddy_system.memory[i] is None else "white"
            if self.buddy_system.memory[i] is not None and (i % self.buddy_system.memory[i]) == 0:
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(self.buddy_system.memory[i]), fill=text_color)
            elif self.buddy_system.memory[i] is None:
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(1), fill=text_color)

def request_memory():
    size = simpledialog.askinteger("Solicitud de Memoria", "Ingrese el tamaño del bloque:")
    if size is not None:
        start_index, block_size = buddy_system.allocate(size)
        if start_index is not None:
            messagebox.showinfo("Asignación Exitosa", f"Se asignaron {block_size} unidades de memoria en el índice {start_index}.")
            simulator.update_canvas()
        else:
            messagebox.showerror("Error de Asignación", "No hay suficiente memoria disponible.")

def free_memory():
    size = simpledialog.askinteger("Liberar Memoria", "Ingrese la cantidad de bloques a liberar:")
    if size is not None:
        buddy_system.free(2 ** math.ceil(math.log(size, 2)))
        simulator.update_canvas()

root = tk.Tk()
root.title("Simulador del Sistema Buddy")

buddy_system = BuddySystem(1024)

simulator = MemorySimulator(root, buddy_system)

request_button = tk.Button(root, text="Solicitar Memoria", command=request_memory)
request_button.pack()

free_button = tk.Button(root, text="Liberar Memoria", command=free_memory)
free_button.pack()

root.mainloop()
