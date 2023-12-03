import csv

input_csv_path = 'top-1m raw.csv'
output_csv_path = 'top-100k.csv'

# Open the original file in read mode and the new file in write mode
with open(input_csv_path, mode='r') as infile, open(output_csv_path, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write only the first 10,000 entries from the original CSV to the new file
    for i, row in enumerate(reader):
        if i >= 100000:  # Stop after writing 10,000 rows
            break
        writer.writerow(row)

#=IF(LEFT(A1, 12)="https://www.", A1, IF(LEFT(A1, 4)="www.", "https://" & A1, "https://www." & A1))
#1000 - 203 - 3.5mins
#10000 - 484 - 8mins
#100000
