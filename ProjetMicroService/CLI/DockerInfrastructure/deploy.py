from CLI.DockerInfrastructure.docker_utils import run_command


def init_swarm():
    print("Initializing Docker Swarm...")
    return run_command("docker swarm init")


def deploy_stack(compose_file, stack_name):
    print(f"Deploying stack '{stack_name}'...")
    return run_command(f"docker stack deploy -c {compose_file} {stack_name}")


def list_services(stack_name):
    print(f"Listing services for stack '{stack_name}'...")
    return run_command(f"docker stack services {stack_name}")


def scale_service(stack_name, service_name, replicas):
    print(f"Scaling service '{service_name}' to {replicas} replicas...")
    return run_command(f"docker service scale {stack_name}_{service_name}={replicas}")


def restart_service(stack_name, service_name):
    print(f"Restarting service '{service_name}'...")
    return run_command(f"docker service update --force {stack_name}_{service_name}")
