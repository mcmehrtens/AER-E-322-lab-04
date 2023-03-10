# AER E 322 Spring 2023 Lab 4
# Section 4 Group 2
# Matthew Mehrtens
# Peter Mikolitis
# Natsuki Oda
import pandas as pd
import matplotlib.pyplot as plt

# Import calibration data
calibration_data = pd.read_excel("Lab 4 Calibration Data.xlsx", sheet_name="Sheet1")

# Import tensile test data
tensile_test_data_instron = pd.read_csv("Lab 4 Tensile Data Instron.csv")
tensile_test_data_yellow_box = pd.read_csv("Lab 4 Tensile Data Yellow Box.csv")

# Import bending test data
bending_test_data = pd.read_csv("Lab 4 Bending Data.csv")