# Banco de Dados Avançado - Sistema de Avaliação de Restaurantes 
# Autor: Anderson Ramos

from pymongo import MongoClient
from pprint import pprint
import time 

# Comandos para conectar com o servidor local, banco de dados "restaurante_db",
database = MongoClient('localhost', 27017)
base = database['restaurante_db']
colecao = base['restaurantes']

# 1 - Incluir novo restaurante
def criar_documento(dados):
    try:
        # Validação básica da estrutura
        campos_obrigatorios = ["nome", "endereco", "categoria", "avaliacoes"]   
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        if not isinstance(dados["avaliacoes"], list):
            raise ValueError("O campo 'avaliacoes' deve ser uma lista.")

        for avaliacao in dados["avaliacoes"]:
            if not all(k in avaliacao for k in ["cliente", "nota", "comentario"]):
                raise ValueError("Cada avaliação deve conter 'cliente', 'nota' e 'comentario'.")

        # Inserção no banco
        resultado = colecao.insert_one(dados)
        return {
            "status": "sucesso",
            "mensagem": f'Documento inserido com id: {resultado.inserted_id}'
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }

# 2 - Consultar todos os restaurantes
def ler_documentos():
    documentos = list(colecao.find())
    if not documentos:
        print("\nNenhum restaurante cadastrado.")
    else:
        print("\n=== Restaurantes Cadastrados ===\n")
        for idx, doc in enumerate(documentos, start=1):
            print(f"Restaurante #{idx}")
            print(f"📝 Nome     : {doc.get('nome', 'N/A')}")
            print(f"📍 Endereço : {doc.get('endereco', 'N/A')}")
            print(f"🍽️ Categoria: {doc.get('categoria', 'N/A')}")
            
            avaliacoes = doc.get("avaliacoes", [])
            if avaliacoes:
                print("⭐ Avaliações:")
                for i, av in enumerate(avaliacoes, start=1):
                    print(f"  {i}. Cliente   : {av.get('cliente', 'N/A')}")
                    print(f"     Nota      : {av.get('nota', 'N/A')}/5")
                    print(f"     Comentário: {av.get('comentario', 'N/A')}")
            else:
                print("⭐ Avaliações: Nenhuma avaliação registrada.")
            
            print("-" * 40)

# 3 - Alterar dados de restaurante
def alterar_restaurante():
    nome = input("Informe o nome do restaurante: ").strip()
    
    restaurante = colecao.find_one({"nome": nome})
    if not restaurante:
        print(f"Nenhum restaurante encontrado com o nome '{nome}'.")
        return

    novos_dados = {}

    if input("Deseja alterar o nome? [Sim/Não]: ").strip().lower() == "sim":
        novo_nome = input("Informe o novo nome: ").strip()
        if novo_nome:
            novos_dados["nome"] = novo_nome

    if input("Deseja alterar o endereço? [Sim/Não]: ").strip().lower() == "sim":
        novo_endereco = input("Informe o novo endereço: ").strip()
        if novo_endereco:
            novos_dados["endereco"] = novo_endereco

    if input("Deseja alterar a categoria? [Sim/Não]: ").strip().lower() == "sim":
        nova_categoria = input("Informe a nova categoria: ").strip()
        if nova_categoria:
            novos_dados["categoria"] = nova_categoria

    if novos_dados:
        resultado = colecao.update_one({"nome": nome}, {"$set": novos_dados})
        if resultado.modified_count > 0:
            print("✅ Restaurante atualizado com sucesso!")
        else:
            print("⚠️ Nenhuma modificação foi realizada (os dados podem ser os mesmos).")
    else:
        print("Nenhuma alteração realizada.")


# 4 - Excluir restaurante
def excluir_restaurante():
    nome = input("Informe o nome do restaurante: ").strip()
    resultado = colecao.delete_one({"nome": nome})
    print(f"Restaurantes excluídos: {resultado.deleted_count}")

# 5 - Incluir avaliação
def incluir_avaliacao():
    nome = input("Informe o nome do restaurante: ").strip()

    # Verifica se o restaurante existe antes de prosseguir
    restaurante_existente = colecao.find_one({"nome": nome})
    if not restaurante_existente:
        print(f"Restaurante '{nome}' não encontrado. Não foi possível adicionar a avaliação.")
        return # Sai da função se o restaurante não existir

    cliente = input("Informe o nome do cliente: ").strip()

    while True:
        try:
            nota = float(input("Nota (0 a 5): "))
            if 0 <= nota <= 5:
                break
            else:
                print("A nota deve estar entre 0 e 5. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número para a nota.")

    comentario = input("Comentário: ")
    avaliacao = {"cliente": cliente, "nota": nota, "comentario": comentario}
    resultado = colecao.update_one({"nome": nome}, {"$push": {"avaliacoes": avaliacao}})

    if resultado.modified_count > 0:
        print(f"Avaliação adicionada com sucesso ao restaurante '{nome}'.")
    else:
        print("Não foi possível adicionar a avaliação. Ocorreu um erro ou o restaurante não foi encontrado (embora já tenhamos verificado).")

