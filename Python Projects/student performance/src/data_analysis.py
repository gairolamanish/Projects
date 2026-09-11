import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

df = pd.read_csv("data/student_performance.csv")


# --------------------------------------------------
# 2. Basic Dataset Exploration
# --------------------------------------------------

print("\nDataset Summary:")
print(df.describe())


# --------------------------------------------------
# 3. Subject-wise Average
# --------------------------------------------------

math_average = df["math"].mean()
science_average = df["science"].mean()
english_average = df["english"].mean()

print("\nSubject Averages:")
print("Math:", math_average)
print("Science:", science_average)
print("English:", english_average)


# --------------------------------------------------
# 4. Student-wise Average
# --------------------------------------------------

df["average"] = df[["math", "science", "english"]].mean(axis=1)

print("\nStudent-wise Average:")
print(df[["name", "average"]])


# --------------------------------------------------
# 5. Find Top Student
# --------------------------------------------------

top_student = df.loc[df["average"].idxmax()]

print("\nTop Student:")
print(top_student)


# --------------------------------------------------
# 6. Find Lowest Student
# --------------------------------------------------

lowest_student = df.loc[df["average"].idxmin()]

print("\nLowest Student:")
print(lowest_student)


# --------------------------------------------------
# 7. Pass / Fail Classification
# --------------------------------------------------

df["status"] = np.where(
    df["average"] >= 70,
    "Pass",
    "Fail"
)

print("\nStudent Status:")
print(df[["name", "average", "status"]])


# --------------------------------------------------
# 8. Count Pass / Fail Students
# --------------------------------------------------

pass_count = (df["status"] == "Pass").sum()
fail_count = (df["status"] == "Fail").sum()

print("\nPass / Fail Count:")
print("Passed students:", pass_count)
print("Failed students:", fail_count)


# --------------------------------------------------
# 9. Subject Average Chart
# --------------------------------------------------

subject_averages = {
    "Math": math_average,
    "Science": science_average,
    "English": english_average
}

print("\nSubject Averages Dictionary:")
print(subject_averages)

plt.bar(
    subject_averages.keys(),
    subject_averages.values()
)

plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")

plt.savefig("charts/subject_average.png")
plt.show()


# --------------------------------------------------
# 10. Marks Distribution Histogram
# --------------------------------------------------

all_marks = df[
    ["math", "science", "english"]
].values.flatten()

plt.hist(
    all_marks,
    bins=5,
    edgecolor="black"
)

plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Number of Students")

plt.savefig("charts/marks_distribution.png")
plt.show()

