import os
import shutil

# create a dummy file and folder to practice with
with open("temp_file.txt", "w") as f:
    f.write("Just some temporary text.")
os.makedirs("archive_folder", exist_ok=True)

# Rename a file (moving it to the same directory with a new name)
os.rename("temp_file.txt", "renamed_file.txt")
print("File renamed to 'renamed_file.txt'")

# Move a file into another directory
source = "renamed_file.txt"
destination = "archive_folder/renamed_file.txt"

shutil.move(source, destination)
print(f"Moved file to {destination}")