# 6 - Consultar avaliações
def consultar_avaliacoes():
    nome = input("Informe o nome do restaurante: ").strip()
    restaurante = colecao.find_one({"nome": nome})

    if restaurante:
        print(f"\n=== Avaliações do restaurante '{nome}' ===\n")
        print(f"📝 Nome     : {restaurante.get('nome', 'N/A')}")
        print(f"📍 Endereço : {restaurante.get('endereco', 'N/A')}")
        print(f"🍽️ Categoria: {restaurante.get('categoria', 'N/A')}")
        
        avaliacoes = restaurante.get("avaliacoes", [])
        if avaliacoes:
            print("\n 😎 Avaliações:")
            for i, av in enumerate(avaliacoes, start=1):
                print(f"  {i}. Cliente   : {av.get('cliente', 'N/A')}")
                print(f"     Nota      : {av.get('nota', 'N/A')}/5")
                print(f"     Comentário: {av.get('comentario', 'N/A')}")
        else:
            print("⭐ Avaliações: Nenhuma avaliação registrada.")
    else:
        print("❌ Restaurante não encontrado.")

# 7 - Alterar avaliação
def alterar_avaliacao():
    nome = input("Informe o nome do restaurante: ").strip()
    cliente = input("Nome do cliente da avaliação: ")
    nova_nota = float(input("Nova nota: "))
    novo_comentario = input("Novo comentário: ")

    resultado = colecao.update_one(
        {"nome": nome, "avaliacoes.cliente": cliente},
        {"$set": {"avaliacoes.$.nota": nova_nota, "avaliacoes.$.comentario": novo_comentario}}
    )
    print(f"Avaliações atualizadas: {resultado.modified_count}")

# 8 - Excluir avaliação
def excluir_avaliacao():
    nome = input("Informe o nome do restaurante: ").strip()
    cliente = input("Nome do cliente da avaliação a ser excluída: ")
    resultado = colecao.update_one(
        {"nome": nome},
        {"$pull": {"avaliacoes": {"cliente": cliente}}}
    )
    print(f"Avaliações removidas: {resultado.modified_count}")

# 9 - Média de avaliações por restaurante
def media_avaliacoes():
    restaurantes = colecao.find()
    lista = []
    for r in restaurantes:
        avals = r.get("avaliacoes", [])
        if avals:
            media = sum(a["nota"] for a in avals) / len(avals)
            lista.append((r["nome"], media))
        else:
            lista.append((r["nome"], 0.0))

    lista.sort()
    print("\n📈 Médias das Avaliações por Restaurante:")
    for nome, media in lista:
        print(f"📚 {nome}: {media:.2f} ⭐")

# Interface de Linha de Comando
def menu():
    while True:
        print("\n" + "╔" + "═" * 38 + "╗")
        print("║" + "Menu de Operações".center(38) + "║")
        print("╠" + "═" * 38 + "╣")
        print("║ 1. Incluir novo restaurante          ║")
        print("║ 2. Consultar todos os restaurantes   ║")
        print("║ 3. Alterar dados de um restaurante   ║")
        print("║ 4. Excluir um restaurante específico ║")
        print("╠" + "─" * 38 + "╣")
        print("║ 5. Incluir uma avaliação             ║")
        print("║ 6. Consultar avaliações              ║")
        print("║ 7. Alterar uma avaliação             ║")
        print("║ 8. Excluir uma avaliação             ║")
        print("╠" + "─" * 38 + "╣")
        print("║ 9. Média das avaliações              ║")
        print("║ 10. Sair                             ║")
        print("╚" + "═" * 38 + "╝\n")

        escolha = input("Escolha uma operação: ").strip()

        if escolha == '1':
            try:
                nome = input("Nome: ")
                endereco = input("Endereço: ")
                categoria = input("Categoria: ")

                avaliacoes = []
                try:
                    num_avaliacoes = int(input("Quantas avaliações deseja adicionar? "))
                except ValueError:
                    print("Número inválido de avaliações.")
                    continue

                for i in range(num_avaliacoes):
                    print(f"\nAvaliação {i+1}:")
                    cliente = input(f"Nome do cliente {i+1}: ")
                    try:
                        nota = float(input(f"Nota do cliente {i+1} (0 a 5): "))
                    except ValueError:
                        print("Nota inválida. Tente novamente.")
                        continue
                    comentario = input(f"Comentário do cliente {i+1}: ")
                    avaliacoes.append({
                        "cliente": cliente,
                        "nota": nota,
                        "comentario": comentario
                    })

                dados = {
                    "nome": nome,
                    "endereco": endereco,
                    "categoria": categoria,
                    "avaliacoes": avaliacoes
                }

                resposta = criar_documento(dados)
                print("\n[INFO] Resultado da inserção:")
                print(resposta["mensagem"])

            except Exception as e:
                print("[ERRO] Falha ao cadastrar restaurante:", e)

        elif escolha == '2':
            ler_documentos()

        elif escolha == '3':
            alterar_restaurante()

        elif escolha == '4':
            excluir_restaurante()

        elif escolha == '5':
            incluir_avaliacao()

        elif escolha == '6':
            consultar_avaliacoes()

        elif escolha == '7':
            alterar_avaliacao()

        elif escolha == '8':
            excluir_avaliacao()

        elif escolha == '9':
            media_avaliacoes()

        elif escolha == '10':
            print("Saindo da aplicação...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Chamando a função menu para iniciar a aplicação
if __name__ == "__main__":
    print("\nConectando ao banco de dados...")
    time.sleep(2)
menu()
