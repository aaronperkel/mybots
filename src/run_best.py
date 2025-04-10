import pickle

with open('./src/data/best_solution.pkl', 'rb') as f:
    best = pickle.load(f)

best.Start_Simulation("GUI")