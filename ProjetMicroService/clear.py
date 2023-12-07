from utils.docker_utils import run_command


def remove_stack(stack_name):
    print(f"Removing stack '{stack_name}'...")
    return run_command(f"docker stack rm {stack_name}")


def remove_network(network_name):
    print(f"Removing network '{network_name}'...")
    return run_command(f"docker network rm {network_name}")


def remove_volume(volume_name):
    print(f"Removing volume '{volume_name}'...")
    return run_command(f"docker volume rm {volume_name}")


def main():
    stack_name = "mystack"
    network_name = "main-network"
    volume_names = ["books_pgdata", "users_pgdata", "transactions_pgdata"]
    
    # Suppress the stack
    print(remove_stack(stack_name))
    
    # Suppress the network
    print(remove_network(network_name))
    
    # Suppress the volumes
    for volume_name in volume_names:
        print(remove_volume(volume_name))


if __name__ == "__main__":
    main()
