import polars as pl
from scipy.spatial.transform import Rotation
import numpy as np
import os
import seaborn as sns
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt


class CoderData:
    def __init__(self, coder_name, csv_path):
        self.coder_name = coder_name
        self.csv_path = csv_path
        self.subject = None
        self.read_csv(csv_path, coder_name)

    def __len__(self):
        return len(self.frames.keys())
    
    def __iter__(self):
        return self.frames.__iter__()

    def read_csv(self, path, coder_name) -> dict:
        data_dict = {}
        dataframe = pl.read_csv(path)
        for row in dataframe.iter_rows():
            self.subject = row[1]
            raw_filename = row[12]
            if raw_filename in data_dict.keys():
                raise KeyError(f"key {raw_filename} already exists in dictionary")
            code_value = int(row[6])
            rotation = None
            if code_value == 1:
                rotation = Rotation.from_euler("YZX", (row[8], row[9], row[7]), degrees=True)
            data_dict[raw_filename] = {"code": code_value, "rotation": rotation, "coder name": coder_name}
        self.frames = data_dict

def get_shared_frames(data1:CoderData, data2:CoderData):
    smaller:CoderData
    larger:CoderData
    shared = {}
    if len(data1) < len(data2):
        smaller = data1
        larger = data2
    else:
        smaller = data2
        larger = data1

    for frame in smaller.frames:
        if frame in larger.frames:
            shared[frame] = (smaller.frames[frame], larger.frames[frame])
    return shared

def compute_angular_diff(r1:Rotation, r2:Rotation):
    quat1 = r1.as_quat()
    quat2 = r2.as_quat()
    dot_product = np.dot(quat1, quat2)
    #TODO error check that this does nothing
    dot_product = np.clip(dot_product, -1, 1)
    angle = 2*np.arccos(np.abs(dot_product))
    return np.degrees(angle)


CODER1_CSV = os.path.normpath(r"/Volumes/Active/Viewer3D_codingApp/ObjectOutput CHC/NewStructure/26100/Raw Data 3D/Exp 2A/26100_3DVD_AJ_2:06:2025.csv")
CODER1_NAME = "Alden"

CODER2_CSV = os.path.normpath(r"/Volumes/Active/Viewer3D_codingApp/ObjectOutput CHC/NewStructure/26100/Raw Data 3D/Exp 2A/26100_3DVD_SH_02:06:2025.csv")
CODER2_NAME = "Shinta"

OUT_DIR = os.path.normpath(r"/Volumes/Active/Viewer3D_codingApp/Reliability 3D Viewer Data")

def main(coder1_name, coder1_csv, coder2_name, coder2_csv, outdir):
    coder1_data = CoderData(CODER1_NAME, CODER1_CSV)
    coder2_data = CoderData(CODER2_NAME, CODER2_CSV)

    shared = get_shared_frames(coder1_data, coder2_data)

    coder1_predictions = []
    coder2_predictions = []
    lookup = {
        -1: 0, #object absent
        -2: 1, #object not codable
        1: 2, #object in view
    }

    labels = [f"Object Absent (-1)", 
          f"Object Not Codable (-2)", 
          f"Object in View (1)"]

    angular_diffs = []

    for frame in shared:
        tup = shared[frame]
        if tup[0]['code'] == 1 and tup[1]['code'] == 1:
            diff = compute_angular_diff(tup[0]['rotation'], tup[1]['rotation'])
            angular_diffs.append(diff)
        coder1_predictions.append(tup[0]['code'])
        coder2_predictions.append(tup[1]['code'])

    confusion = confusion_matrix(coder1_predictions, coder2_predictions)

    fig, ax = plt.subplots(2, 1)
    sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues', ax=ax[0], xticklabels=["(-1)", "(-2)", "(1)"], yticklabels=labels)
    ax[0].set_xlabel(f"{coder1_name}'s claims")
    ax[0].set_ylabel(f"{coder2_name}'s claims")
    ax[0].xaxis.tick_top()
    ax[0].xaxis.set_label_position('top')

    bins = np.arange(0, 181, 1)
    ax[1].hist(angular_diffs, bins=bins, edgecolor="blue")
    ax[1].set_xlabel('Angular Difference (degrees)')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Distribution of Angular Differences')

    print(len(angular_diffs))
    fig.tight_layout()
    
    filename = f"Reliability_{coder1_data.subject}_{coder1_name}_{coder2_name}.png"
    file_path = os.path.join(outdir, filename)
    fig.savefig(file_path)

if __name__ == "__main__":
    main(CODER1_NAME, CODER1_CSV, CODER2_NAME, CODER2_CSV, OUT_DIR)