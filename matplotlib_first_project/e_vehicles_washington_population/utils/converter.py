import csv
import sqlite3

def create_table(cursor, table_name, columns):
    columns_str = ', '.join(columns)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

def insert_data(cursor, table_name, columns, data):
    placeholders = ', '.join(['?' for _ in range(len(columns))])
    cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", data)

def csv_to_sqlite(csv_file, db_file, table_name, columns):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    create_table(cursor, table_name, columns)

    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        data = []
        i = 1
        for row in csvreader:
            row.append(i)
            data.append(row)
            i+=1

    insert_data(cursor, table_name, columns, data)

    conn.commit()
    conn.close()

# Пример использования:
csv_file = 'matplotlib/e_vehicles_washington_population/data/Electric_Vehicle_Population_Data.csv'
db_file = 'matplotlib/e_vehicles_washington_population/data/Electric_Vehicle_Population_Data.db'
table_name = 'Electric_Vehicle_Population_Data'
columns = ['VIN','County','City','State','Postal_Code','Model_Year','Make','Model','Electric_Vehicle_Type','Clean_Alternative_Fuel_Vehicle_Eligibility','Electric_Range','Base_MSRP','Legislative_District','DOL_Vehicle_ID','Vehicle_Location','Electric_Utility',"Census_tract", 'id']  # Замените на реальные названия столбцов из вашего CSV

csv_to_sqlite(csv_file, db_file, table_name, columns)