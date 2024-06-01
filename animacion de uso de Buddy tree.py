import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

class BuddyTree:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.free_blocks = [(0, 0, width, height)]
        self.allocated_blocks = []

    def allocate(self, size):
        for i, (x, y, w, h) in enumerate(self.free_blocks):
            if w >= size and h >= size:
                self.free_blocks.pop(i)
                self.allocated_blocks.append((x, y, size, size))
                if w > size:
                    self.free_blocks.append((x + size, y, w - size, h))
                if h > size:
                    self.free_blocks.append((x, y + size, size, h - size))
                return (x, y, size, size)
        return None

    def deallocate(self, block):
        self.allocated_blocks.remove(block)
        self.free_blocks.append(block)
        self.free_blocks = sorted(self.free_blocks)

    def draw(self, ax):
        ax.clear()
        for x, y, w, h in self.free_blocks:
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        for x, y, w, h in self.allocated_blocks:
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='g', facecolor='g', alpha=0.5)
            ax.add_patch(rect)
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        plt.gca().invert_yaxis()

# Crear una instancia del Buddy Tree
buddy_tree = BuddyTree(16, 16)

# Lista de operaciones (tamaño del bloque a asignar o liberar)
operations = [
    ('allocate', 8), ('allocate', 4), ('allocate', 4),
    ('deallocate', (0, 0, 8, 8)), ('allocate', 2), ('allocate', 2),
    ('deallocate', (0, 8, 4, 4)), ('allocate', 4)
]

# Configurar la figura y el eje
fig, ax = plt.subplots()

def update(frame):
    op, size_or_block = frame
    if op == 'allocate':
        buddy_tree.allocate(size_or_block)
    elif op == 'deallocate':
        buddy_tree.deallocate(size_or_block)
    buddy_tree.draw(ax)

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=operations, repeat=False, interval=1000)

plt.show()
