import os
from Bio import Entrez

# Definir o e-mail para uso da API do NCBI
Entrez.email = "thiagomafra@gmail.com"

def download_assembly(accession):
    """
    Função para baixar a sequência genômica de uma montagem pelo identificador de acesso.
    """
    try:
        # Busca o identificador de montagem
        search_handle = Entrez.esearch(db="assembly", term=accession, retmax="1")
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        # Pega o ID da montagem
        assembly_id = search_results["IdList"][0]
        summary_handle = Entrez.esummary(db="assembly", id=assembly_id)
        summary_results = Entrez.read(summary_handle)
        summary_handle.close()
        
        # URL do ftp para download
        ftp_path = summary_results['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_RefSeq']
        if ftp_path == "":
            ftp_path = summary_results['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_GenBank']
        file_name = os.path.basename(ftp_path)
        link = os.path.join(ftp_path, file_name + "_genomic.fna.gz")
        
        # Usar 'wget' ou uma biblioteca Python para baixar o arquivo
        os.system(f"wget -P downloads {link}")
        return f"Arquivo baixado em downloads/{file_name}_genomic.fna.gz"
    except Exception as e:
        print(f"Erro ao baixar a sequência {accession}: {e}")
        return None

# Cria o diretório se não existir
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Suponha que você tem uma lista de identificadores em um arquivo chamado 'accessions.txt'
with open("accessions.txt", "r") as file:
    accessions = file.read().strip().split()

# Baixando as montagens
for accession in accessions:
    result = download_assembly(accession)
    if result:
        print(result)
