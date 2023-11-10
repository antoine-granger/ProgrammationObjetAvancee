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


def remove_docker_image(image_name):
    command = f"docker image rm {image_name}"
    subprocess.run(command, shell=True, check=True)


def clear_images(_list):
    for image in _list:
        # print image name
        image_name = image.tags[0]
        print(image_name)
        if str(image_name).__contains__("question3") or str(image_name).__contains__("postgre"):
            command = f"docker image rm {image_name}"
            subprocess.run(command, shell=True, check=True)


def clear_volumes(_list):
    for volume in _list:
        volume_name = str(volume.name)
        if volume_name.__contains__("question3"):
            command = f"docker volume rm {volume_name}"
            subprocess.run(command, shell=True, check=True)

