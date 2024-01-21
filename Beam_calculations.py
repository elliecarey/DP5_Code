import matplotlib.pyplot as plt
import numpy as np 

uniform_load = 100000 # N/m
length = 5 # m
YM = 200e9 # Pa (Young's Modulus)
SMoA = 1e-4 # m^4 (Second Moment of Area)
y = 0.1 # m (Distance from the neutral axis to the outermost fiber)
material_yield_strength = 250e6 # Pa (example yield strength for steel)


# Second Moment of Area of I-Beam cross section
def Ibeam_second_moment_of_area(height, base, thickness):
    SMoA_Ibeam = ((1/6)*(height**3)*thickness) * (1 + 3*(base/height))
    return SMoA_Ibeam

# Second Moment of Area of hollow square cross section
def HSS_second_moment_of_area(height, base, thickness):
    SMoA_HSS = ((1/6)*(height**3)*thickness) * (1 + 3*(base/height))
    return SMoA_HSS



def beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength):
    # Determine the maximum deflection of the beam
    def calculate_max_deflection(uniform_load, length, YM, SMoA):
        delta_max = (uniform_load * length**4) / (384 * YM * SMoA)
        return delta_max

    # print("The maximum deflection of the beam is", calculate_max_deflection(uniform_load, length, YM, SMoA), "m")

    # Determine the maximum bending moment of the beam
    def calculate_max_bending_moment(uniform_load, length):
        M_max = (uniform_load * length**2) / 12
        return M_max

    # Determine the maximum shear stress of the beam
    def calculate_max_shear_stress(M_max, y, SMoA): 
        tau_max = (M_max * y) / (SMoA)
        return tau_max

    M_max = calculate_max_bending_moment(uniform_load, length)
    tau_max = calculate_max_shear_stress(M_max, y, SMoA)

    # if tau_max > material_yield_strength:
    #     # print("The beam will fail by ductile failure.")
    #     return True
    # else:
    #     # print("The beam will not fail by ductile failure.")
    #     return False
        
    deflection = calculate_max_deflection(uniform_load, length, YM, SMoA)
    
    ductile_failure = tau_max > material_yield_strength
    
    return deflection, tau_max, ductile_failure

# Call the function with the given parameters
beam_analysis(1000, 5, 200e9, 1e-4, 0.1, 250e6)

lengths = [4, 5, 6, 7, 8]  # example lengths
y_values = [0.08, 0.1, 0.12, 0.14, 0.16]  # example y values

max_length = None
max_y = None

for length, y in zip(lengths, y_values):
    _, _, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength)
    if not ductile_failure:
        max_length = length
        max_y = y

print("The maximum length before ductile failure is", max_length, "m")
print("The maximum y value before ductile failure is", max_y, "m")

shear_stresses = []

for length, y in zip(lengths, y_values):
    _, shear_stress, _ = beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength)
    shear_stresses.append(shear_stress)

plt.plot(lengths, shear_stresses, label='Shear Stress')
plt.axhline(y=material_yield_strength, color='r', linestyle='--', label='Yield Strength')
plt.xlabel('Beam Length (m)')
plt.ylabel('Shear Stress (MPa)')
plt.title('Beam Length vs Shear Stress')
plt.legend()
plt.show()
