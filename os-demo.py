import os


def check_directory():
	dir_name = input("Enter a directory name: ")
	if os.path.isdir(dir_name):
		print("That is a valid directory")
	else:
		print("That is not a valid directory")

def create_directory():
	dir_name = input("Enter the new directory's name: ")
	if os.path.exists(dir_name):
		print("You cannot overwrite an existing file/directory.")
	else:
		os.makedirs(dir_name)
		print("Directory has been created")

def create_file():
	dir_name = input("Enter the name of the directory to put the file: ")

	if os.path.isdir(dir_name):
		file_name = input("Enter the name of the file: ")
		file_path = os.path.join(dir_name, file_name)
		if not os.path.exists(file_path):
			contents = input("Enter the contents for the file: ")
			fileout = open(file_path, "w")
			fileout.write(contents)
			fileout.close()
		else:
			print("Something already exists with that name.")
	else:
		print("There is no directory with that name.")

def list_directory():
	dir_name = input("Enter the directory's name: ")
	if os.path.isdir(dir_name):
		files = os.listdir(dir_name)
		print("The files in that directory are: ")
		for file in files:
			print(file)
	else:
		print("That directory doesn't exist.")

def check_file():
	dir_name = input("Enter the directory's name: ")
	if os.path.isdir(dir_name):
		file_name = input("Enter the name of the file: ")
		file_path = os.path.join(dir_name, file_name)
		if os.path.isfile(file_path):
			print("That file exists.")
		else:
			print("That is not a file within the given directory.")
	else:
		print("That directory doesn't exist.")

def print_file():
	dir_name = input("Enter the directory's name: ")
	if os.path.isdir(dir_name):
		file_name = input("Enter the name of the file: ")
		file_path = os.path.join(dir_name, file_name)
		if os.path.isfile(file_path):
			filein = open(file_path, "r")
			print("Here are the contents: ")
			print(filein.read())
			filein.close()
		else:
			print("That is not a file within the given directory.")
	else:
		print("That directory doesn't exist.")

def delete_file():
	dir_name = input("Enter the directory's name: ")
	if os.path.isdir(dir_name):
		file_name = input("Enter the name of the file: ")
		file_path = os.path.join(dir_name, file_name)
		if os.path.isfile(file_path):
			os.remove(file_path)
		else:
			print("That is not a file within the given directory.")
	else:
		print("That directory doesn't exist.")

def delete_directory():
	dir_name = input("Enter the directory's name: ")
	if os.path.isdir(dir_name):
		files = os.listdir(dir_name)
		for file in files:
			os.remove(os.path.join(dir_name, file))
		os.rmdir(dir_name)
	else:
		print("That directory doesn't exist.")


def get_user_selection():
	print()
	print()
	print("Make a selection:")
	print("1. Check if directory exists")
	print("2. Create a new directory")
	print("3. Create a file within a directory")
	print("4. List all files in a directory")
	print("5. Check if file exists in directory")
	print("6. Print contents of file in directory")
	print("7. Delete a file in a directory")
	print("8. Delete a directory")
	print("9. Quit")

	return int(input("Enter a choice: "))


choice = get_user_selection()

while choice != 9:
	if choice == 1:
		check_directory()
	elif choice == 2:
		create_directory()
	elif choice == 3:
		create_file()
	elif choice == 4:
		list_directory()
	elif choice == 5:
		check_file()
	elif choice == 6:
		print_file()
	elif choice == 7:
		delete_file()
	elif choice == 8:
		delete_directory()

	choice = get_user_selection()
