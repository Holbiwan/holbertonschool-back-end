#!/usr/bin/python3
"""Imports"""
import csv
import requests
import sys

def get_user_todos(user_id):
    """Get TODOs for a specific user."""
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/todos")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TODOs for user {user_id}: {e}")
        return []

def export_to_csv(employee_id, employee_name, todo_data):
    """Export TODO data to CSV."""
    csv_filename = f"{employee_id}.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(fieldnames)
        for task in todo_data:
            writer.writerow([
                employee_id,
                employee_name,
                str(task["completed"]),
                task["title"]
            ])

    print(f"CSV file '{csv_filename}' has been successfully created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} employee_id(int)")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Invalid employee ID. Please provide a valid integer.")
        sys.exit(1)

    # Fetch user data
    BASE_URL = "https://jsonplaceholder.typicode.com"
    user_url = f"{BASE_URL}/users/{employee_id}"

    # Fetch user data
    user_response = requests.get(user_url)
    
    if user_response.status_code != 200:
        print(f"Error fetching user data. Status code: {user_response.status_code}")
        sys.exit(1)

    user_data = user_response.json()
    if not user_data:
        print(f"Employee with ID {employee_id} not found.")
        sys.exit(1)

    employee_name = user_data["username"]
    # Fetch user's TODO list
    todo_data = get_user_todos(employee_id)

    # Export TODO data to CSV
    export_to_csv(employee_id, employee_name, todo_data)
