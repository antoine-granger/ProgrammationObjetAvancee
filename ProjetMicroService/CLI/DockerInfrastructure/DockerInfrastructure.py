from CLI.DockerInfrastructure.clear import (
    remove_stack,
    remove_network,
    remove_volume,
)

from CLI.DockerInfrastructure.deploy import (
    deploy_stack,
    init_swarm,
    scale_service,
    restart_service,
)
from CLI.DockerInfrastructure.stop import stop_stack


class DockerInfrastructure:
    def __init__(self, stack_name, network_name, volume_names):
        self.stack_name = stack_name
        self.network_name = network_name
        self.volume_names = volume_names

    def deploy(self):
        # Deploy the stack
        init_swarm()
        deploy_output = deploy_stack("docker-compose.yml", self.stack_name)
        print(deploy_output)
        # Scale the service api-gateway to be 2 containers
        scale_output = scale_service(self.stack_name, "api-gateway", 2)
        print(scale_output)

    def stop(self):
        # Stop the stack
        stop_output = stop_stack(self.stack_name)
        print(stop_output)

    def clear(self):
        # Suppress the stack
        print(remove_stack(self.stack_name))
        # Suppress the network
        print(remove_network(self.network_name))
        # Suppress the volumes
        for volume_name in self.volume_names:
            print(remove_volume(volume_name))

    def purge(self):
        # Relaunch the stack
        self.stop()
        self.clear()
        self.deploy()
