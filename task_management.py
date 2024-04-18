import datetime
import mysql.connector
from plyer import notification


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1234",
    database="task_managament"
)

cursor = conn.cursor()


class TaskManager:

    def __init__(self):
        self.tasks = {}

    def add_task(self):
        task_name = input("Enter task name: ").strip()
        description = input("Enter description: ").strip()
        due_date = input("Enter due date (yyyy-mm-dd): ")
        category = input("Enter category: ").strip().lower()

        cursor.execute(
            f"SELECT * FROM categories WHERE category = '{category}'")

        category_id, *_ = cursor.fetchall()[0]

        cursor.execute(
            f"INSERT INTO tasks (task_name, description, due_date, user_id, category_id) VALUES ('{task_name}', '{description}', '{due_date}', '{user_id}', '{category_id}')")
        conn.commit()

    def view_tasks(self, user_id):
        cursor.execute(
            f"SELECT id, category_id, task_name, description, due_date FROM tasks WHERE user_id = {user_id}")
        tasks = cursor.fetchall()
        tasks_to_show = []
        if not tasks:
            print("No tasks available.")
            exit(0)

        for task in tasks:
            cursor.execute(
                f"SELECT category FROM categories WHERE id = {task[1]}")

            category_name, *_ = cursor.fetchall()[0]
            tasks_to_show.append(
                f"{task[0]} - {task[2]} - {task[3]} - {task[4]} - {category_name}")

        for task in tasks_to_show:
            print(task)

    def remove_tasks(self, task_id):
        cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
        tasks = cursor.fetchall()
        if not tasks:
            print("Task not found.")
            return
        else:
            cursor.execute(
                f"DELETE FROM tasks WHERE id = {task_id}")
            conn.commit()

    def send_reminders(self, user_id):
        cursor.execute(
            f"SELECT task_name, due_date FROM tasks WHERE user_id = '{user_id}'")
        tasks = cursor.fetchall()

        for task in tasks:
            task_name, due_date = task
            print(due_date)
            if due_date == datetime.date.today():
                notification.notify(
                    title="Task Reminder",
                    message=f"Task '{task_name}' is due today!",
                    app_icon=None,
                    timeout=5,
                )


if __name__ == "__main__":

    username = input("enter username: ")
    password = input("enter password: ")

    cursor.execute(f"SELECT * FROM users WHERE name = '{username}'")

    user_info = cursor.fetchall()

    if user_info:
        cursor.execute(
            f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'")
        user_info = cursor.fetchall()

        while not user_info:
            print("Invalid credentials.")
            password = input("enter password: ")

            cursor.execute(
                f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'")
            user_info = cursor.fetchall()

            if user_info:
                break

        user_id, *args = user_info[0]
        print("Login successful")

        while user_info:
            task_manager = TaskManager()
            print("choose an option: ")
            print("1. Add task")
            print("2. View tasks")
            print("3. Remove task")
            print("4. Send reminders")
            print("5. Exit")

            input_option = int(input("Enter your choice: "))

            if input_option == 1:
                task_manager.add_task()

            elif input_option == 2:
                task_manager.view_tasks(user_id=user_id)

            elif input_option == 3:
                task_id = int(input("Enter task ID to remove: "))
                task_manager.remove_tasks(task_id)
            elif input_option == 4:
                task_manager.send_reminders(user_id=user_id)
            elif input_option == 5:
                print("Exiting...")
                exit(0)
    else:
        print("1. Register")
        print("2. Exit")

        input_option = int(input("Enter your choice: "))

        if input_option == 1:
            username = input("enter username: ")
            password = input("enter password: ")

            cursor.execute(
                f"INSERT INTO users (name, password) VALUES ('{username}', '{password}')")
            conn.commit()
            print("User registered successfully.")
        else:
            print("Exiting...")
            exit(0)
