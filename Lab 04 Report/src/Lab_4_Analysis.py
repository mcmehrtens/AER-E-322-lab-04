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
gage_length     = 11 * ureg.cm      # [cm]
b               = 2 * ureg.inch     # [in]
h               = 0.025 * ureg.inch # [in]
E_actual        = 73.1 * ureg.GPa   # [GPa]

###############
# IMPORT DATA #
###############

# Import calibration data
calibration_data = pd.read_excel("Lab 4 Calibration Data.xlsx", 
                                 sheet_name="Sheet1")

calibration_load = (calibration_data["load (lbf)"].to_numpy()
                    * ureg.lbf) # [lbf]
calibration_extension = (calibration_data["extension (mm)"].to_numpy()
                        * ureg.mm) # [mm]

# Import tensile test data (Instron)
tensile_test_data_instron = pd.read_csv("Lab 4 Tensile Data Instron.csv")

time = (tensile_test_data_instron["Time (s)"].to_numpy() * ureg.s) # [s]
tensile_load = (tensile_test_data_instron["Load (lbf)"].to_numpy()
                * ureg.lbf) # [lbf]
tensile_extension = (
    tensile_test_data_instron["Extension (in)"].to_numpy()
    * ureg.inch) # [in]

# Import tensile test data (Yellow Box)
tensile_test_data_yellow_box = pd.read_csv(
    "Lab 4 Tensile Data Yellow Box.csv")

tensile_strain_yb = (
    tensile_test_data_yellow_box["strain (microstrain)"].to_numpy() * 1000
    / 0.2605 / 2 * 1e-6 * ureg.dimensionless)[250:5125] # []

# Import bending test data
bending_test_data = pd.read_csv("Lab 4 Bending Data.csv")

bending_strain = (bending_test_data["epsilon (microstrain)"].to_numpy()
                  * 1e-6
                  * ureg.dimensionless) # []

# ################
# # PROCESS DATA #
# ################

# Create line of best fit for calibration data
a1,b1 = np.polyfit(calibration_load.magnitude,
                   calibration_extension.magnitude, 1)
a1 *= ureg.mm / ureg.lbf # [mm/lbf]
b1 *= ureg.mm # [mm]

# Correct the tensile test data from the instron
corrected_tensile_extension = (
    tensile_extension
    - (a1 * tensile_load + b1)).to(ureg.inch) # [in]

# Calculate strain from the tensile test data from the instron
tensile_strain_instron = (corrected_tensile_extension / gage_length).to(
    ureg.dimensionless) # []

# Calculate stress from the tensile test data from the Instron
tensile_stress = (tensile_load / (b * h)).to(ureg.psi) # [psi]

# Create line of best fit for stress-strain curve from the Instron
a2,b2 = np.polyfit(tensile_strain_instron.magnitude,
                   tensile_stress.magnitude, 1)
a2 *= ureg.psi / ureg.dimensionless # [psi/]
b2 *= ureg.psi # [psi]

# Smooth the tensile strain data from the yellow box
window = 15
smoothed_tensile_strain_yb = (
    np.convolve(tensile_strain_yb.magnitude, np.ones(window), "valid")
    / window * ureg.dimensionless) # []

# Get the time domain for the yellow box strain
time_yb = np.arange(time[0].magnitude, time[-1].magnitude,
                    (time[-1].magnitude - time[0].magnitude)
                    / len(smoothed_tensile_strain_yb)) * ureg.s # [s]

# Generate an equation for the stress
a3,b3 = np.polyfit(time.magnitude, tensile_stress.magnitude, 1)
a3 *= ureg.psi / ureg.s # [psi/s]
b3 *= ureg.psi # [psi]

# Calculate stress with respect to the yellow box strain
tensile_stress_yb = (a3 * time_yb + b3) # [psi]

# Calculate line of best fit for the yellow box stress-strain curve
a4,b4 = np.polyfit(smoothed_tensile_strain_yb.magnitude,
                   tensile_stress_yb.magnitude, 1)
a4 *= ureg.psi / ureg.dimensionless # [psi/]
b4 *= ureg.psi # [psi]

# Calculate Young's Modulus
E_instron = a2.to(ureg.GPa) # [GPa]
E_yb = a4.to(ureg.GPa) # [GPa]

################
# Print Values #
################

print("Young's Modulus (Actual)     = {:.2f}".format(E_actual))
print("Young's Modulus (Instron)    = {:.2f}".format(E_instron))
print("Young's Modulus (Yellow Box) = {:.2f}".format(E_yb))

################
# PRINT GRAPHS #
################

# Plot the calibration data
plt.figure()
plt.plot(calibration_load.magnitude, calibration_extension.magnitude,
         label="Calibration Data")
plt.plot(calibration_load.magnitude,
         (a1 * calibration_load + b1).to(ureg.mm).magnitude,
         label="Line of Best Fit")
plt.legend()
plt.grid()
plt.xlabel("Load (lbf)")
plt.ylabel("Elongation (mm)")
plt.title("Calibration Data from Instron")

# Plot the stress-strain curve from the Instron
plt.figure()
plt.plot(tensile_strain_instron.magnitude, tensile_stress.magnitude,
         label="Tensile Test Data")
plt.plot(tensile_strain_instron.magnitude,
         (a2 * tensile_strain_instron + b2).to(ureg.psi).magnitude,
         label="Line of Best Fit")
plt.legend()
plt.grid()
plt.xlabel("Strain (in/in)")
plt.ylabel("Stress (psi)")
plt.title("Stress vs Strain (Instron)")

# Plot strain vs time
plt.figure()
plt.plot(time.magnitude, tensile_strain_instron.magnitude * 1e6,
         label="Tensile Strain (Instron)")
plt.plot(time_yb.magnitude, smoothed_tensile_strain_yb.magnitude * 1e6,
         label="Tensile Strain (Yellow Box)")
plt.legend()
plt.grid()
plt.xlabel("Time (s)")
plt.ylabel("Strain (microstrain)")
plt.title("Strain vs Time")

# Plot the stress-strain curve from the yellow box
plt.figure()
plt.plot(smoothed_tensile_strain_yb.magnitude,
         tensile_stress_yb.magnitude, label="Tensile Test Data")
plt.plot(smoothed_tensile_strain_yb.magnitude,
         (a4 * smoothed_tensile_strain_yb + b4).to(ureg.psi).magnitude,
         label="Line of Best Fit")
plt.legend()
plt.grid()
plt.xlabel("Strain (in/in)")
plt.ylabel("Stress (psi)")
plt.title("Stress vs Strain (Yellow Box)")

# Plot the Young's Moduli
plt.figure()
plt.bar(["Actual", "Instron", "Yellow Box"],
        [E_actual.magnitude, E_instron.magnitude, E_yb.magnitude])
plt.xlabel("Young's Modulus")
plt.ylabel("GPa")
plt.title("Young's Modulus Comparison")
plt.show()