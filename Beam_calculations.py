import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

uniform_load = 100000 # N/m
# length = 5 # m
YM = 200e9 # Pa (Young's Modulus) of Steel 
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

# Second Moment of Area of hollow square cross section
def HSS_second_moment_of_area(height, base, thickness):
    SMoA_HSS = ((1/6)*(height**3)*thickness) * (1 + 3*(base/height))
    return SMoA_HSS

# Second Moment of Area of Tee-bar cross section
def Teebar_second_moment_of_area(height, base, thickness):
    SMoA_Teebar = ((1/6)*thickness) * ((height**3) + 4*(base*(thickness**2)))
    return SMoA_Teebar


def get_second_moment_of_area_function(beam_type):
    if beam_type == 'I-beam':
        return Ibeam_second_moment_of_area
    elif beam_type == 'HSS':
        return HSS_second_moment_of_area
    elif beam_type == 'Tee-bar':
        return Teebar_second_moment_of_area
    else:
        raise ValueError(f"Unknown beam type: {beam_type}")

# # Calculate the base/2 values
# df['half_base'] = df['base'] / 2000
# # Calculate the second moment of area for each beam
# df['SMoA_Ibeam'] = df.apply(lambda row: Ibeam_second_moment_of_area(row['height'], row['base'], row['thickness']), axis=1)
# # Append the values to a list
# SMoA_Ibeam_list = df['SMoA_Ibeam'].tolist()
# half_bases = df['half_base'].tolist()

def process_beam_data(df, beam_type):
    df['height'] = pd.to_numeric(df['height']) / 1000
    df['base'] = pd.to_numeric(df['base']) / 1000 
    df['thickness'] = pd.to_numeric(df['thickness']) / 1000
    df['half_base'] = df['base'] / 2000

    second_moment_of_area_function = get_second_moment_of_area_function(beam_type)
    df['SMoA'] = df.apply(lambda row: second_moment_of_area_function(row['height'], row['base'], row['thickness']), axis=1)

    return df

df_Ibeam = pd.read_excel('Beam_specifications.xlsx', sheet_name='I-beam')  # replace with your spreadsheet file path
df_HSS = pd.read_excel('Beam_specifications.xlsx', sheet_name='HSS')  # replace with your spreadsheet file path
df_Teebar = pd.read_excel('Beam_specifications.xlsx', sheet_name='Tee-bar')  # replace with your spreadsheet file path

df_Ibeam = process_beam_data(df_Ibeam, 'I-beam')
df_HSS = process_beam_data(df_HSS, 'HSS')
df_Teebar = process_beam_data(df_Teebar, 'Tee-bar')

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

    deflection = calculate_max_deflection(uniform_load, length, YM, SMoA)
    
    ductile_failure = tau_max > material_yield_strength
    
    return deflection, tau_max, ductile_failure

# Call the function with the given parameters
# beam_analysis(1000, 5, 200e9, 1e-4, 0.1, 250e6)

# max_length = None
# max_height = None
# max_base = None
# max_thickness = None
# max_serial_size = None
# selected_lengths = []
# selected_shear_stresses = []

# for _, row in df.iterrows():
#     height = row['height']
#     base = row['base']
#     thickness = row['thickness']
#     serial_size = row['Serial size']
#     SMoA = Ibeam_second_moment_of_area(height, base, thickness)
#     lengths = []
#     shear_stresses = []
#     for length in np.arange(1, 10, 0.1):  # replace with your range of lengths
#         _, shear_stress, ductile_failure = beam_analysis(uniform_load, length, YM, SMoA, height/2, material_yield_strength)
#         lengths.append(length)
#         shear_stresses.append(shear_stress)
#         if not ductile_failure and (max_length is None or length > max_length):
#             max_length = length
#             max_height = height
#             max_base = base
#             max_thickness = thickness
#             max_serial_size = serial_size
#             selected_lengths = lengths
#             selected_shear_stresses = shear_stresses

# print(f"The optimum length before ductile failure is {max_length} m")
# print(f"The optimum height is {max_height} m")
# print(f"The optimum base is {max_base} m")
# print(f"The optimum thickness is {max_thickness} m")
# print(f"The selected serial size is {max_serial_size}")

# plt.plot(selected_lengths, selected_shear_stresses, label='Shear Stress of Selected Beam')
# plt.axhline(y=material_yield_strength, color='r', linestyle='-', label='Yield Strength')
# plt.xlabel('Beam Length (m)')
# plt.ylabel('Shear Stress (Pa)')
# plt.title('Beam Length vs Shear Stress')
# plt.legend()
# plt.show()

def analyze_beams(df, beam_type):
    max_length = None
    max_height = None
    max_base = None
    max_thickness = None
    max_serial_size = None
    selected_lengths = []
    selected_shear_stresses = []

    second_moment_of_area_function = get_second_moment_of_area_function(beam_type)

    for _, row in df.iterrows():
        height = row['height']
        base = row['base']
        thickness = row['thickness']
        serial_size = row['Serial size']
        SMoA = second_moment_of_area_function(height, base, thickness)
        lengths = []
        shear_stresses = []
        for length in np.arange(1, 20, 0.1):  # replace with your range of lengths
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

    print(f"The optimum length before ductile failure for {beam_type} is {max_length} m")
    print(f"The optimum height for {beam_type} is {max_height} m")
    print(f"The optimum base for {beam_type} is {max_base} m")
    print(f"The optimum thickness for {beam_type} is {max_thickness} m")
    print(f"The selected serial size for {beam_type} is {max_serial_size}")

    plt.plot(selected_lengths, selected_shear_stresses, label=f'Shear Stress of Selected {beam_type}')
    plt.axhline(y=material_yield_strength, color='r', linestyle='-', label='Yield Strength')
    plt.xlabel('Beam Length (m)')
    plt.ylabel('Shear Stress (Pa)')
    plt.title(f'Beam Length vs Shear Stress for {beam_type}')
    plt.legend()
    plt.show()

analyze_beams(df_Ibeam, 'I-beam')
analyze_beams(df_HSS, 'HSS')
analyze_beams(df_Teebar, 'Tee-bar')