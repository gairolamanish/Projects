# Student Performance Analysis

A beginner-friendly Python data analysis project that analyzes student performance using **Pandas, NumPy, and Matplotlib**.

The project calculates subject-wise and student-wise performance, identifies the top and lowest-performing students, classifies students as Pass or Fail, and generates visualizations of the results.

## Features

* Load student performance data from a CSV file
* Explore the dataset using Pandas
* Generate statistical summaries
* Calculate subject-wise average marks
* Calculate student-wise average marks
* Identify the top-performing student
* Identify the lowest-performing student
* Classify students as Pass or Fail
* Count the number of passing and failing students
* Generate an average marks bar chart
* Generate a marks distribution histogram

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib

## Project Structure

```
student performance/
│
├── data/
│   └── student_performance.csv
│
├── charts/
│   ├── subject_average.png
│   └── marks_distribution.png
│
├── src/
│   └── data_analysis.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The program will display the analysis results in the terminal and generate the charts inside the `charts` folder.

## Analysis Performed

### Subject-wise Average

The project calculates the average marks for:

* Math
* Science
* English

### Student-wise Average

The average score of each student is calculated using all three subjects.

### Top and Lowest Student

The project identifies:

* Student with the highest average
* Student with the lowest average

### Pass/Fail Classification

Students with an average score of **70 or above** are classified as:

```
Pass
```

Students with an average below 70 are classified as:

```
Fail
```

## Visualizations

### Average Marks by Subject

The project generates a bar chart comparing the average marks across subjects.

### Marks Distribution

A histogram is generated to show how the marks are distributed across different score ranges.






