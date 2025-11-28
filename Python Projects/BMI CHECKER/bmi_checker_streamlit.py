import streamlit as st

def get_float_value(prompt: str, min_value:float = None, allow_zero:bool= False):
    """
    This function repeatedly prompts the user until they enter a valid
    floating-point number. It also supports optional validation rules:

    Parameters
    ----------
    prompt : str
        The message shown to the user when requesting input.
    min_value : float, optional
        Minimum allowed value. If provided, the function rejects
        numbers smaller than this limit. Default is None (no limit).
    allow_zero : bool, optional
        If False (default), zero is considered invalid input.
        If True, zero is allowed.

    Returns
    -------
    float
        A validated floating-point number entered by the user.

    Notes
    -----
    - The function also converts comma (",") to dot (".")
    - The function keeps asking until valid input is received.
    """
    while True:
        s = input(prompt).strip()  # .strip used to remove extra space at start or
        try:
            s = s.replace(",", ".")  # replace comma with dot if enter mistakenly by the user
            val = float(s)           
        except ValueError:
            print("  Please enter a number (e.g. 1.75).")
            continue

        if not allow_zero and val == 0:  # check if the value entered by the user is 0
            print("  Value cannot be zero. Try again.")
            continue
        if (min_value is not None) and (val < min_value):
            print(f"  Please enter a value >= {min_value}.")
            continue
        return val
    
def get_int_value(prompt:str, min_value:int = None):
    """
    This function repeatedly prompts the user until they enter a valid
    integer number. It also supports optional validation rules:

    Parameters
    ----------
    prompt : str
        The message shown to the user when requesting input.
    min_value : int, optional
        Minimum allowed value. If provided, the function rejects
        numbers smaller than this limit. Default is None (no limit).

    Returns
    -------
    int
        A validated integer number entered by the user.

    Notes
    -----
    - The function keeps asking until valid input is received.
      
    """
    while True:
        s = input(prompt).strip()
        if not s:
            print("  Please type something.")
            continue
        try:
            val = int(s)
        except ValueError:
            print("  Please enter an integer (e.g. 25).")
            continue
        if (min_value is not None) and (val < min_value):
            print(f"  Please enter a value >= {min_value}.")
            continue
        return val
    
def choose_options(prompt: str, options: dict[str, str]):
    """
    This function repeatedly displays a numbered menu of options
    and asks the user to select one by entering the corresponding key.
    It ensures that the user's input matches one of the available options.

    Parameters
    ----------
    prompt : str
        The message displayed to the user when requesting input.
    options : dict of str -> str
        A dictionary mapping keys (user inputs) to descriptions.
        Example: {"1": "Meters", "2": "Centimeters", "3": "Inches"}

    Returns
    -------
    str
        The key corresponding to the user's selected option.

    """
    keys = list(options.keys())
    while True:
        for k in keys:
            print(f"  {k}. {options[k]}")

        choice = input(prompt).strip()
        
        if choice in keys:
            return choice 
        print("  Invalid choice — try again.") 


def bmi(weight:float, height:float):
    """
    Calculate Body Mass Index (BMI) from weight and height.

    Parameters
    ----------
    weight: float
        Weight of the person in kilograms (kg).
    height : float
        Height of the person in meters (m).

    Returns
    -------
    float
        The BMI value calculated using the formula:
        BMI = weight (kg) / (height (m))^2 
    """
    return weight / (height ** 2)

def classify_bmi(bmi:float, age:int):
    """
    Classify BMI into categories and provide health advice.

    Parameters
    ----------
    bmi : float
        Body Mass Index value.
    age : int
        Age of the person in years.

    Returns
    -------
    tuple of (status, advice, note) : (str, str, str)
        status : str
            BMI category (Underweight, Normal weight, Overweight, Obese)
        advice : str
            Health advice based on the BMI category
        note : str
            Additional note if the person is under 18 years old

    """
    if bmi < 18.5:
        status = "Underweight"
        advice = (
            "Consider a balanced increase in calories and nutrient-dense foods. "
            "Consult a professional if concerned."
        )
    elif 18.5 <= bmi < 25:
        status = "Normal weight"
        advice = "Great — maintain with balanced diet and regular physical activity."
    elif 25 <= bmi < 30:
        status = "Overweight"
        advice = (
            "Increase physical activity and reduce energy-dense / sugary foods. "
            "Small changes add up."
        )
    else:
        status = "Obese"
        advice = (
            "Consider a comprehensive plan with diet and activity changes; "
            "consult a healthcare professional for personalized guidance."
        )

    note = ""
    if age < 18:
        note = (
            "Note: BMI categories for children/teens are different (percentiles). "
            "This result uses adult thresholds."
        )

    return status, advice, note

