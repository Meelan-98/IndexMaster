import csv

def join_csv_files(file1, file2, output_file):
    rows = []
    with open(file1, 'r') as csvfile1, open(file2, 'r') as csvfile2:
        reader1 = csv.reader(csvfile1)
        reader2 = csv.reader(csvfile2)
        
        for row1, row2 in zip(reader1, reader2):
            joined_row = row1 + row2
            rows.append(joined_row)
    
    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerows(rows)

# Usage example
file1 = 'workloads/results/base_train_workload.csv'
file2 = 'workloads/results/reinforced_train_workload.csv'
output_file = 'workloads/results/combined_train_workload.csv'

join_csv_files(file1, file2, output_file)
