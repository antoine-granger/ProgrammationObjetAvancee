import atexit

from CLI.CommandHandler.BookCommandHandler import BookCommandHandler
from CLI.CommandHandler.TransactionCommandHandler import TransactionCommandHandler
from CLI.CommandHandler.UserCommandHandler import UserCommandHandler
from CLI.DockerInfrastructure.DockerInfrastructure import DockerInfrastructure
from CLI.Terminal.Terminal import Terminal
from CLI.User.User import User

API_GATEWAY_URL = "http://localhost:5000"


def exit_handler(docker_infra):
    # Handler executed when the program exits
    print("Exiting program...")
    docker_infra.stop()


def cmd_prompt(session_user):
    if session_user.role == "admin":
        # Admin section
        print(
            "\nAdmin space"
            "\nHere is the list of available commands\n"
            "\n  - \033[32m'exit'\033[0m to exit"
            "\n  - \033[32m'book'\033[0m to manage books"
            "\n  - \033[32m'user'\033[0m to manage users"
            "\n  - \033[32m'transaction'\033[0m to manage transactions"
            "\n  - \033[32m'purge'\033[0m to purge the database and redeploy\n"
        )
        pass
    elif session_user.role == "user":
        print(
            "User space"
            "\nHere is the list of available commands\n"
            "\n  - \033[32m'exit'\033[0m to exit"
            "\n  - \033[32m'book'\033[0m to list books"
        )
    else:
        print("\033[31mInvalid role\033[0m")
        exit(1)


def get_login_info():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return {"username": username, "password": password}


def login_or_register(terminal):
    while True:
        command = input("Enter command \033[32m'login'\033[0m or \033[32m'register'\033[0m: ").lower()
        if command == "login":
            user_info = get_login_info()
            response = terminal.login(user_info)
            if isinstance(response, User):
                return response
            else:
                print(f"\033[31mLogin failed : {response}\033[0m")
        elif command == "register":
            user_info = get_login_info()
            response = terminal.register(user_info)
            if isinstance(response, User):
                print(f"Register user successful : \n{response.display_info()}")
                return response
            else:
                print(f"\033[31mRegister user failed : {response}\033[0m")
        else:
            print("\033[31mInvalid command, try again...\033[0m")


def handle_admin_commands(command, session_user, docker_infra):
    if command == "purge":
        docker_infra.purge()
    elif command in ["book", "user", "transaction"]:
        handle_entity_commands(command, session_user)


def handle_user_commands(command, session_user):
    if command in ["book", "transaction"]:
        handle_entity_commands(command, session_user)


def handle_entity_commands(entity, session_user):
    command_handler = {
        "book": BookCommandHandler(session_user),
        "user": UserCommandHandler(session_user),
        "transaction": TransactionCommandHandler(session_user)
    }.get(entity)

    if command_handler:
        command_handler.display_functions(session_user.role)
        entity_command = input(f"Enter command for {entity}: \n")
        command_handler.handle_command(entity_command)
    else:
        print("\033[31mInvalid command\033[0m")


def main(docker_infra):
    terminal = Terminal()
    if terminal.healthcheck() is not True:
        docker_infra.deploy()
        if terminal.healthcheck() is not True:
            print(f"\033[31mdocker infra failed to deploy...\033[0m")
            docker_infra.stop()
            return

    print("Welcome to the library\n")
    session_user = login_or_register(terminal)

    if not session_user:
        print("\033[31mLogin or registration failed. Exiting program.\033[0m")
        return

    while True:
        print("\n=====================")
        cmd_prompt(session_user)
        command = input().lower()
        if command == "exit":
            break
        if session_user.role == "admin":
            handle_admin_commands(command, session_user, docker_infra)
        elif session_user.role == "user":
            handle_user_commands(command, session_user)
        else:
            print("\033[31mInvalid role\033[0m")
            break


if __name__ == "__main__":
    docker_infra = DockerInfrastructure(
        stack_name="library",
        network_name="main-network",
        volume_names=["books_pgdata", "users_pgdata", "transactions_pgdata"],
    )
    #atexit.register(lambda: exit_handler(docker_infra))
    try:
        main(docker_infra)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected.")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        print("Exiting program.")
