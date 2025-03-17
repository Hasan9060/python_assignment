def calculate_grade(percentage):
    if percentage >= 80:
        return "A+"
    elif percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "F"
    else:
        return "Fail"

students = []

while True:
    student = {}
    student["name"] = input("Enter Student Name: ")
    student["roll_number"] = input("Enter Roll Number: ")
    subjects = ["Math", "Physics", "Urdu", "English", "Computer"]
    total_marks = 0
    
    for subject in subjects:
        while True:
            try:
                marks = int(input(f"Enter marks for {subject} (0-100): "))
                if 0 <= marks <= 100:
                    student[subject] = marks
                    total_marks += marks
                    break
                else:
                    print("Marks should be between 0 and 100.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    student["total"] = total_marks
    student["percentage"] = total_marks / len(subjects)
    student["grade"] = calculate_grade(student["percentage"])
    students.append(student)
    
    print(f"Record of {student['name']} inserted successfully.")
    more = input("Do you want to insert more? (Y/N): ").strip().upper()
    if more != 'Y':
        break

print("\nFinal Report Cards")
print("=" * 50)
for student in students:
    print(f"Name: {student['name']}  | Roll No: {student['roll_number']}")
    for subject in subjects:
        print(f"{subject}: {student[subject]}")
    print(f"Total Marks: {student['total']} | Percentage: {student['percentage']:.2f}% | Grade: {student['grade']}")
    print("-" * 50)
