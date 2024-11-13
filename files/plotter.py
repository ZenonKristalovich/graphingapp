def draw_plot(canvas, matrix, row_names, plot_index, temperatures, 
              components, x_bounds, y_bounds, dashed_lines, title, 
              x_title, y_title, pointer_size, component_names, pointer_types,
              legend, colours,hollow, line, cap_size):
    
    canvas.axes.clear()
    pos = 2 * plot_index
    if pos + 1 >= len(matrix):
        return  # Exit if index is out of range

    y_data = matrix[pos]
    uncertainty_data = matrix[pos + 1]

    y_data_by_temp = [y_data[i:i + components] for i in range(0, len(y_data), components)]
    uncertainty_by_temp = [uncertainty_data[i:i + components] for i in range(0, len(uncertainty_data), components)]

    for j in range(components):
        values = [y_data_by_temp[i][j] for i in range(len(temperatures))]
        uncertainty_values = [uncertainty_by_temp[i][j] for i in range(len(temperatures))]
        
        # Set fmt='o' to use markers only, no connecting lines
        canvas.axes.errorbar(temperatures, values, yerr=uncertainty_values,
                             fmt=pointer_types[j], label=component_names[j], markersize=pointer_size, 
                             markerfacecolor= hollow[j],elinewidth=line, capsize=cap_size,
                             color=colours[j], markeredgewidth=line)

    if x_title == None:
        canvas.axes.set_xlabel('Temperature [K]', labelpad=10)
    else:
        canvas.axes.set_xlabel(x_title, labelpad=10)

    if y_title == None:
        canvas.axes.set_ylabel(row_names[pos] if pos < len(row_names) else "")
    else:
        canvas.axes.set_ylabel(y_title)

    if title == None:
        canvas.axes.set_title("")
    else:
        canvas.axes.set_title(title)

    # Apply bounds if they are not None
    if x_bounds is not None:
        split = x_bounds.split('|')
        canvas.axes.set_xlim(float(split[0]), float(split[1]))
    if y_bounds is not None:
        split = y_bounds.split('|')
        canvas.axes.set_ylim(float(split[0]), float(split[1]))

    # Add horizontal dashed lines for each value in dashed_lines
    if dashed_lines:
        count = 0
        for value in dashed_lines:
            count += 1
            canvas.axes.axhline(y=float(value), color='black', linestyle='--', linewidth=2, label=f"Bulk {count}")

    canvas.axes.grid(True)
    if legend == "TopRight":
        canvas.axes.legend(loc='upper right', bbox_to_anchor=(1.2, 1), borderaxespad=0.)
    elif legend == "TopLeft":
        canvas.axes.legend(loc='upper left', bbox_to_anchor=(-0.25, 1), borderaxespad=0.)
    elif legend == "BottomRight":
        canvas.axes.legend(loc='lower right', bbox_to_anchor=(1.2, 0), borderaxespad=0.)
    elif legend == "BottomLeft":
        canvas.axes.legend(loc='lower left', bbox_to_anchor=(-0.25, 0), borderaxespad=0.)
    else:
        canvas.axes.legend()
    
    canvas.figure.tight_layout()  # Automatically adjust layout to fit the plot and legend
    canvas.draw()

def draw_multi_plot(canvas, matrix, row_names, plot_index, component_index, files, temperatures, 
              components, x_bounds, y_bounds, dashed_lines, title, 
              x_title, y_title, pointer_size, component_names, pointer_types,
              legend, colours,hollow, line, cap_size):
    # Clear the previous plot on the canvas
    canvas.axes.clear()

    # Calculate the correct indices for plotting
    pos = 2 * plot_index
    if pos + 1 >= len(matrix):
        print("Index out of range")
        return

    # Extract y_data and uncertainty data
    y_data = matrix[pos][component_index]
    uncertainty_data = matrix[pos + 1][component_index]
    print(y_data)
    print(files)
    # Organize y_data and uncertainty data by components
    y_data_by_temp = [y_data[i:i + components] for i in range(0, len(y_data), files)]
    uncertainty_by_temp = [uncertainty_data[i:i + components] for i in range(0, len(uncertainty_data), files)]
    print(y_data_by_temp)

    # Plot the data for the selected component
    count = 0
    for file_idx, (y_values, uncertainty_values) in enumerate(zip(y_data_by_temp, uncertainty_by_temp)):
        temperatures_used = temperatures[count%len(temperatures)]
        count += 1
        print("Swap")
        print(temperatures_used)
        print(y_values)
        print(uncertainty_values)
        canvas.axes.errorbar(
            temperatures_used,
            y_values,
            yerr=uncertainty_values,
            fmt='o',  # Use the corresponding shape from shape_matrix
            color=colours[file_idx],
            label=f"ll",
            markersize=pointer_size,
            elinewidth=2,
            capsize=4,
            capthick=2
        )

    # Set axis labels and title
    canvas.axes.set_xlabel(x_title if x_title else 'Temperature [K]', labelpad=10)
    canvas.axes.set_ylabel(y_title if y_title else (row_names[pos] if pos < len(row_names) else ""))
    canvas.axes.set_title(title if title else "")

    # Apply bounds if provided
    if x_bounds:
        x_min, x_max = map(float, x_bounds.split('|'))
        canvas.axes.set_xlim(x_min, x_max)
    if y_bounds:
        y_min, y_max = map(float, y_bounds.split('|'))
        canvas.axes.set_ylim(y_min, y_max)

    # Add horizontal dashed lines for the bulk values if any
    if dashed_lines:
        for idx, value in enumerate(dashed_lines):
            canvas.axes.axhline(y=float(value), color='black', linestyle='--', linewidth=2, label=f"Bulk {idx + 1}")

    # Display grid and legend in the specified position
    canvas.axes.grid(True)
    legend_positions = {
        "TopRight": 'upper right',
        "TopLeft": 'upper left',
        "BottomRight": 'lower right',
        "BottomLeft": 'lower left'
    }
    if legend in legend_positions:
        loc = legend_positions[legend]
        bbox_anchor = (1.2, 1) if "Right" in legend else (-0.25, 1)
        canvas.axes.legend(loc=loc, bbox_to_anchor=bbox_anchor, borderaxespad=0.)
    else:
        canvas.axes.legend()
    print("Draw Canvas")
    # Adjust layout and draw the canvas
    canvas.figure.tight_layout()
    canvas.draw()