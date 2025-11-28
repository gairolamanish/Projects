def bmi_checker():
    name = input("Please Enter Your Name: ")
    age = int(input("Please Enter Your Age: "))
    height = float(input("Please Enter Your Height(in meter): "))
    weight = float(input("Please Enter Your weight(in kg): "))

    bmi = weight/(height **2)

    if bmi < 18.5:
        bmi_status = "Underweight"
        advice = ("You are underweight. Consider eating nutrient-dense foods "
                  "and increasing calories.")
    elif 18.5 <= bmi < 25:
        bmi_status = "Normal weight"
        advice = ("Healthy weight! Maintain with balanced diet and exercise.")
    elif 25 <= bmi < 30:
        bmi_status = "Overweight"
        advice = ("Slightly overweight. Try more physical activity and reduce junk food.")
    else:
        bmi_status = "Obese"
        advice = ("Obese category. Try healthier diet and regular exercise.")

    print("\n--- RESULTS ---")
    print(f"BMI: {bmi:.2f}")
    print(f"Category: {bmi_status}")
    print("\nAdvice:")
    print(advice)


bmi_checker()        