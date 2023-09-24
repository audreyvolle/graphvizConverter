import json

# Prompt the user for the list of all classes offered
courses_file = input("Enter the path to the file containing the list of all courses offered: ")
required_file = input("Enter the path to the JSON file containing the names of required courses: ")

try:
    # Load the list of all courses offered
    with open(courses_file, 'r') as courses_file:
        all_courses_data = json.load(courses_file)
    
    # Load the JSON file containing the names of required courses
    with open(required_file, 'r') as required_file:
        required_courses_data = json.load(required_file)
except FileNotFoundError:
    print("One or both files not found. Please enter valid file paths.")
    exit(1)
except json.JSONDecodeError:
    print("Invalid JSON format in one or both files. Please provide valid files.")
    exit(1)

# Create a set of required course names for faster lookup
required_course_names = set(required_courses_data["degree_requirements"])
print(required_course_names);
# Filter the list of all courses to include only required courses
required_courses_data = [course for course in all_courses_data if course["id"] in required_course_names]

# Create a Graphviz DOT script
dot_script = "digraph G {\n"

# Dictionary to track unique course titles
unique_titles = {}

# Iterate through the required courses and add nodes and edges
for course in required_courses_data:
    course_id = course["id"]
    course_title = course["title"]
    prerequisites_and = course.get("prerequisitesAND", [])
    prerequisites_or = course.get("prerequisitesOR", [])

    # Add the course as a node if not already added
    if course_title not in unique_titles:
        dot_script += f'  "{course_id}" [label="{course_id}"];\n'
        unique_titles[course_title] = course_id

    # Add edges for prerequisites from "prerequisitesAND"
    for prereq in prerequisites_and:
        prereq_id = prereq["id"]
        dot_script += f'  "{prereq_id}" [label="{prereq_id}\\n{prereq.get("Grade", "")}"];\n'
        dot_script += f'  "{prereq_id}" -> "{course_id}";\n'

    # Add edges for prerequisites from "prerequisitesOR"
    for prereq in prerequisites_or:
        prereq_id = prereq["id"]
        dot_script += f'  "{prereq_id}" [label="{prereq_id}\\n{prereq.get("Grade", "")}"];\n'
        dot_script += f'  "{prereq_id}" -> "{course_id}" [style=dotted];\n'

# Close the DOT script
dot_script += "}"

# Print the DOT script
print(dot_script)
