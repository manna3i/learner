#!/usr/bin/env python3
"""
manage.py

A single-file manager to create Topics and Problems under:
Learner/Pre-algebra/

Features:
- Create main README.md if missing
- Add Topic (creates Learner/Pre-algebra/<topic>/README.md and registers it in main README)
- Add Problem (creates problem_XX_<slug_title>/ with README.md and solution.py)
- Updates tables in main README and topic README
- Uses placeholders when user presses Enter
"""

import os
import re
import sys
from datetime import datetime

ROOT = "Learner"
SUBJECT = "Pre-algebra"
BASE_PATH = os.path.join(ROOT, SUBJECT)
MAIN_README = os.path.join(BASE_PATH, "README.md")

TOPIC_README_TEMPLATE = """# {topic_title}

{topic_description}

## Problems

| Problem | Description |
|---------|-------------|
"""

PROBLEM_README_TEMPLATE = """# Problem {num} — {title}

## Problem Description
(Write the problem statement here.)

## Notes / Math Explanation
(Add reasoning, math steps, examples.)

## Python Implementation
See `solution.py`.
"""

MAIN_README_TEMPLATE = """# Pre-Algebra Learning Hub

This folder contains all the topics and practice problems I'm learning.

## Topics

(Topics will be listed below.)
"""

def ensure_base():
    os.makedirs(BASE_PATH, exist_ok=True)
    if not os.path.exists(MAIN_README):
        with open(MAIN_README, "w", encoding="utf-8") as f:
            f.write(MAIN_README_TEMPLATE)
        print(f"Created main README: {MAIN_README}")

