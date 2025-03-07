import os
import re
import polars as pl
from argparse import ArgumentParser
from typing import List

def search_for_csvs(search_path:os.PathLike) -> List[os.PathLike]:
    paths = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if os.path.splitext(file)[1] == ".csv":
                paths.append(os.path.join(root, file))
    return paths

def consolidate(csv_paths:List[os.PathLike]) -> pl.DataFrame:
    #TODO this is hacky but just make all the schemas conform please god
    consolidated = pl.read_csv(csv_paths[0])
    schema = consolidated.schema
    for path in csv_paths[1:]:
        current_dataframe = pl.read_csv(path, schema=schema)
        consolidated.extend(current_dataframe)
    return consolidated

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_directory", help="directory to search")
    parser.add_argument("-o", "--output_file", help="where to output the file")
    args = parser.parse_args()

    csv_paths = search_for_csvs(args.input_directory)
    consolidated = consolidate(csv_paths)
    consolidated.write_csv(args.output_file)