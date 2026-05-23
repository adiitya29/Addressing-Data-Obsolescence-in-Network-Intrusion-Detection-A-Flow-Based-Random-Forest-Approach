import pandas as pd
import glob

path = r"C:\Users\DELL\Downloads\Cybersecurity-Intrusion-Detection-main\Cybersecurity-Intrusion-Detection-main\data\MachineLearningCVE\*.csv"

files = glob.glob(path)

df_list = []

for file in files:
    print("Reading:", file)
    df = pd.read_csv(file)
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

combined_df.to_csv("combined_dataset.csv", index=False)

print("Dataset combined successfully!")