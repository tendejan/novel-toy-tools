from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # For a visual progress bar (install via `pip install tqdm`)
import pandas as pd
from novel_toy_tools.implementations.rendition_statistics_cv2 import RenditionStatisticsCv2

NULL_DATA_SHEET_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/null_distributions/null_master_data_sheet.csv"
EXPERIMENTAL_DATA_SHEET_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/master_data_sheet.csv"
NULL_OUT = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/null_distributions/null_computed_datasheet.csv"
EXPERIMENTAL_OUT = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/experimental_computed_datasheet.csv"

# Read and prepare dataframes
def prepare_dataframe(file_path):
    dataframe = pd.read_csv(file_path)
    dataframe.insert(1, 'area presented', None)
    dataframe.insert(1, 'longest edge length', None)
    dataframe.insert(1, 'edge point 1', None)
    dataframe.insert(1, 'edge point 2', None)
    dataframe.fillna('nan', inplace=True)
    return dataframe

null_dataframe = prepare_dataframe(NULL_DATA_SHEET_PATH)
experimental_dataframe = prepare_dataframe(EXPERIMENTAL_DATA_SHEET_PATH)

# Function to compute statistics for a single row
def compute_row_statistics(row):
    if row['rendition'] == 'nan':
        return None
    rendition_path = row['rendition']
    rendition_obj = RenditionStatisticsCv2(rendition_path + ".png")
    stats_dict = rendition_obj.get_rendition_statistics()
    return {
        'index': row.name,
        'area': stats_dict['area'],
        'longest_edge_length': stats_dict['longest edge'][0],
        'edge_point_1': stats_dict['longest edge'][1],
        'edge_point_2': stats_dict['longest edge'][2],
    }

# Parallel computation and update of the dataframe with progress monitoring
def compute_and_update_parallel(dataframe, outpath):
    # Initialize progress bar
    total_rows = len(dataframe)
    progress_bar = tqdm(total=total_rows, desc="Processing Rows", unit="row")
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(compute_row_statistics, row): index for index, row in dataframe.iterrows()}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                dataframe.at[result['index'], 'area presented'] = result['area']
                dataframe.at[result['index'], 'longest edge length'] = result['longest_edge_length']
                dataframe.at[result['index'], 'edge point 1'] = result['edge_point_1']
                dataframe.at[result['index'], 'edge point 2'] = result['edge_point_2']
            progress_bar.update(1)
    
    progress_bar.close()
    dataframe.to_csv(outpath, index=False)

# Process the dataframes in parallel with progress monitoring
compute_and_update_parallel(experimental_dataframe, EXPERIMENTAL_OUT)
compute_and_update_parallel(null_dataframe, NULL_OUT)
