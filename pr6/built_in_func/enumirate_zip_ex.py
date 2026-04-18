#enumerate: Gives you both the index (count) and the item at the same time
print("--- Enumerate Example ---")
subjects = ["Discrete Structures", "Calculus 2", "Python"]

for index, subject in enumerate(subjects):
    print(f"Index {index}: {subject}")

#zip: Combines two or more lists so you can loop through them side-by-side
print("\n--- Zip Example ---")
students = ["Alice", "Bob", "Charlie"]
grades = [95, 88, 92]

for student, grade in zip(students, grades):
    print(f"{student} received a grade of {grade}")
