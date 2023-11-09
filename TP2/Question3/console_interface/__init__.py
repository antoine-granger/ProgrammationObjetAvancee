import subprocess
import docker


def deploy_docker_compose_up():
    try:
        # Assurez-vous d'être dans le répertoire où se trouve votre docker-compose.yml
        # Vous pouvez utiliser os.chdir() pour changer de répertoire si nécessaire.

        # Commande pour déployer avec docker-compose
        command = "docker-compose up -d"

        # Exécutez la commande avec subprocess
        subprocess.run(command, shell=True, check=True)

        print("Docker-compose déployé avec succès!")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du déploiement de Docker-compose : {e}")


def deploy_docker_compose_down():
    try:
        # Assurez-vous d'être dans le répertoire où se trouve votre docker-compose.yml
        # Vous pouvez utiliser os.chdir() pour changer de répertoire si nécessaire.

        # Commande pour déployer avec docker-compose
        command = "docker-compose down"

        # Exécutez la commande avec subprocess
        subprocess.run(command, shell=True, check=True)

        print("Docker-compose stoppé avec succès!")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'arret de Docker-compose : {e}")


def check_docker_status():
    try:
        client = docker.from_env()
        client.ping()
        print("Docker is up and running!")
    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker: {e}")


def remove_docker_image(image_name):
    command = f"docker image rm {image_name}"
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    print("=========================== Compose Up ==========================")
    deploy_docker_compose_up()

    client = docker.from_env()
    image_list = client.images.list()

    print("=========================== Conteneurs ===========================")
    for container in client.containers.list():
        print(container.name)
    print("=========================== Compose Down =========================")
    deploy_docker_compose_down()
    print("=========================== Clear Images =========================")
    for image in image_list:
        # print image name
        print(str(image.tags[0]).__contains__("question3") or str(image.tags[0]).__contains__("postgre"))
        remove_docker_image(image.tags[0])
