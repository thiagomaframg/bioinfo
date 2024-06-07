#!/usr/bin/env python3
import os
import subprocess

# Caminho para o diretório onde estão os arquivos .fna
path_to_fna_files = "./"

# Caminho para o diretório onde você quer salvar os resultados do BUSCO
output_dir = "./busco_outputs"

# Linhagem BUSCO a ser usada
busco_lineage = "saccharomycetes"

# Caminho para onde o BUSCO deve baixar suas bases de dados
download_path = "/data/busco_downloads/"

# Verifique e crie o diretório de saída se ele não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Verifique e crie o diretório para o download das bases de dados se ele não existir
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Lista todos os arquivos .fna no diretório especificado
for filename in os.listdir(path_to_fna_files):
    if filename.endswith(".fna"):
        # Extrai o identificador até o segundo underscore
        parts = filename.split('_')
        genome_id = '_'.join(parts[:2])

        # Monta o caminho completo para o arquivo
        file_path = os.path.join(path_to_fna_files, filename)

        # Define o diretório de saída para este genoma
        specific_output_dir = os.path.join(output_dir, genome_id)

        # Comando BUSCO
        busco_command = [
            "busco",
            "-i", file_path,
            "-o", genome_id,  # Busco usa o nome do diretório de saída como parte do identificador
            "-m", "genome",
            "-l", busco_lineage,
            "--cpu", "64",  # Usa 64 CPUs
            "--offline",  # Executa em modo offline
            "--download_path", download_path,  # Define o caminho de download para as bases de dados do BUSCO
            "--out_path", output_dir  # Especifica o diretório principal de saída para o resultado do BUSCO
        ]

        # Executa o BUSCO
        print(f"Rodando BUSCO para {genome_id}...")
        subprocess.run(busco_command)
        print(f"BUSCO completo para {genome_id}.")

print("BUSCO executado para todos os genomas.")

