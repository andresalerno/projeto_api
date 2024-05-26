echo "Instalador de pacotes do smart-farm"

apt upgrade

echo "Updated apt"

apt install python3 -y

apt install python3-pip -y

echo "Instaled python"

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

echo "Installed docker"
