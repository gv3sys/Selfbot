#!/bin/bash

# Detectar la distribución de Linux
if [ -f /etc/os-release ]; then
    source /etc/os-release
    DISTRO=$ID
elif [ -f /etc/lsb-release ]; then
    DISTRO=$(lsb_release -si)
else
    DISTRO="Unknown"
fi

# Verificar si Python está instalado
python --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Python ya está instalado en tu sistema."
else
    echo "Python no está instalado en tu sistema."

    # Instalar Python según la distribución
    case $DISTRO in
        "ubuntu" | "debian")
            echo "Puedes instalar Python en Ubuntu/Debian con: sudo apt-get install python"
            ;;
        "fedora")
            echo "Puedes instalar Python en Fedora con: sudo dnf install python"
            ;;
        "centos" | "rhel")
            echo "Puedes instalar Python en CentOS/RHEL con: sudo yum install python"
            ;;
        *)
            echo "No se pudo determinar cómo instalar Python en tu sistema. Por favor, instálalo manualmente."
            ;;
    esac

    exit 1
fi

# Instalar dependencias
echo "Instalando las dependencias..."
pip install -r requirements.txt

# Limpiar la pantalla
clear

# Mostrar instrucciones finales
echo "Ahora ejecuta 'run.sh' para iniciar el Selfbot."
