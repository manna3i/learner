import os

BASE_PATH = "Learner/Pre-algebra"

README_TEMPLATE = """# Problem {num} — Topic: {topic}

## Problem Description
(Write the problem here.)

## Notes
(Add steps, hints, or explanation.)

## Python Implementation
See `solution.py`.
"""

def get_next_problem_number(topic_path):
    folders = [f for f in os.listdir(topic_path) if f.startswith("problem_")]
    if not folders:
        return 1
    nums = []
    for f in folders:
        try:
            num = int(f.split("_")[1])
            nums.append(num)
        except:
            pass
    return max(nums) + 1 if nums else 1

def create_problem():
    topic = input("Enter topic name (e.g., fractions, equations, ratios): ").strip().lower()

    # Create topic directory if needed
    topic_path = os.path.join(BASE_PATH, topic)
    os.makedirs(topic_path, exist_ok=True)

    # Get next problem number
    problem_num = get_next_problem_number(topic_path)

    # Folder name
    folder_name = f"problem_{problem_num:02d}_in_{topic}"
    full_path = os.path.join(topic_path, folder_name)
    os.makedirs(full_path)

    # Create README.md
    readme_path = os.path.join(full_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(README_TEMPLATE.format(num=problem_num, topic=topic))

    # Create solution.py
    solution_path = os.path.join(full_path, "solution.py")
    with open(solution_path, "w") as f:
        f.write(f"# Solution for Problem {problem_num} in topic '{topic}'\n\n")

    print("\nCreated:")
    print(full_path)
    print("Files:")
    print(f"- {readme_path}")
    print(f"- {solution_path}\n")

if __name__ == "__main__":
    create_problem()
