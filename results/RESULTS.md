at 50 reps, 2500 steps, 75NOG, 2POPSIZE, 2 swarm size
max mean = 1.269, avg mean = 0.495
t‑test p‑value = 0.0130

at 50 reps, 5000 steps, 75NOG, 4POPSIZE, 2 swarm size\
max mean = 1.549, avg mean = 0.940
t‑test p‑value = 0.1975

# Results

| Obstacles? | Reps | Steps | Generations | Pop Size | Swarm Size | Max Mean | Avg Mean | p-value | Significant? | File Name |
| ---------- | ---- | ----- | ----------- | -------- | ---------- | -------- | -------- | ------- | ------------ | ---- ---- |
| Yes        | 50   | 2500  | 75          | 2        | 2          | 1.269    | 0.495    | 0.0130  | Yes          | a.csv     |
| Yes        | 50   | 5000  | 75          | 4        | 2          | 1.549    | 0.940    | 0.1975  | No           | b.csv     |
| Yes        | 50   | 1000  | 10          | 2        | 2          | 0.000    | 0.000    | 0.0000  | Y/N          | c.csv     |
| No         | 50   | 2500  | 50          | 5        | 5          | 0.000    | 0.000    | 0.0000  | Y/N          | d.csv     |

## Interpretation of Results

Each experiment compares two fitness evaluation methods for the genetic algorithm:

- **Max-based selection**: uses the maximum distance traveled by any swarm member as fitness.
- **Avg-based selection**: uses the average distance traveled across the swarm.

I ran **50 replicates** for each configuration and performed an independent two-sample t-test to see if the difference in mean fitness between methods is statistically significant ($\alpha$ = 0.05).

- In the first setup (2 pop size, 2500 steps), max-based selection significantly outperformed average-based selection (p = 0.0130 < 0.05).
- In the second setup (4 pop size, 5000 steps), the difference was not statistically significant (p = 0.1975 > 0.05).

### Key Takeaways

- Under tighter budgets (smaller population or fewer steps), picking the best individual drives better performance.
- With larger populations or longer simulations, the advantage of max-based selection can disappear.
- Consider tuning population size, simulation length, or increasing replicates for more statistical power.

