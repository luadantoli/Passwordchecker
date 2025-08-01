# Passwordchecker
🔎 Verificador de Senhas Vazadas

Para criar esse verificador, utilizei uma API pública e segura para isso, a "Have I Been Pwned" (HIBP).

# O que é o "Have I Been Pwned" (HIBP)?
O HIBP é um serviço criado por Troy Hunt que agrega bilhões de senhas que foram expostas em vazamentos de dados conhecidos. Ele permite que você verifique se suas senhas (ou partes delas) apareceram em algum desses vazamentos sem precisar enviar a senha completa, o que é um ponto crucial de segurança e privacidade.

# Como funciona a verificação?
A API do HIBP utiliza um método chamado k-Anonymity para verificar senhas. Basicamente, você envia os primeiros 5 caracteres do hash SHA-1 da sua senha, e a API retorna uma lista de todos os hashes SHA-1 que começam com esses mesmos 5 caracteres, junto com a frequência com que apareceram em vazamentos.

Se sua senha estiver na lista retornada, significa que ela foi vazada. O restante do hash da sua senha é então comparado localmente com os hashes retornados, garantindo que sua senha completa nunca seja transmitida.

# O que é um hash?
É o resultado da aplicação de uma função hash, que transforma uma entrada (como um texto, arquivo, senha, etc.) em uma sequência fixa de caracteres, geralmente em formato hexadecimal, é como um "resumo digital" de qualquer informação. Armazena senhas de forma protegida (sem guardar a senha real).

✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧✧⋄⋆⋅⋆⋄✧⋄⋆⋅⋆⋄✧

_Durante a execução do código tive que quebrar cabeça e recorrer a ajuda de duas IAs, as senhas comuns como "123456" ou "senha123" davam o erro "❌ Não foi possível verificar a senha devido a um erro, Tente novamente mais tarde." ao invés de considerar que era uma senha comum e/ou que foram vazadas, e testando esse código no Google Colab, todas as senhas, até mesmo as mais complexas com infinitos símbolos, davam "senha comum" como resultado._

_Ainda não sei como resolver isso, pode ser só as minhas configurações de segurança, mas vou correr atrás de ter a resposta correta com senhas comuns e vazadas._
