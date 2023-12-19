#!/usr/bin/python3
"""
Uses a REST API for a given employee ID, returns
information about TODO list progress and exports in JSON
"""

import json
import requests
import sys

BASE_URL = "https://jsonplaceholder.typicode.com"


def get_user_todos(user_id):
    """Get TODOs for a specific user."""
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/todos")
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TODOs for user {user_id}: {e}")
        return []


def main():
    try:
        users_response = requests.get(f"{BASE_URL}/users")
        users_response.raise_for_status()
        users = users_response.json()

        dic_user = {}

        for user in users:
            tasks = get_user_todos(user['id'])
            dic_user[user["id"]] = []

            for task in tasks:
                dic_task = {
                    "task": task["title"],
                    "completed": task["completed"],
                    "username": user["username"]
                }
                dic_user[user["id"]].append(dic_task)

        with open("todo_all_employees.json", "w") as file:
            json.dump(dic_user, file, indent=2)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
