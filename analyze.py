"""
analyze.py
Script to analyze sensor data from robots.
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    backLegSensorValues = np.load('data/backLegSensorValues.npy')
    plt.plot(backLegSensorValues)
    plt.show()

if __name__ == '__main__':
    main()
