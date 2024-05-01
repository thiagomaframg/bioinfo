import sys

def main(input_file):
    """
    Este script lê um arquivo FASTA multifasta, processa cada entrada, extrai informações de cabeçalho e sequência,
    e organiza essas informações em um dicionário para escrever duas saídas: um arquivo FASTA concatenado e um
    arquivo de partição.

    Args:
    input_file (str): Caminho para o arquivo de entrada que contém dados das proteínas.
                      O arquivo deve ser um arquivo multifasta com cabeçalhos no formato ">rep1__Sp_boni",
                      onde 'rep1' é o nome do gene e 'Sp_boni' é o ID da espécie.

    O script produz dois arquivos de saída:
    - "concatenated_output.fasta": Contém todas as sequências, concatenadas e etiquetadas por espécie.
    - "partition_output.txt": Contém informações de partição úteis para análises filogenéticas, geradas apenas na
      primeira iteração completa das sequências.
    """
    with open(input_file, 'r') as file:
        content = file.read().strip().split(">")[1:]  # Lê o arquivo e divide as entradas

    hash = {}

    for entry in content:
        lines = entry.strip().split("\n")
        header = lines[0]
        seq = ''.join(lines[1:]).replace('\n', '')  # Remove quebras de linha da sequência
        header_parts = header.split("__")
        header2_parts = header_parts[1].split()
        if header2_parts[0] not in hash:
            hash[header2_parts[0]] = {}
        hash[header2_parts[0]][header_parts[0]] = seq

    with open("concatenated_output.fasta", "w") as out, open("partition_output.txt", "w") as out2:
        count = 1
        length = 1
        control = False

        for organism in hash:
            out.write(f">{organism}\n")
            for protein in sorted(hash[organism]):
                out.write(hash[organism][protein])
                if not control:
                    prot_length = length + len(hash[organism][protein]) - 1
                    out2.write(f"AUTO,gene{count}={length}-{prot_length}\n")
                    length = prot_length + 1
                    count += 1
            out.write("\n")
            control = True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
