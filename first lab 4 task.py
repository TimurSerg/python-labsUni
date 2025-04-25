def add_task(task_dict, task_name, status):
    task_dict[task_name] = status

def remove_task(task_dict, task_name):
    if task_name in task_dict:
        del task_dict[task_name]

def update_task_status(task_dict, task_name, new_status):
    if task_name in task_dict:
        task_dict[task_name] = new_status

task_dict = {'task1': 'in progress', 'task2': 'pending', 'task3': 'completed'}
add_task(task_dict, 'task4', 'pending')
remove_task(task_dict, 'task1')
update_task_status(task_dict, 'task2', 'completed')

# Створюємо список задач, що в статусі 'pending'
pending_tasks = [task for task, status in task_dict.items() if status == 'pending']
print(task_dict)
print(pending_tasks)