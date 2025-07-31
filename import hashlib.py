import hashlib
import requests 

#--- Função para obter os hashes vazados do API do HIBP---
def obter_hashes_vazados(prefixo_hash):
    """
    Faz uma requisição à API do HIBP para obter hashes que começam com o prefixo_hash fornecido.

    Args:
        prefixo_hash (str): Os primeiros 5 caracteres do hash SHA-1 da senha.
    
    Returns:
      dict: Um dicionário onde as chaves são os hashes vazados (o restante do hash) e os 
      valores são a contagem de vezes que apareceram os vazamentos.
      Retorna um dicionário vazio se houver um erro ou nenhum hash encontrado.

    """
url = f"https://api.pwnedpasswords.com/range/{prefixo_hash}"
try:
    #Faz a requisição GET para a API
    resposta = requests.get(url, timeout=5) #timeout para evitar que a requisição demore muito

   #Verifica se a requisião foi bem-sucedida (código de status 200)
   resposta.raise_for_status() # Lança uma exceção para códigos de status de erro HTTP

hashes_e_contagens = {}
#A resposta da API vem como uma string com hashes e contagens, um por linha
for linha in resposta.text.splitlines():
    partes = linha.split(':')
    if len(partes) == 2:
        #O HIBP retorna o restante do hash (depois dos 5 primeiros caracteres)
        #e a contagem de vezes que ele apareceu.
        hash_restante = partes[0]
        contagem = int(partes[1])
        hashes_e_contagens[hash_restante] = contagem
return hashes_e_contagens

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro ao conectar à API do HIBP: {e}")
    return {}
except ValueError:
    print("Erro ao processar a resposta da API (formato inesperado).")
    return {}






senha_bytes = senha.encode('uft-8')
