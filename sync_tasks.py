import requests
import uuid
import json
from dotenv import dotenv_values


def get_new_elements(todoist, github):
    for i in github:
        if i not in todoist:
            yield i


def get_delete_elements(todoist, github):
    for i in todoist:
        if i not in github:
            yield i


def main():
    config = dotenv_values(".env")
    github_token = config["GITHUB_TOKEN"]
    github_auth_header = {"Authorization": f'token {github_token}'}

    todoist_token = config["TODOIST_TOKEN"]
    todoist_project = int(config["TODOIST_PROJECT"])

    todoist_auth_header = {"Authorization": f'Bearer {todoist_token}'}

    github_json_response = requests.get('https://api.github.com/issues',
                                        headers=github_auth_header).json()

    todoist_json_response = requests.get("https://api.todoist.com/rest/v1/tasks",
                                         params={"project_id": todoist_project}, headers=todoist_auth_header).json()

    github_names = list(map(lambda elem: elem["title"], github_json_response))

    todoist_names = list(
        map(lambda elem: elem["content"][2:], todoist_json_response))

    new_elementes = list(get_new_elements(todoist_names, github_names))
    delete_elementes = list(get_delete_elements(todoist_names, github_names))
    delete_element_id = list(map(lambda elem: elem["id"], filter(
        lambda elem: elem["content"][2:] in delete_elementes, todoist_json_response)))

    # create tasks
    for i in new_elementes:
        x = requests.post(
            "https://api.todoist.com/rest/v1/tasks",
            data=json.dumps({
                "content": f'* {i}',
                "due_string": "today",
                "project_id": todoist_project,
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": todoist_auth_header["Authorization"]
            })
        if x.status_code != 200:
            raise Exception("Status code is not 200")

    # delete tasks
    for i in delete_element_id:
        x = requests.delete(f'https://api.todoist.com/rest/v1/tasks/{i}',
                            headers=todoist_auth_header)
        if x.status_code != 204:
            raise Exception("Element not deleted")


if __name__ == "__main__":
    main()
