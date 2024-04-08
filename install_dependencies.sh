#!/bin/bash

# Atualiza os repositórios de pacotes
sudo apt-get update

# Instala dependências do sistema
sudo apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    libpq-dev \
    libjpeg-dev \
    libjpeg8-dev \
    libtiff5-dev \
    libx11-6 \
    libx11-dev \
    zlib1g-dev \
    libpng-dev \
    libltdl7 \
    libltdl-dev \
    libstdc++6 \
    libc6 \
    libncurses5 \
    libstdc++ \
    libgtk2.0-0 \
    libgtk2.0-dev \
    git \
    openjdk-8-jdk \
    autoconf \
    automake \
    libtool \
    pkg-config

# Conclui a instalação
echo "Instalação de dependências concluída."