def age_group(age: int):
    """
    Categorize a person into an age group.

    Parameters
    ----------
    age : int
        Age of the person in years.

    Returns
    -------
    str
        Age category based on the following ranges:
        - "Child"  : age < 13
        - "Teen"   : 13 <= age < 18
        - "Adult"  : 18 <= age < 60
        - "Senior" : age >= 60
        """
    if age < 13:
        return "Child"
    elif 13 <= age < 18:
        return "Teen"
    elif 18 <= age < 60:
        return "Adult"
    else:
        return "Senior"
    
# st.set_page_config(page_title="BMI Checker", page_icon="🩺")
# st.title("🩺 Age & BMI Checker")

# st.sidebar.header("Enter Your Details")

# # Sidebar inputs
# name = st.sidebar.text_input("Name", value="Anonymous")
# age = st.sidebar.number_input("Age (years)", min_value=0, step=1)

# height_unit = st.sidebar.selectbox("Height Unit", ["meters", "centimeters", "inches"])
# weight_unit = st.sidebar.selectbox("Weight Unit", ["kilograms", "pounds"])

# height_input = st.sidebar.number_input(f"Height ({height_unit})", min_value=0.0, step=0.01)
# weight_input = st.sidebar.number_input(f"Weight ({weight_unit})", min_value=0.0, step=0.1)

# # Calculate BMI
# if st.sidebar.button("Calculate BMI"):
#     # Convert height to meters
#     if height_unit == "centimeters":
#         height_m = height_input / 100
#     elif height_unit == "inches":
#         height_m = height_input * 0.0254
#     else:
#         height_m = height_input

#     # Convert weight to kg
#     if weight_unit == "pounds":
#         weight_kg = weight_input * 0.45359237
#     else:
#         weight_kg = weight_input

#     # Validate inputs
#     if height_m <= 0 or weight_kg <= 0:
#         st.error("Height and weight must be positive numbers!")
#     else:
#         bmi_val = bmi(weight_kg, height_m)
#         status, advice, note = classify_bmi(bmi_val, age)
#         ag = age_group(age)

#         # --- Display Results ---
#         st.subheader("Results")
#         st.write(f"**Name:** {name}")
#         st.write(f"**Age:** {age} ({ag})")
#         st.write(f"**Height:** {height_m:.2f} m")
#         st.write(f"**Weight:** {weight_kg:.1f} kg")
#         st.write(f"**BMI:** {bmi_val:.2f}")

#         if status == "Underweight":
#             st.warning(f"**Category:** {status}")
#         elif status == "Normal weight":
#             st.success(f"**Category:** {status}")
#         else:
#             st.error(f"**Category:** {status}")

#         if note:
#             st.info(note)

#         st.markdown("**Health Advice:**")
#         st.info(advice)

#         st.markdown("_Disclaimer: This tool provides general information only and is not medical advice._")  
# 
st.title("🧍‍♂️ Age & BMI Checker")

# Two columns for name and age
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", value="Anonymous")
with col2:
    age = st.number_input("Age (years)", min_value=0, step=1)

# Two columns for units
col3, col4 = st.columns(2)
with col3:
    height_unit = st.selectbox("Height Unit", ["meters", "centimeters", "inches"])
with col4:
    weight_unit = st.selectbox("Weight Unit", ["kilograms", "pounds"])

# Two columns for actual height and weight input
col5, col6 = st.columns(2)
with col5:
    height_input = st.number_input(f"Height ({height_unit})", min_value=0.0, step=0.01)
with col6:
    weight_input = st.number_input(f"Weight ({weight_unit})", min_value=0.0, step=0.1)

# ---------- Compute BMI ----------

if st.button("Calculate BMI"):
    # Convert height to meters
    if height_unit == "meters":
        height_m = height_input
    elif height_unit == "centimeters":
        height_m = height_input / 100
    else:
        height_m = height_input * 0.0254

    # Convert weight to kg
    if weight_unit == "kilograms":
        weight_kg = weight_input
    else:
        weight_kg = weight_input * 0.45359237

    # Safety check
    if height_m <= 0:
        st.error("Error: Height must be greater than 0.")
    elif weight_kg <= 0:
        st.error("Error: Weight must be greater than 0.")
    else:
        bmi_val = bmi(weight_kg, height_m)
        status, advice, note = classify_bmi(bmi_val, age)
        ag = age_group(age)

        # Display results
        st.subheader("📊 Results")
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age} ({ag})")
        st.write(f"**Height:** {height_m:.2f} m")
        st.write(f"**Weight:** {weight_kg:.1f} kg")
        st.write(f"**BMI:** {bmi_val:.2f}")
        st.write(f"**Category:** {status}")
        if note:
            st.info(note)
        st.write("**Health Advice:**")
        st.success(advice)

        st.caption("Disclaimer: This tool provides general information only and is not medical advice.")  