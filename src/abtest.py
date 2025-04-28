import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("./50r5000s75-4-4.csv")

# basic stats
max_vals = df[df.method=="max"].fitness
avg_vals = df[df.method=="avg"].fitness
t, p = stats.ttest_ind(max_vals, avg_vals)
print(f"max mean = {max_vals.mean():.3f}, avg mean = {avg_vals.mean():.3f}")
print(f"t‑test p‑value = {p:.4f}")

# box‑and‑whisker
df.boxplot(column="fitness", by="method")
plt.suptitle("")   # drop the default “Boxplot grouped by method”
plt.ylabel("Final fitness")
plt.show()