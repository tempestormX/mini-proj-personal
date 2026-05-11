#Want to read csv file from mini-proj-personal/csv/PublicTransportUtilisation.csv
import csv

def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data
if __name__ == "__main__":
    file_path = 'csv/PublicTransportUtilisationAveragePublicTransportRidership.csv'
    csv_data = read_csv_file(file_path)
    for row in csv_data:
        print(row)