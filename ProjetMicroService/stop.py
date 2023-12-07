from utils.docker_utils import run_command


def stop_stack(stack_name):
    print(f"Stopping stack '{stack_name}'...")
    return run_command(f"docker stack rm {stack_name}")


def main():
    stop_output = stop_stack("mystack")
    print(stop_output)


if __name__ == "__main__":
    main()
