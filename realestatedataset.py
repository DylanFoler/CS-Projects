import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator

# Configuring Module-Based Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
def main() -> None:
    file_path: str = 'small_dataset.csv'
    
    try:
        data = load_data(file_path)
    except FileNotFoundError as e:
        logger.error(e)
        return

    data = clean_data(data)
    analyze_data(data)
    plot_data(data)
   
    """
    Main function that orchestrates data loading, cleaning, analysis, and plotting.
    """

def load_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"The file {file_path} was not found.")
    try:
        data = pd.read_csv(path)
        logger.info("Data loaded successfully.")
        return data
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        raise
    
    """
        Load the dataset from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded data as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If there is an error reading the CSV.
    """
    
def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    # Removing Duplicate Rows
    duplicate_count = data.duplicated().sum()
    logger.info(f"Duplicate rows found: {duplicate_count}")
    data = data.drop_duplicates()

    # Removing Rows With Missing Values
    missing_before = data.isnull().sum().sum()
    logger.info(f"Total missing values before cleaning: {missing_before}")
    data = data.dropna()
    missing_after = data.isnull().sum().sum()
    logger.info(f"Total missing values after cleaning: {missing_after}")

    # Dropping Unwanted Columns If They Exist
    if 'brokered_by' in data.columns:
        data = data.drop(columns=['brokered_by'])
        logger.info("Dropped 'brokered_by' column.")

    # Converting Specified Columns To Numeric If They Exist
    numeric_columns = ['price', 'bed', 'bath', 'acre_lot', 'house_size']
    for col in numeric_columns:
        if col in data.columns:
            try:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                logger.info(f"Converted '{col}' to numeric.")
            except Exception as e:
                logger.error(f"Error converting '{col}': {e}")

    # Converting Specific Columns To String
    if 'street' in data.columns:
        data['street'] = data['street'].astype(str)
        logger.info("Converted 'street' to string.")
    if 'zip_code' in data.columns:
        data['zip_code'] = data['zip_code'].astype(str)
        logger.info("Converted 'zip_code' to string.")

    # Rounding Numeric Columns Appropriately
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

    """
    Clean the dataset by removing duplicates, handling missing values,
    converting data types, and rounding numeric columns.

    Args:
        data (pd.DataFrame): Raw dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    
def analyze_data(data: pd.DataFrame) -> None:
   
    logger.info("Dataset Information:")
    data.info()

    """
    Generate bar plots for the top 50 cities by average property price and
    average property price by bedroom count, with enhanced y-axis formatting.

    Args:
        data (pd.DataFrame): The dataset to plot.
    """
    
def plot_data(data: pd.DataFrame) -> None:
    
    # Formatter For Dollar Values On The Y-Axis
    dollar_formatter = FuncFormatter(lambda x, pos: '${:,.0f}'.format(x))

    # Plotting Top 50 Cities By Average Property Price
    top_cities = data.groupby('city')['price'].mean().sort_values(ascending=False).head(50)
    plt.figure(figsize=(12, 6))
    top_cities.plot(kind='bar', color='skyblue')
    plt.title('Top 50 Cities By Average Property Price')
    plt.xlabel('City')
    plt.ylabel('Average Price (Dollars)')
    plt.xticks(rotation=45, ha='right')

    ax = plt.gca()
    ax.yaxis.set_major_formatter(dollar_formatter)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Plot: Average Property Price By Number Of Bedrooms
    if 'bed' in data.columns:
        average_price_by_bed = data.groupby('bed')['price'].mean()
        plt.figure(figsize=(10, 6))
        average_price_by_bed.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Average Property Price by Number of Bedrooms')
        plt.xlabel('Number of Bedrooms')
        plt.ylabel('Average Price (Dollars)')
        plt.xticks(rotation=0)

        ax = plt.gca()
        ax.yaxis.set_major_formatter(dollar_formatter)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        
        """
        Generate bar plots for the top 50 cities by average property price and
        average property price by bedroom count, with enhanced y-axis formatting.

        Args:
        data (pd.DataFrame): The dataset to plot.
        """
        
if __name__ == '__main__':
    main()
