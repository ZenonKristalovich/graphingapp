import csv
import matplotlib.pyplot as plt

def graph(filename, component_names, temperatures):
    #Convert Strings to Lists
    component_names = component_names.split(',')
    temperatures = [int(item) for item in temperatures.split(',')]

    try:
        with open(filename, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            first_line = next(csv_reader)  # Read the first line

            #Gather Information of base data
            components = len(component_names)
            print("Components provided = " + str(len(component_names)) )
            
            #Skip number line
            next(csv_reader)

            #Make it a matrix
            matrix = []
            row_names = []

            for row in csv_reader:
                row_names.append(row[0])
                # Convert row elements to float and append to the matrix
                matrix.append([float(item) for item in row[1:] if item and (item.replace('.', '', 1).replace('-', '', 1).isdigit())])

            print(matrix)

            #Graph Each Diagram

            for x in range( int(len(matrix)/2) ):
                pos = 2 * x
                print("pos = " + str(pos) )
                print("tables = " + str(len(matrix)/2) )
                y_data = matrix[pos]
                uncertainty_data = matrix[pos + 1]

                # Split data for each temperature//
                y_data_by_temp = [y_data[i:i + components] for i in range(0, len(y_data), components)]
                uncertainty_by_temp = [uncertainty_data[i:i + components] for i in range(0, len(uncertainty_data), components)]
                # Plotting
                plt.figure(figsize=(8, 6))

                # Colors for the components
                colors = ['red', 'blue', 'green']
                print("test2")
                # Loop through each component (A, B, C) and plot across temperatures
                for j in range(components):
                    print("j = " + str(j))
                    print(y_data_by_temp)
                    values = [y_data_by_temp[i][j] for i in range(len(temperatures))]
                    print('values')
                    print(values)
                    uncertainty_values = [uncertainty_by_temp[i][j] for i in range(len(temperatures))]
                    print(uncertainty_values)
                    plt.errorbar(temperatures, values, yerr=uncertainty_values, fmt='o', color=colors[j], label=f'Component {component_names[j]}')

                print("test3")
                # Customize the plot
                plt.xlabel('Temperature (K)')
                plt.ylabel(row_names[pos])
                plt.title('')
                plt.legend()
                plt.grid(True)

                # Show the plot
                plt.show()

            

            return 
        
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")