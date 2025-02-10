import pandas as pd
import matplotlib.pyplot as plt
import os as os
from pathlib import Path
import logging

def main():
    file_path = 'small_dataset.csv'
    data = load_data(file_path)
    if data is not None:
        data = clean_data(data)
        analyze_data(data)
        plot_data(data)
        
# Load dataset
def load_data(file_path: str):
    path = Path(file_path)
   
    if not path.exists():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"The file {file_path} was not found.")
    
    try:
        data = pd.read_csv(path)
        logging.info("Data loaded successfully.")
        return data
    
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return None
    

# Cleaning The Dataset

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    duplicate_count = data.duplicated().sum()
    logging.info(f"Duplicate rows found: {duplicate_count}")
    data = data.drop_duplicates()

    missing_before = data.isnull().sum().sum()
    logging.info(f"Total missing values before cleaning: {missing_before}")
    data = data.dropna()
    
    missing_after = data.isnull().sum().sum()
    logging.info(f"Total missing values after cleaning: {missing_after}")
    
    if 'brokered_by' in data.columns:
        data = data.drop(columns=['brokered_by'])

    numeric_columns = ['price', 'bed', 'bath', 'acre_lot', 'house_size']
    
    for col in numeric_columns:
        if col in data.columns:
            try:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                logging.info(f'Converted {col} to numeric')
            except Exception as e:
                logging.error(f"Error converting {col}: {e}")

    # Converting zip code and street to string
    if 'street' in data.columns:
        data['street'] = data['street'].astype(str)
        logging.info("Converted street to string")
        
    if 'zip_code' in data.columns:
        data['zip_code'] = data['zip_code'].astype(str)
        logging.info("Converted zip code to string")

    # Rounding numerical columns
    if 'price' in data.columns:
        data['price'] = data['price'].round(2)
        
    if 'bed' in data.columns:
        data['bed'] = data['bed'].round(0).astype(int)
        
    if 'bath' in data.columns:
        data['bath'] = data['bath'].round(0).astype(int)
        
    if 'acre_lot' in data.columns:
        data['acre_lot'] = data['acre_lot'].round(2)
        
    if 'house_size' in data.columns:
        data['house_size'] = data['house_size'].round(0).astype(int)
    
    return data

def analyze_data(data: pd.DataFrame) -> None:
    
    # Logging Dataset info 
    logging.info("Dataset Information:")
    data.info()

    # Summary statistics
    print("\nSummary statistics after cleaning:")
    print(data.describe())

# Selecting numeric columns for analysis
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    numeric_columns = [col for col in numeric_columns if col not in ['street', 'zip_code']]
    print("\nNumeric columns:", numeric_columns)

# Summary statistics for each numeric column
    for column in numeric_columns:
        print(f"\nSummary for {column}:")
        print(f"Min: {data[column].min()}")
        print(f"Max: {data[column].max()}")
        print(f"Mean: {data[column].mean():.2f}")
        print(f"Median: {data[column].median()}")
        print(f"Variance: {data[column].var():.2f}")
        print(f"Standard Deviation: {data[column].std():.2f}")


def plot_data(data: pd.DataFrame) -> None:
# Grouping and analyzing price in regards to city
    price_by_city = data.groupby('city')['price'].describe()
    print("\nSummary Statistics for Price by City:")
    print(price_by_city)

    pivot_table = data.pivot_table(values='price', index='city', aggfunc=['count', 'mean', 'median', 'var', 'std'])
    print("\nPivot Table Summary for Prices by City:")
    print(pivot_table)

    # Top 50 cities by average price
    top_cities = data.groupby('city')['price'].mean().sort_values(ascending=False).head(50)

    # Data plot
    plt.figure(figsize=(12, 6))
    top_cities.plot(kind='bar', color='skyblue')
    plt.title('Top 50 Cities by Average Property Price')
    plt.xlabel('City')
    plt.ylabel('Average Price (In Millions)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Grouping and analyzing price by number of bedrooms
    if 'bed' in data.columns:
        price_by_bed = data.groupby('bed')['price'].describe()
        print("\nSummary Statistics for Price by Bedroom:")
        print(price_by_bed)

        pivot_bedroom_price = data.pivot_table(values='price', index='bed', aggfunc=['count', 'mean', 'median', 'var', 'std'])
        print("\nPivot Table Summary for Price by Bedroom:")
        print(pivot_bedroom_price)

    # Plotting average price by number of bedrooms
    plt.figure(figsize=(10, 6))
    average_price_by_bed = data.groupby('bed')['price'].mean()
    average_price_by_bed.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Average Property Price by Number of Bedrooms')
    plt.xlabel('Number of Bedrooms')
    plt.ylabel('Average Price (In Dollars)')
    plt.xticks(rotation=0)
    plt.show()

if __name__ == '__main__':
    main()
