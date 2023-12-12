from CLI.DockerInfrastructure.docker_utils import run_command


def remove_stack(stack_name):
    print(f"Removing stack '{stack_name}'...")
    return run_command(f"docker stack rm {stack_name}")


def remove_network(network_name):
    print(f"Removing network '{network_name}'...")
    return run_command(f"docker network rm {network_name}")


def remove_volume(volume_name):
    print(f"Removing volume '{volume_name}'...")
    return run_command(f"docker volume rm {volume_name}")
