import os
import json
from datetime import datetime
from sys import argv

todo_template = {"Tasks-Done": 0}
todo_list = {"Tasks-Done": 0}
prompt_str = "TODO-APP--> "
script_dir = os.path.dirname(__file__)
save_file = script_dir + "/save--todo--app.json"

def save(obj, dest):
	with open(dest, "w") as f:
		json.dump(obj, f, indent=4)

def load(dest):
	try:
		with open(dest, "r") as f:
			return json.load(f)
	except:
		return todo_template

def view_list():
	for x, y in todo_list.items():
		print(f"{x}: {y}")


def add_to_list():
	add_prompt = f"{prompt_str}:ADD: "
	new_task = input(f"{add_prompt}")
	i = str(len(todo_list.keys()))
	todo_list.update({i: new_task})

def refresh_keys():
	temp_dict = {"Tasks-Done": todo_list["Tasks-Done"]}
	count = 1
	for x, y in todo_list.items():
		if x != "Tasks-Done":
			temp_dict.update({str(count): y})
			count += 1
	return temp_dict


def clear_done_str():
	done_str = " --> Done"
	for x, y in todo_list.items():
		if done_str in str(y):
			todo_list[x] = y.replace(done_str, "")
	todo_list["Tasks-Done"] = 0

to_view = True
cmds = f"Commands:\nadd\tremove\nhelp\tclose\ndone\tremove all\nreset\n"
explanation = "For the remove and done commands you simply type the word and when prompted input the index of the todo you want to remove or mark as done.\nThe reset command will bring all todos back to being unfinished.\nThe add command will give you a prompt to add a todo.\n"
quick_cmds = f"Quick Command Line Commands: python3 todo_program.py -r (prints out the list without opening interface)\npython3 todo_program.py -a 'your-todo-here' (adds to todo list without opening interface)\npython3 todo_program.py -d indexesOfDoneTodos Sperated By a Space (marks those todos as done)\npython3 todo_program.py -reset (marks all todos as unfinished)"
remove_prompt = f"{prompt_str}:REMOVE: "
todo_list = load(save_file)


def save_view_and_exit(to_save=True):
	if to_save:
		save(todo_list, save_file)
	view_list()
	exit()


def quick_add(s):
	print("Todo-Added!\n")
	index = str(len(todo_list.keys()))
	todo_list.update({index: s})
	save_view_and_exit()


if len(argv) == 2:
	if argv[1] == "-r":
		save_view_and_exit(False)
	elif argv[1] == "-reset":
		clear_done_str()
		save_view_and_exit()

if len(argv) >= 3:
	if argv[1] == "-a":
		quick_add(argv[2])
	elif argv[1] == "-d":
		for x in range(2, len(argv)):
			if argv[x] in todo_list.keys():
				if " --> Done" in todo_list[argv[x]]:
					continue
				todo_list[argv[x]] = todo_list[argv[x]] + " --> Done"
				todo_list["Tasks-Done"] += 1
		save_view_and_exit()

		
print("--TODO APP INITALIZED--")
print(cmds)
print(datetime.now())
view_list()



while True:
	# Want to update the list based off of a user prompt
	cmd = input(prompt_str)

	if cmd == "add":
		add_to_list()
	elif cmd == "remove":
		task_to_remove = input(remove_prompt)
		if task_to_remove in todo_list.keys():
			del todo_list[task_to_remove]
			todo_list = refresh_keys()
	elif cmd == "help":
		print(cmds)
		print(explanation)
		print(quick_cmds)
		to_view = False
	elif cmd == "close":
		print("Exiting")
		save(todo_list, save_file)
		break
	elif cmd == "remove all":
		todo_list = todo_template
		print("List cleared")
	elif cmd == "done":
		done_prompt = f"{prompt_str}:DONE: "
		done_str = " --> Done"
		task_done = input(done_prompt)
		if task_done in todo_list.keys():
			todo_list[task_done] = todo_list[task_done] + done_str
			todo_list["Tasks-Done"] += 1
	elif cmd == "reset":
		clear_done_str()
	



	if to_view: view_list()
	to_view = True