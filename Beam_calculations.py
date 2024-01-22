import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

uniform_load = 100000 # N/m
# length = 5 # m
YM = 200e9 # Pa (Young's Modulus)
SMoA = 1e-4 # m^4 (Second Moment of Area)
# y = 0.1 # m (Distance from the neutral axis to the outermost fiber)
material_yield_strength = 250e6 # Pa (example yield strength for steel)

# Read the spreadsheet data
df = pd.read_excel('Beam_specifications.xlsx')  # replace with your spreadsheet file path

df['height'] = pd.to_numeric(df['height']) / 1000
df['base'] = pd.to_numeric(df['base']) / 1000 
df['thickness'] = pd.to_numeric(df['thickness']) / 1000

# Second Moment of Area of I-Beam cross section
def Ibeam_second_moment_of_area(height, base, thickness):
    SMoA_Ibeam = ((1/6)*(height**3)*thickness) * (1 + 3*(base/height))
    return SMoA_Ibeam

# Calculate the base/2 values
df['half_base'] = df['base'] / 2000
# Calculate the second moment of area for each beam
df['SMoA_Ibeam'] = df.apply(lambda row: Ibeam_second_moment_of_area(row['height'], row['base'], row['thickness']), axis=1)
# Append the values to a list
SMoA_Ibeam_list = df['SMoA_Ibeam'].tolist()
half_bases = df['half_base'].tolist()

# # Second Moment of Area of hollow square cross section
# def HSS_second_moment_of_area(height, base, thickness):
#     SMoA_HSS = ((1/6)*(height**3)*thickness) * (1 + 3*(base/height))
#     return SMoA_HSS

# # Second Moment of Area of Tee-bar cross section
# def Teebar_second_moment_of_area(height, base, thickness):
#     SMoA_Teebar = ((1/6)*thickness) * ((height**3) + 4*(base*(thickness**2)))
#     return SMoA_Teebar

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

# lengths = [4, 5, 6, 7, 8]  # example lengths
# y_values = [0.08, 0.1, 0.12, 0.14, 0.16]  # example y values

# max_length = None
# max_y = None

# for length, y in zip(lengths, y_values):
#     _, _, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength)
#     if not ductile_failure:
#         max_length = length
#         max_y = y

# print("The maximum length before ductile failure is", max_length, "m")
# print("The maximum y value before ductile failure is", max_y, "m")

# shear_stresses = []

# for length, y in zip(lengths, y_values):
#     _, shear_stress, _ = beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength)
#     shear_stresses.append(shear_stress)

# plt.plot(lengths, shear_stresses, label='Shear Stress')
# plt.axhline(y=material_yield_strength, color='r', linestyle='--', label='Yield Strength')
# plt.xlabel('Beam Length (m)')
# plt.ylabel('Shear Stress (MPa)')
# plt.title('Beam Length vs Shear Stress')
# plt.legend()
# plt.show()

# length = 4

# max_length = None
# max_y = None
# shear_stresses = []

# for SMoA, y in zip(SMoA_Ibeam_list, half_bases):
#     _, shear_stress, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, y, material_yield_strength)
#     shear_stresses.append(shear_stress)
#     if not ductile_failure:
#         max_length = length
#         max_y = y

# print("The maximum length before ductile failure is", max_length, "m")
# print("The maximum y value before ductile failure is", max_y, "m")

# plt.plot(lengths, shear_stresses, label='Shear Stress')
# plt.axhline(y=material_yield_strength, color='r', linestyle='--', label='Yield Strength')
# plt.xlabel('Beam Length (m)')
# plt.ylabel('Shear Stress (MPa)')
# plt.title('Beam Length vs Shear Stress')
# plt.legend()

# max_height = None
# max_base = None
# max_thickness = None
# heights = []
# shear_stresses = []

# for _, row in df.iterrows():
#     height = row['height']
#     base = row['base']
#     thickness = row['thickness']
#     SMoA = Ibeam_second_moment_of_area(height, base, thickness)
#     _, shear_stress, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, height/2, material_yield_strength)
#     shear_stresses.append(shear_stress)
#     heights.append(height)
#     if not ductile_failure and (max_height is None or height > max_height):
#         max_height = height
#         max_base = base
#         max_thickness = thickness

# print(f"The maximum height before ductile failure is {max_height} m")
# print(f"The associated base is {max_base} m")
# print(f"The associated thickness is {max_thickness} m")

# plt.plot(heights, shear_stresses, label='Shear Stress')
# plt.axhline(y=material_yield_strength, color='r', linestyle='-', label='Yield Strength')
# plt.xlabel('Height (m)')
# plt.ylabel('Shear Stress (Pa)')
# plt.legend()
# plt.show()

max_length = None
max_height = None
max_base = None
max_thickness = None
max_serial_size = None
selected_lengths = []
selected_shear_stresses = []

for _, row in df.iterrows():
    height = row['height']
    base = row['base']
    thickness = row['thickness']
    serial_size = row['Serial size']
    SMoA = Ibeam_second_moment_of_area(height, base, thickness)
    lengths = []
    shear_stresses = []
    for length in np.arange(1, 10, 0.1):  # replace with your range of lengths
        _, shear_stress, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, height/2, material_yield_strength)
        lengths.append(length)
        shear_stresses.append(shear_stress)
        if not ductile_failure and (max_length is None or length > max_length):
            max_length = length
            max_height = height
            max_base = base
            max_thickness = thickness
            max_serial_size = serial_size
            selected_lengths = lengths
            selected_shear_stresses = shear_stresses

print(f"The optimum length before ductile failure is {max_length} m")
print(f"The optimum height is {max_height} m")
print(f"The optimum base is {max_base} m")
print(f"The optimum thickness is {max_thickness} m")
print(f"The selected serial size is {max_serial_size}")

plt.plot(selected_lengths, selected_shear_stresses, label='Shear Stress of Selected Beam')
plt.axhline(y=material_yield_strength, color='r', linestyle='-', label='Yield Strength')
plt.xlabel('Beam Length (m)')
plt.ylabel('Shear Stress (Pa)')
plt.title('Beam Length vs Shear Stress')
plt.legend()
plt.show()
