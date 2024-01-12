students_dictionary = {
    'UID_of_Student_1': 'Student 1',
    'UID_of_Student_2': 'Student 2',
    # Add more students as needed
}

# Example of how to access the names using UIDs
uid_to_lookup = 'UID_of_Student_1'
if uid_to_lookup in students_dictionary:
    student_name = students_dictionary[uid_to_lookup]
    print(f"Student with UID {uid_to_lookup} is {student_name}")
else:
    print(f"Unknown UID: {uid_to_lookup}")
