🧮 Problem 1 : Day of the Week After Adding N Days
📘 Overview

This problem explores cyclic patterns—a key idea in pre-algebra and an important concept in computer science.

The days of the week repeat every 7 days, which means we can treat them as a cycle.
The task is to determine what day it will be after adding a certain number of days to a starting day.

This problem builds intuition about:

Modular arithmetic

Zero-based indexing

Repeating patterns

Mapping math patterns to real code

📥 Input Description

A starting day of the week, e.g. "Monday".

A number of days to add (non-negative integer).

The program validates the starting day and keeps asking until it receives a valid one.

🎯 Goal

Compute and print the resulting day of the week after adding the specified number of days to the starting day.

🔢 Mathematical Idea

Days of the week repeat every 7 days.
If each day has an index:

Monday → 0
Tuesday → 1
...
Sunday → 6


Then:

new_index = (start_index + num_days) % 7


The modulo % 7 ensures we wrap around correctly when the number of days exceeds 6.

Example:

Start = Tuesday (index 1)

Add = 10 days

1 + 10 = 11

11 % 7 = 4

Result = Friday

🧠 Skills Practiced

Input validation

Loops (while True)

List indexing

Modulo arithmetic

Mapping mathematical patterns to code logic

📂 Files in This Problem
README.md   → This explanation  
solution.py → Your Python implementation

 [Khan academy video ](https://www.khanacademy.org/math/pre-algebra/xb4832e56:patterns/xb4832e56:math-patterns/v/figuring-out-days-of-the-week)explaining the problem