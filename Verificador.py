import hashlib
import requests

# Função para obter os hashes vazados da API do HIBP
def obter_hashes_vazados(prefixo_hash):
    """
    Faz uma requisição à API do HIBP para obter hashes que começam
    com o prefixo_hash fornecido.

    Esta versão lê a resposta em streaming para evitar timeouts com
    senhas muito comuns.
    """
    url = f"https://api.pwnedpasswords.com/range/{prefixo_hash}"
    try:
 
        with requests.get(url, stream=True, timeout=30) as resposta:
            resposta.raise_for_status()

            hashes_e_contagens = {}
            linha_contador = 0
            # A resposta da API vem como uma string com hashes e contagens, um por linha
            for linha in resposta.iter_lines(decode_unicode=True):
                # Se o número de linhas exceder um limite, a senha é muito comum
                linha_contador += 1
                if linha_contador > 1000:

                    return {'TOO_COMMON': 1}
                
                partes = linha.split(':')
                if len(partes) == 2:
                    hash_restante = partes[0]
                    contagem = int(partes[1])
                    hashes_e_contagens[hash_restante] = contagem
            return hashes_e_contagens

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu uma exceção de requisição: {type(e).__name__} - {e}")
        return {}
    except ValueError as e:
        print(f"Ocorreu um erro ao processar a resposta da API: {e}")
        return {}


# Função para verificar a senha
def verificar_senha_vazada(senha):
    """
    Verifica se uma senha foi encontrada em vazamentos usando a API do HIBP.
    """
    senha_bytes = senha.encode('utf-8')
    hash_sha1 = hashlib.sha1(senha_bytes).hexdigest().upper()
    prefixo_hash = hash_sha1[:5]
    
    print(f"Prefix hash: {prefixo_hash}") 
    
    hash_restante = hash_sha1[5:]

    hashes_vazados = obter_hashes_vazados(prefixo_hash)
    
    foi_vazada = False  # NOVA VARIÁVEL

    if 'TOO_COMMON' in hashes_vazados:
        # Mesmo se for muito comum, verificamos se está na lista recebida
        if hash_restante in hashes_vazados:
            foi_vazada = True
        return -2, foi_vazada  # Retorna também a info de vazamento
    
    if hash_restante in hashes_vazados:
        foi_vazada = True
        contagem = hashes_vazados[hash_restante]
        return contagem, foi_vazada
    else:
        return 0, foi_vazada

# Código principal (onde você usa as funções) 
    print("--- Verificador de Senhas Vazadas ---")
    print("Este programa verifica se sua senha foi exposta em vazamentos de dados.")
    print("Sua senha completa NUNCA é enviada para o serviço externo, apenas uma parte do hash.")
    print("-" * 35)

    while True:
        senha_para_verificar = input("Digite a senha que você quer verificar (ou 'sair' para terminar): ")

        if senha_para_verificar.lower() == 'sair':
            print("Saindo do verificador. Até mais!")
            break

        if not senha_para_verificar:
            print("Por favor, digite uma senha para verificar.")
            continue

        print(f"\nVerificando a senha: '{senha_para_verificar}'...")
        resultado = verificar_senha_vazada(senha_para_verificar)

        if resultado == -2:
            print("\n⚠️ AVISO! Esta senha é EXTREMAMENTE comum.")
            if foi_vazada:
                print("Além disso, ELA JÁ FOI ENCONTRADA EM VAZAMENTOS!")
            print("É ALTAMENTE RECOMENDADO que você MUDE esta senha IMEDIATAMENTE.")
        elif resultado > 0:
            print(f"\n🚨 ATENÇÃO! Esta senha foi encontrada em {resultado} vazamento(s) de dados.")
            print("É ALTAMENTE RECOMENDADO que você MUDE esta senha IMEDIATAMENTE em todos os lugares onde a utiliza.")
        elif resultado == 0:
            print("\n✅ Boa notícia! Esta senha NÃO foi encontrada nos vazamentos de dados conhecidos.")
            print("Isso não garante 100% de segurança, mas é um bom sinal.")
        else:
            print("\n❌ Não foi possível verificar a senha devido a um erro. Tente novamente mais tarde.")

        print("\n" + "-" * 35)