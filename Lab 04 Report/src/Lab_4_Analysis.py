# AER E 322 Spring 2023 Lab 4
# Section 4 Group 2
# Matthew Mehrtens
# Peter Mikolitis
# Natsuki Oda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pint import UnitRegistry

# Declare unit registry
ureg = UnitRegistry()

# Define constants
gage_length = 11 * ureg.cm # [cm]
b = 2 * ureg.inch # [in]
h = 0.025 * ureg.inch # [in]

#
# IMPORT DATA
#

# Import calibration data
calibration_data = pd.read_excel("Lab 4 Calibration Data.xlsx", 
                                 sheet_name="Sheet1")

calibration_load = calibration_data["load (lbf)"].to_numpy() * ureg.lbf # [lbf]
calibration_extension = (calibration_data["extension (mm)"].to_numpy()
                        * ureg.mm) # [mm]

# Import tensile test data
tensile_test_data_instron = pd.read_csv("Lab 4 Tensile Data Instron.csv")
tensile_test_data_yellow_box = pd.read_csv("Lab 4 Tensile Data Yellow Box.csv")

time = (tensile_test_data_instron["Time (s)"].to_numpy() * ureg.s) # [s]
tensile_load = (tensile_test_data_instron["Load (lbf)"].to_numpy()
                * ureg.lbf) # [lbf]
tensile_extension = (tensile_test_data_instron["Extension (in)"].to_numpy()
                     * ureg.inch) # [in]

tensile_strain_yb = (
    tensile_test_data_yellow_box["strain (microstrain)"].to_numpy() * 10e-6
    * ureg.dimensionless) # []

# Import bending test data
bending_test_data = pd.read_csv("Lab 4 Bending Data.csv")

bending_strain = (bending_test_data["epsilon (microstrain)"].to_numpy() * 10e-6
                * ureg.dimensionless) # []

#
# PROCESS DATA
#

# Scale the tensile test data from the yellow box
tensile_strain_yb = (tensile_strain_yb * 1000 / 0.2605 / 2) # []

# Create line of best fit for calibration data
a1,b1 = np.polyfit(calibration_load.magnitude, calibration_extension.magnitude,
                   1)
a1 *= ureg.mm / ureg.lbf # [mm/lbf]
b1 *= ureg.mm # [mm]

# Correct the tensile test data from the instron
corrected_tensile_extension = (tensile_extension -
                               (a1 * tensile_load + b1)) # [in]

# Calculate strain from the tensile test data from the instron
tensile_strain_instron = (corrected_tensile_extension / gage_length).to(
    ureg.dimensionless) # []

# Calculate stress from the tensile test data from the instron
tensile_stress = (tensile_load / (b * h)).to(ureg.psi) # [psi]

# Create line of best fit for stress-strain curve from the instron
a2,b2 = np.polyfit(tensile_strain_instron.magnitude,tensile_stress.magnitude,1)
a2 *= ureg.psi / ureg.dimensionless # [psi/]
b2 *= ureg.psi # [psi]

#
# PRINT GRAPHS
#

# Plot the calibration data
plt.figure()
plt.plot(calibration_load, calibration_extension, label="Calibration Data")
plt.plot(calibration_load, a1 * calibration_load + b1,
         label="Line of Best Fit")
plt.legend()
plt.grid()
plt.xlabel("Load (lbf)")
plt.ylabel("Elongation (mm)")
plt.title("Calibration Data from Instron")

# Plot the tensile test data from the instron
plt.figure()
plt.plot(tensile_strain_instron, tensile_stress, label="Tensile Test Data")
plt.plot(tensile_strain_instron, a2 * tensile_strain_instron + b2,
         label="Line of Best Fit")
plt.legend()
plt.grid()
plt.xlabel("Strain (in/in)")
plt.ylabel("Stress (psi)")
plt.title("Stress vs Strain (Instron)")

# Plot strain vs time
plt.figure()
plt.plot(time, tensile_strain_instron, label="Tensile Strain (Instron)")
plt.legend()
plt.grid()
plt.xlabel("Time (s)")
plt.ylabel("Strain (in/in)")
plt.title("Strain vs Time")
plt.show()