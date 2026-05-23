import pandas as pd

df = pd.DataFrame(columns=["time", "status"])
df["bucket"] = df["time"]
bs = df.groupby("bucket")["status"].apply(len).reset_index()
print("Cols before:", bs.columns)
try:
    bs.columns = ["Time", "Attack %"]
    print("Success")
except Exception as e:
    print("Error:", e)
