import matplotlib.pyplot as plt

def get_input():
    entities = []
    x_positions = []
    y_positions = []
    sizes = []

    n = int(input("Enter the number of entities: "))

    for _ in range(n):
        entity = input("Enter the name of the entity: ")
        x_pos = float(input(f"Enter the x position for {entity}: "))
        y_pos = float(input(f"Enter the y position for {entity}: "))
        size = float(input(f"Enter the size of the dot for {entity}: "))

        entities.append(entity)
        x_positions.append(x_pos)
        y_positions.append(y_pos)
        sizes.append(size)

    x_axis_name = input("Enter the name for the X axis: ")
    y_axis_name = input("Enter the name for the Y axis: ")

    return entities, x_positions, y_positions, sizes, x_axis_name, y_axis_name

def generate_bubble_chart(entities, x_positions, y_positions, sizes, x_axis_name, y_axis_name):
    dpi = 80
    width_in_inches = 1920 / dpi
    height_in_inches = 1080 / dpi

    fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches))
    scatter = ax.scatter(x_positions, y_positions, s=sizes, alpha=0.6, label=entities)

    # Add labels to the bubbles
    for i, entity in enumerate(entities):
        ax.annotate(entity, (x_positions[i], y_positions[i]))

    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title("Bubble Chart")

    # Create a legend
    legend_labels = [f'{entity} ({size})' for entity, size in zip(entities, sizes)]
    handles, _ = scatter.legend_elements(prop="sizes", alpha=0.6)
    ax.legend(handles, legend_labels, title="Entities")

    # Save the figure as a PNG
    plt.savefig("bubble_chart.png", dpi=dpi)
    plt.show()

def main():
    entities, x_positions, y_positions, sizes, x_axis_name, y_axis_name = get_input()
    generate_bubble_chart(entities, x_positions, y_positions, sizes, x_axis_name, y_axis_name)

if __name__ == "__main__":
    main()
