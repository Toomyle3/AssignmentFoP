import numpy as np
import matplotlib.pyplot as plt
import random

class Item:
    def __init__(self, name, color, thermal_value):
        self.name = name
        self.color = color
        self.thermal_value = thermal_value

    def get_rgb(self):
        return np.array(self.color) / 255

    def get_thermal_value(self):
        return self.thermal_value

class Block:
    def __init__(self, position, block_type='house'):
        self.position = position
        self.items = []
        self.block_type = block_type
        self.background_color = self.set_background_color()

    def set_background_color(self):
        if self.block_type == 'house':
            return (255, 255, 255)
        elif self.block_type == 'road':
            return (128, 128, 128)
        return (0, 0, 0)

    def add_item(self, item):
        self.items.append(item)

    def get_rgb(self):
        if not self.items:
            return np.array(self.background_color) / 255
        avg_color = np.mean([item.get_rgb() for item in self.items], axis=0)
        return avg_color

    def get_thermal_value(self):
        if not self.items:
            return 25
        avg_thermal = np.mean([item.get_thermal_value() for item in self.items])
        return avg_thermal

    def get_item_names(self):
        if self.items:
            color_to_name = {tuple(item.get_rgb()): item.name for item in self.items}
            return color_to_name
        return {tuple(np.array(self.background_color) / 255): self.block_type}

    
def create_map(height, width):
    blocks = np.empty((height, width), dtype=object)
    house_count = 0
    tree_count = 0

    for i in range(height):
        for j in range(width):
            # Draw a road in the middle
            if 3 < j < 6:
                block = Block(position=(i, j), block_type='road')
            else:
                block_type = 'house' if random.random() > 0.3 else 'tree'
                block = Block(position=(i, j), block_type=block_type)

                if block_type == 'house':
                    if house_count > tree_count:
                        item = Item("Tree", (0, 128, 0), -1)
                        block.add_item(item)
                        tree_count += 1
                    house_count += 1
                elif block_type == 'tree':
                    item = Item("Tree", (0, 128, 0), -1)
                    block.add_item(item)
                    tree_count += 1

            blocks[i, j] = block
    return blocks

def calculate_overall_thermal(map_blocks):
    total_thermal = 10
    count = 0

    for i in range(map_blocks.shape[0]):
        for j in range(map_blocks.shape[1]):
            if map_blocks[i, j].block_type != 'road':
                total_thermal += map_blocks[i, j].get_thermal_value()
                count += 1

    return total_thermal / count if count > 0 else 25

def generate_views(map_blocks, overall_thermal):
    height, width = map_blocks.shape
    rgb_view = np.zeros((height, width, 3))
    thermal_view = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            rgb_view[i, j] = map_blocks[i, j].get_rgb()
            if map_blocks[i, j].block_type == 'road':
                thermal_view[i, j] = overall_thermal
            else:
                thermal_view[i, j] = map_blocks[i, j].get_thermal_value()

    return rgb_view, thermal_view

def draw_map(rgb_view, thermal_view, map_blocks):
    fig, axs = plt.subplots(1, 2, figsize=(8, 4))

    axs[0].imshow(rgb_view)
    axs[0].set_title("RGB View", fontsize=16, fontweight='bold', fontfamily='serif')
    axs[0].axis('off')

    cax = axs[1].imshow(thermal_view, cmap='hot_r', vmin=-30, vmax=30)
    axs[1].set_title("Thermal View", fontsize=16, fontweight='bold', fontfamily='serif')
    axs[1].axis('off')
    fig.colorbar(cax, ax=axs[1], label="°C")

    plt.tight_layout()
    
    # Tooltips
    tooltip = axs[0].text(0, 0, "", va="bottom", ha="left", fontsize=12, color="black", fontweight="bold", bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    tooltip.set_visible(False)

    def on_hover(event):
        if event.inaxes == axs[0]:
            i, j = int(event.ydata), int(event.xdata)
            if 0 <= i < rgb_view.shape[0] and 0 <= j < rgb_view.shape[1]:
                rgb_color = tuple(rgb_view[i, j])
                item_names = map_blocks[i, j].get_item_names()
                closest_item = None
                min_diff = float('inf')

                for color, name in item_names.items():
                    diff = np.linalg.norm(np.array(rgb_color) - np.array(color))
                    if diff < min_diff:
                        min_diff = diff
                        closest_item = name
                
                tooltip.set_position((event.xdata, event.ydata))
                tooltip.set_text(f"{closest_item}" if closest_item else "Empty")
                tooltip.set_visible(True)
                fig.canvas.draw_idle()
            else:
                tooltip.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", on_hover)
    
    plt.show()

if __name__ == "__main__":
    height = 10
    width = 10
    blocks = create_map(height, width)
    overall_thermal = calculate_overall_thermal(blocks)
    rgb_view, thermal_view = generate_views(blocks, overall_thermal)
    draw_map(rgb_view, thermal_view, blocks)
