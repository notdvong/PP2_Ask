import os

#1 Create a single directory
new_folder = "my_new_folder"
if not os.path.exists(new_folder):
    os.mkdir(new_folder)
    print(f"Created directory: {new_folder}")
#2 Create nested directories (a folder inside a folder)
nested_folders = "parent_folder/child_folder"
os.makedirs(nested_folders, exist_ok=True)
print(f"Created nested directories: {nested_folders}")

#3 List the contents of the current directory
print("\nContents of the current directory:")
current_contents = os.listdir('.')
for item in current_contents:
    print("-", item)