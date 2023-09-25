import docker
from utils.docker_utils import clear_images, clear_volumes

client = docker.from_env()
clear_volumes(client.volumes.list())
clear_images(client.images.list())