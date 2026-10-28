

import pandas as pd

df = pd.read_csv("StudentPerformanceFactors.csv")

print("Dataset shape:", df.shape)
print("\nColumn names:")
for col in df.columns:
    print(repr(col))

print("\nTarget column exists:", "Exam_Score" in df.columns)
