import pandas as pd

r = pd.read_csv("requirements.csv")
print(r.to_json("all.json", orient='records'))
