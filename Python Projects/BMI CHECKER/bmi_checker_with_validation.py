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
    
def bmi_checker_improved() -> dict[str, float | str]:
    """
    Interactive BMI checker that collects user information, computes BMI,
    classifies it, and provides health advice.

    Returns
    -------
    dict
        A dictionary containing:
        - name : str
        - age : int
        - age_group : str
        - height_m : float
        - weight_kg : float
        - bmi : float (rounded to 2 decimals)
        - status : str (BMI category)
        - advice : str (health advice)
        - note : str (extra note for age < 18)

    Notes
    -----
    - Users can input height in meters, centimeters, or inches.
    - Users can input weight in kilograms or pounds.
    - Inputs are validated to prevent invalid or unrealistic values.

    """
    print("=== AGE & BMI CHECKER (IMPROVED) ===")
    
    name = input("Enter your name: ").strip() or "Anonymous"
    age = get_int_value("Enter your age (years): ", min_value=0)

    # Choose units
    print("\nChoose height unit:")
    height_unit = choose_options(
        "Select (type number): ",
        {"1": "meters (e.g. 1.75)", "2": "centimeters (e.g. 175)", "3": "inches (e.g. 69)"}
    )

    print("\nChoose weight unit:")
    weight_unit = choose_options("Select (type number): ", {"1": "kilograms (kg)", "2": "pounds (lb)"})

    # Read and convert height
    if height_unit == "1":
        height_m = get_float_value("Enter height in meters: ", min_value=0.3)
    elif height_unit == "2":
        height_m = get_float_value("Enter height in centimeters: ", min_value=30) / 100
    else:
        height_m = get_float_value("Enter height in inches: ", min_value=10) * 0.0254

    # Read and convert weight
    if weight_unit == "1":
        weight_kg = get_float_value("Enter weight in kilograms: ", min_value=1)
    else:
        weight_kg = get_float_value("Enter weight in pounds: ", min_value=2) * 0.45359237

    # Safety check
    if height_m <= 0:
        print("Error: computed height is zero or negative. Aborting.")
        return {}

    bmi_val = bmi(weight_kg, height_m)
    status, advice, note = classify_bmi(bmi_val, age)
    ag = age_group(age)

    result = {
        "name": name,
        "age": age,
        "age_group": ag,
        "height_m": height_m,
        "weight_kg": weight_kg,
        "bmi": round(bmi_val, 2),
        "status": status,
        "advice": advice,
        "note": note,
    }

    print("\n--- RESULTS ---")
    print(f"Name: {result['name']}")
    print(f"Age: {result['age']} ({result['age_group']})")
    print(f"Height: {result['height_m']:.2f} m")
    print(f"Weight: {result['weight_kg']:.1f} kg")
    print(f"BMI: {result['bmi']:.2f}")
    print(f"Category: {result['status']}")
    if result['note']:
        print(result['note'])
    print("\nHealth Advice:")
    print(result['advice'])

    print("\nDisclaimer: This tool provides general information only and is not medical advice.")

    return result


if __name__ == "__main__":
    bmi_checker_improved()




