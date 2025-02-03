"""
analyze.py
Script to analyze sensor data from robots.
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Main function to load sensor values and plot them.
    """
    # back_leg_vals = np.load("data/backLegSensorValues.npy")
    # front_leg_vals = np.load("data/frontLegSensorValues.npy")
    target_angles_bl = np.load("data/sin_values_bl.npy")
    target_angles_fl = np.load("data/sin_values_fl.npy")

    plt.plot(target_angles_bl)
    plt.plot(target_angles_fl)
    # plt.plot(back_leg_vals, label="Back Leg", linewidth=3)
    # plt.plot(front_leg_vals, label="Front Leg")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
