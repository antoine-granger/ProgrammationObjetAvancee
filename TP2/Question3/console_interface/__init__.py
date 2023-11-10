import requests

import utils.docker_utils
import os
from utils.docker_utils import *


def post_user():
    global name, role, user
    print("User name: ")
    name = input()
    print("User role: ")
    role = input()
    print("User password: ")
    password = input()
    user = {
        "username": name,
        "password": password,
        "role": role
    }
    print(requests.post(USERS_URL + "/users", json=user))


def delete_user():
    print("User id: ")
    id = input()
    requests.delete(USERS_URL + "/users/" + id)


if __name__ == "__main__":
    print("Welcome to the Interface!")
    stopProgram = False
    USERS_URL= "http://users-service:5000"
    BOOKS_URL= "http://books-service:5000"
    TRANSACTIONS_URL= "http://transactions-service:5000"
    appState = 0
    while not stopProgram:
        # get input from user
        user_input = input()
        client = docker.from_env()
        # 0 for docker interface, 1 for http interface
        if appState == 0:
            if user_input == "exit":
                stopProgram = True

            elif user_input == "deploy":
                print("=========================== Compose Up ==========================")
                deploy_docker_compose_up()
                client = docker.from_env()

            elif user_input == "stop":
                print("=========================== Compose Down =========================")
                deploy_docker_compose_down()

            elif user_input == "clean":
                print("=========================== Clear Images =========================")
                image_list = client.images.list()
                clear_images(image_list)
                print("=========================== Clear Images =========================")
                volume_list = client.volumes.list()
                clear_volumes(volume_list)

            elif user_input == "list":
                print("=========================== Conteneurs Actifs ====================")
                client = docker.from_env()
                for container in client.containers.list():
                    print(container.name)

            elif user_input == "http":
                appState = 1
                print("http commands enabled")
                print("Available commands: ")
            elif user_input == "help":
                print("Available commands: ")
                print("exit: exit the program")
                print("deploy: deploy the dockers")
                print("stop: stop the dockers")
                print("clear: clean the docker images and volumes")

            else:
                print("Commande invalide")

        elif appState == 1:
            if user_input == "exit":
                stopProgram = True

            elif user_input == "docker":
                appState = 0
                print("docker commands enabled")

            elif user_input == "help":
                print("Available commands: exit docker")
            else:
                print("Commande invalide")
