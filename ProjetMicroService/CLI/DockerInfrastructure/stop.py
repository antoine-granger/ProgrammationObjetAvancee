from CLI.DockerInfrastructure.docker_utils import run_command


def stop_stack(stack_name):
    print(f"Stopping stack '{stack_name}'...")
    return run_command(f"docker stack rm {stack_name}")
