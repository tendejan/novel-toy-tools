from novel_toy_tools.implementations.rendition_statistics_cv2 import RenditionStatisticsCv2
import pandas as pd
import math

NULL_DATA_SHEET_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/null_distributions/null_master_data_sheet.csv"
EXPERIMENTAL_DATA_SHEET_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/master_data_sheet.csv"

null_dataframe = pd.read_csv(NULL_DATA_SHEET_PATH)
null_dataframe.insert(1, 'area presented', None)
null_dataframe.insert(1, 'longest edge length', None)
null_dataframe.insert(1, 'edge point 1', None)
null_dataframe.insert(1, 'edge point 2', None)

experimental_dataframe = pd.read_csv(EXPERIMENTAL_DATA_SHEET_PATH)
experimental_dataframe.insert(1, 'area presented', None)
experimental_dataframe.insert(1, 'longest edge length', None)
experimental_dataframe.insert(1, 'edge point 1', None)
experimental_dataframe.insert(1, 'edge point 2', None)

def compute_and_update(dataframe, outpath):
    dataframe.fillna('nan',inplace=True)
    for index, row in dataframe.iterrows():
        rendition_path = row['rendition']
        if not (rendition_path == 'nan'):
            rendition_obj = RenditionStatisticsCv2(rendition_path + ".png")
            stats_dict = rendition_obj.get_rendition_statistics()
            dataframe.at[index, 'area presented'] = stats_dict['area']
            dataframe.at[index, 'longest edge length'] = stats_dict['longest edge'][0]
            dataframe.at[index, 'edge point 1'] = stats_dict['longest edge'][1]
            dataframe.at[index, 'edge point 2'] = stats_dict['longest edge'][2]
        print(f'{index/dataframe.size}% done')
    dataframe.to_csv(outpath, index=False)


NULL_OUT = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/null_distributions/null_computed_datasheet.csv"
EXPERIMENTAL_OUT = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/experimental_computed_datasheet.csv"

compute_and_update(experimental_dataframe, EXPERIMENTAL_OUT)
compute_and_update(null_dataframe, NULL_OUT)