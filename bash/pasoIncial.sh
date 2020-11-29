#!/bin/bash
# -*- ENCODING: UTF-8 -*-

sudo apt-get update
sudo apt-get install python3-boto3

if [ -d "proyectoFinalBI"  ] 
then
	cd proyectoFinalBI
	git pull
else
	git clone https://github.com/JGcarvajal/proyectoFinalBI.git
	cd proyectoFinalBI
fi

python3 Consultar_datos.py
