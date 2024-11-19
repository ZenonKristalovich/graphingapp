import csv
import os


def read_csv(filename):
    print("Current working directory:", os.getcwd())
    matrix = []
    row_names = []
    try:
        with open(filename, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            temperatures = get_temps(next(csv_reader))  
            components = int(max(next(csv_reader)))
            for row in csv_reader:
                row_names.append(row[0])
                matrix.append([float(item) for item in row[1:] if item.replace('.', '', 1).replace('-', '', 1).isdigit()])
        return matrix, row_names, temperatures,components
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return [], [], [], 0

def read_multi_csv(filenames):
    matrix = []
    row_names = []
    temperatures = [] # Using a set to keep unique temperatures
    components = 0

    # Split the filenames string by commas to get individual file paths
    file_list = filenames

    try:
        for file_idx, file_name in enumerate(file_list):
            with open(file_name.strip(), mode='r', newline='') as file:
                csv_reader = csv.reader(file)

                # Read temperatures from the first line of each file
                new_temperatures = get_temps(next(csv_reader))
                temperatures.append(new_temperatures)  # Add new temperatures to the set

                # Read the number of components from the second line
                components = max(components,int(max(next(csv_reader))))

                for row_idx, row in enumerate(csv_reader):
                    if file_idx == 0:
                        # For the first file, initialize rows in the matrix and store row names
                        row_names.append(row[0])
                        matrix.append([[] for _ in range(components)])

                    # Fill in the matrix with component values
                    for component_index in range(components):
                        component_values = [
                            float(row[1 + j * components + component_index])
                            for j in range(len(row[1:]) // components)
                        ]
                        matrix[row_idx][component_index].extend(component_values)

        # Convert temperatures set back to a sorted list

        return matrix, row_names, temperatures, components

    except FileNotFoundError:
        print(f"Error: One of the files {filenames} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return [], [], [], 0


def get_temps(line):
    temps = []
    for temp in line:
        if temp == "":
            continue
        if temp == "RT":
            temps.append(300)
        else:
            temps.append(int(temp[:-1]))
    return temps