def slugify(text):
    """Make a safe slug for folder names: lowercase, replace spaces with underscore,
       remove non-alphanumeric/underscore characters, collapse multiple underscores."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)        # remove non-word chars
    text = re.sub(r"[-\s]+", "_", text)         # spaces/dashes -> underscore
    text = re.sub(r"_+", "_", text)             # collapse multiple underscores
    return text or "untitled"

def title_case_topic(topic):
    # keep nice display: each word capitalized
    return " ".join([w.capitalize() for w in re.split(r"[_\s]+", topic)])

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def add_topic():
    topic_raw = input("Enter topic name (e.g., fractions, equations): ").strip()
    topic = slugify(topic_raw) if topic_raw else input("Topic empty — enter a short topic name (or press Enter to use 'untitled'): ").strip() or "untitled"
    topic_title = title_case_topic(topic)
    topic_desc = input("Enter topic description (optional — press Enter for placeholder): ").strip() or "Description coming soon."

    topic_path = os.path.join(BASE_PATH, topic)
    topic_readme_path = os.path.join(topic_path, "README.md")

    if os.path.exists(topic_path):
        print(f"Topic '{topic_title}' already exists at {topic_path}")
    else:
        os.makedirs(topic_path, exist_ok=True)
        write_file(topic_readme_path, TOPIC_README_TEMPLATE.format(topic_title=topic_title, topic_description=topic_desc))
        print(f"Created topic folder and README: {topic_path}")

    # Ensure main README contains this topic section
    main_md = read_file(MAIN_README)
    topic_header = f"### {topic_title}"
    if topic_header in main_md:
        print("Main README already has this topic listed.")
        return

    # Append topic section at the end
    append_text = f"\n### {topic_title}\n{topic_desc}\n\n| Problem | Description |\n|---------|-------------|\n"
    with open(MAIN_README, "a", encoding="utf-8") as f:
        f.write(append_text)
    print(f"Added topic '{topic_title}' to main README.")

def get_next_problem_number_for_topic(topic_path):
    # lists directories that start with 'problem_'
    try:
        entries = os.listdir(topic_path)
    except FileNotFoundError:
        return 1
    nums = []
    for name in entries:
        m = re.match(r"problem_(\d{2})_", name)
        if m:
            try:
                nums.append(int(m.group(1)))
            except:
                pass
    return (max(nums) + 1) if nums else 1

def insert_problem_row_into_readme(readme_path, topic_slug, topic_title, problem_num, problem_title, description):
    """
    Adds a row under the relevant topic's table in readme_path.
    For main README: link should be relative path to topic/problem README.
    If the topic section or table is missing, create it.
    """
    content = read_file(readme_path)
    topic_header = f"### {topic_title}"
    rows_line = f"| [Problem {problem_num:02d} \u2013 {problem_title}]({topic_slug}/problem_{problem_num:02d}_{slugify(problem_title)}/README.md) | {description} |"

    if topic_header not in content:
        # Append a fresh topic section with table and the row
        append = f"\n### {topic_title}\nDescription coming soon.\n\n| Problem | Description |\n|---------|-------------|\n{rows_line}\n"
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(append)
        return

    # Topic exists — we need to find the table under this header.
    parts = content.split(topic_header, 1)
    before, after = parts[0], parts[1]
    # after starts with newline + description etc.
    # Find the table header (| Problem | Description |). If not found, create it.
    table_header_re = r"\| Problem \| Description \|"
    if re.search(table_header_re, after):
        # find end of table header line then insert the row after the header (or at end of table)
        # naive approach: find the table block (from header line to the first blank line after it)
        table_start = re.search(table_header_re, after).start()
        # from here, find the position of the newline after the header and the dashed row
        # we'll find first blank line (two consecutive newlines) or the next section header starting with '### '
        # So extract the chunk until next '### ' or end
        next_topic_match = re.search(r"\n### ", after)
        if next_topic_match:
            table_block = after[:next_topic_match.start()]
            rest = after[next_topic_match.start():]
        else:
            table_block = after
            rest = ""
        # Insert the row at the end of the table_block (before the blank line)
        if table_block.rstrip().endswith("|"):
            # likely already ends with a row
            new_table_block = table_block.rstrip() + "\n" + rows_line + "\n\n"
        else:
            new_table_block = table_block + "\n" + rows_line + "\n\n"
        new_content = before + topic_header + new_table_block + rest
        write_file(readme_path, new_content)
    else:
        # no table — create a table and insert row
        insertion = "\nDescription coming soon.\n\n| Problem | Description |\n|---------|-------------|\n" + rows_line + "\n"
        new_content = content.replace(topic_header, topic_header + insertion, 1)
        write_file(readme_path, new_content)

def add_problem():
    topic_raw = input("Enter topic name (existing topic): ").strip()
    if not topic_raw:
        print("Topic name required.")
        return
    topic = slugify(topic_raw)
    topic_title = title_case_topic(topic)
    topic_path = os.path.join(BASE_PATH, topic)
    if not os.path.exists(topic_path):
        create_new = input(f"Topic '{topic_title}' does not exist. Create it? (y/n): ").strip().lower()
        if create_new != "y":
            print("Aborting. Create the topic first or choose another topic.")
            return
        # create topic with placeholder description
        os.makedirs(topic_path, exist_ok=True)
        write_file(os.path.join(topic_path, "README.md"), TOPIC_README_TEMPLATE.format(topic_title=topic_title, topic_description="Description coming soon."))
        # add to main readme
        insert_problem_row_into_readme(MAIN_README, topic, topic_title, 0, "placeholder", "Description coming soon.")  # this will create the section if missing
        # then remove placeholder row below (we'll proceed)
        print(f"Created topic {topic_title} with placeholder README.")

    # ask for problem title
    problem_title_raw = input("Enter short problem title (optional — press Enter for 'untitled problem'): ").strip()
    problem_title = problem_title_raw if problem_title_raw else "untitled problem"
    description = input("Enter a one-line description for the table (optional): ").strip() or "No description provided."

    next_num = get_next_problem_number_for_topic(topic_path)
    slug_title = slugify(problem_title)
    folder_name = f"problem_{next_num:02d}_{slug_title}"
    problem_path = os.path.join(topic_path, folder_name)

    if os.path.exists(problem_path):
        print("Problem folder already exists — aborting to avoid overwrite.")
        return

    os.makedirs(problem_path, exist_ok=True)
    # create problem README and solution.py
    problem_readme_path = os.path.join(problem_path, "README.md")
    solution_py_path = os.path.join(problem_path, "solution.py")
    write_file(problem_readme_path, PROBLEM_README_TEMPLATE.format(num=next_num, title=problem_title))
    write_file(solution_py_path, f"# Solution for Problem {next_num:02d} — {problem_title}\n\n")
    print(f"Created problem folder: {problem_path}")

    # Update topic README (insert row under topic table in topic's README)
    topic_readme_path = os.path.join(topic_path, "README.md")
    # Ensure topic README exists and has table header
    if not os.path.exists(topic_readme_path):
        write_file(topic_readme_path, TOPIC_README_TEMPLATE.format(topic_title=topic_title, topic_description="Description coming soon."))
    # Insert row into topic README (link relative)
    row_topic = f"| [Problem {next_num:02d} \u2013 {problem_title}]({folder_name}/README.md) | {description} |"
    # read and write logic similar to main insert but simpler for local topic README
    topic_md = read_file(topic_readme_path)
    if "| Problem | Description |" not in topic_md:
        # append table and the row
        append = f"\n| Problem | Description |\n|---------|-------------|\n{row_topic}\n"
        write_file(topic_readme_path, topic_md + append)
    else:
        # insert row at end of table
        # find end of table (first blank line after the table header)
        parts = topic_md.split("| Problem | Description |", 1)
        before = parts[0] + "| Problem | Description |"
        after = parts[1]
        # after starts with the dashed line or continues
        # find where the next double-newline occurs
        match = re.search(r"\n\n", after)
        if match:
            table_block = after[:match.start()]
            rest = after[match.start():]
            new_table_block = table_block + "\n" + row_topic + "\n"
            new_topic_md = before + new_table_block + rest
        else:
            # append at the end
            new_topic_md = topic_md + "\n" + row_topic + "\n"
        write_file(topic_readme_path, new_topic_md)

    # Update main README with a relative link to topic/problem README
    insert_problem_row_into_readme(MAIN_README, topic, topic_title, next_num, problem_title, description)
    print("Updated topic README and main README with the new problem entry.")

def menu():
    ensure_base()
    print("\nManage Learner/Pre-algebra")
    print("Choose an action:")
    print("1) Add a new topic")
    print("2) Add a new problem to an existing topic")
    print("q) Quit")
    choice = input("> ").strip().lower()
    if choice == "1":
        add_topic()
    elif choice == "2":
        add_problem()
    elif choice == "q":
        print("Goodbye.")
        sys.exit(0)
    else:
        print("Unknown choice — try again.")

if __name__ == "__main__":
    while True:
        menu()
        cont = input("\nDo another action? (Y/n): ").strip().lower()
        if cont == "n":
            print("Done.")
            break
