# Importação de bibliotecas necessárias
import os  # Para verificar a existência do arquivo
import json  # Para salvar as tarefas em formato estruturado

# Nome do arquivo onde as tarefas serão armazenadas
arquivo_tarefas = "tarefas.json"

# Dicionário que mapeia níveis de prioridade a números para ordenação
prioridades = {
    "Alta": 3,
    "Média": 2,
    "Baixa": 1
}

# Tupla com opções válidas de prioridade
opcoes_prioridade = ("Alta", "Média", "Baixa")


def carregar_tarefas():
    """
    Carrega as tarefas salvas no arquivo JSON.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    if not os.path.exists(arquivo_tarefas):  # Verifica se o arquivo existe
        return []  # Retorna uma lista vazia se o arquivo não existir

    with open(arquivo_tarefas, "r", encoding="utf-8") as file:
        return json.load(file)  # Lê o arquivo JSON e retorna a lista de tarefas


def salvar_tarefas(tarefas):
    """
    Salva a lista de tarefas no arquivo JSON.
    """
    with open(arquivo_tarefas, "w", encoding="utf-8") as file:
        json.dump(tarefas, file, indent=4, ensure_ascii=False)  # Salva em formato legível


def adicionar_tarefa():
    """
    Permite que o usuário adicione uma nova tarefa com descrição e prioridade.
    """
    descricao = input("Digite a nova tarefa: ")  # Solicita a descrição da tarefa

    # Definição do tipo de dado 'float' para o tempo estimado
    while True:
        user_input = input("Tempo estimado para completar (ex: 1.5 -> 1 hora e 30 min): ")

        # Verifica se a entrada está vazia
        if user_input.strip() == "":
            print("Por favor, insira um valor válido.")
            continue  # Repete o loop se a entrada estiver vazia

        try:
            # Tenta converter a entrada para um float
            tempo_estimado = float(user_input)
            break  # Sai do loop se a conversão for bem-sucedida
        except ValueError:
            print("Por favor, insira um valor válido.")  # Mensagem de erro se a conversão falhar

    # Agora você pode usar tempo_estimado como um float válido
    print(f"Tempo estimado: {tempo_estimado} horas")

    # Loop para definir a prioridade da tarefa
    while True:
        prioridade = input("Defina a prioridade (Alta, Média, Baixa): ").capitalize()
        if prioridade in opcoes_prioridade:  # Verifica se a prioridade é válida
            break
        print("Prioridade inválida. Escolha entre: Alta, Média ou Baixa.")

    tarefas = carregar_tarefas()  # Carrega as tarefas existentes
    # Dicionário => key : value
    nova_tarefa = {
        "descricao": descricao,
        "tempo_estimado": tempo_estimado,
        "prioridade": prioridade,
        "data_conclusao": data
    }

    tarefas.append(nova_tarefa)  # Adiciona a nova tarefa à lista
    salvar_tarefas(tarefas)  # Salva as tarefas atualizadas no arquivo
    print("✅ Tarefa adicionada com sucesso!")


def listar_tarefas_prioridade():
    """
    Lista todas as tarefas salvas no arquivo, ordenadas por prioridade.
    """
    tarefas = carregar_tarefas()  # Carrega as tarefas

    if not tarefas:  # Verifica se não há tarefas
        print("📂 Nenhuma tarefa encontrada.")
        return

    # Ordenando as tarefas por prioridade usando dicionário de mapeamento
    tarefas_ordenadas = sorted(tarefas, key=lambda x: prioridades[x["prioridade"]], reverse=True)

    print("\n📌 Lista de Tarefas (Ordenadas por Prioridade):")
    for i, tarefa in enumerate(tarefas_ordenadas, 1):  # Enumera as tarefas
        print(f"{i}. {tarefa['descricao']} - 🕒 {tarefa['tempo_estimado']}h - 🔥 Prioridade: {tarefa['prioridade']}")

def listar_tarefas_date():
    tarefas = carregar_tarefas()  # Carrega as tarefas

    if not tarefas: 
        print("📂 Nenhuma tarefa encontrada")
        return

def remover_tarefa():
    """
    Permite que o usuário remova uma tarefa pelo número correspondente.
    """
    tarefas = carregar_tarefas()  # Carrega as tarefas
    listar_tarefas_prioridade()  # Lista as tarefas

    if not tarefas:  # Verifica se não há tarefas
        return

    try:
        num_tarefa = int(input("\nDigite o número da tarefa a remover: "))  # Solicita o número da tarefa a ser removida
        if 1 <= num_tarefa <= len(tarefas):  # Verifica se o número está dentro do intervalo válido
            tarefa_removida = tarefas.pop(num_tarefa - 1)  # Remove a tarefa selecionada
            salvar_tarefas(tarefas)  # Atualiza o arquivo com a lista de tarefas
            print(f"🗑️ Tarefa '{tarefa_removida['descricao']}' removida com sucesso!")  # Confirma a remoção
        else:
            print("❌ Número inválido. Tente novamente.")  # Mensagem de erro se o número for inválido
    except ValueError:
        print("⚠️ Entrada inválida. Digite um número válido.")  # Mensagem de erro se a entrada não for um número


def visualizar_estatisticas():
    """
    Exibe estatísticas sobre as tarefas cadastradas.
    """
    tarefas = carregar_tarefas()  # Carrega as tarefas
    if not tarefas:  # Verifica se não há tarefas
        print("📊 Nenhuma estatística disponível, pois não há tarefas cadastradas.")
        return

    total_tarefas = len(tarefas)  # Conta o total de tarefas
    tempo_total = sum(tarefa["tempo_estimado"] for tarefa in tarefas)  # Soma o tempo estimado de todas as tarefas
    prioridades_unicas = set(tarefa["prioridade"] for tarefa in tarefas)  # Coleta as prioridades únicas

    print("\n📊 Estatísticas das Tarefas:")
    print(f"📌 Total de tarefas: {total_tarefas}")  # Exibe o total de tarefas
    print(f"🕒 Tempo total estimado: {tempo_total:.2f} horas")  # Exibe o tempo total estimado
    print(f"🔥 Prioridades presentes: {', '.join(prioridades_unicas)}")  # Exibe as prioridades únicas

def menu_listagem():
    while True:
        print("\n📝 Menu de Listagem de Tarefas:")
        print("1️⃣ Listar tarefas por prioridade")
        print("2️⃣ Listar tarefas por data de entrega")

        opcao_prioridade = input("Escolha uma opção: ")
        if opcao_prioridade == "1":
            listar_tarefas_prioridade()
        elif opcao_prioridade == "2":
            listar_tarefas_date()
        else: 
            print("⚠️ Opção inválida. Tente novamente.")  # Mensagem de erro se a opção for inválida


def menu():
    """
    Exibe um menu interativo para o usuário escolher ações.
    """
    while True:
        print("\n📌 GERENCIADOR DE TAREFAS")  # Título do menu
        print("1️⃣ Adicionar Tarefa")  # Opção para adicionar tarefa
        print("2️⃣ Listar Tarefas")  # Opção para listar tarefas
        print("3️⃣ Remover Tarefa")  # Opção para remover tarefa
        print("4️⃣ Visualizar Estatísticas")  # Opção para visualizar estatísticas
        print("5️⃣ Sair")  # Opção para sair do programa

        opcao = input("Escolha uma opção: ")  # Solicita a escolha do usuário

        if opcao == "1":
            adicionar_tarefa()  # Chama a função para adicionar tarefa
        elif opcao == "2":
            menu_listagem()  # Chama a função para listar tarefas
        elif opcao == "3":
            remover_tarefa()  # Chama a função para remover tarefa
        elif opcao == "4":
            visualizar_estatisticas()  # Chama a função para visualizar estatísticas
        elif opcao == "5":
            print("👋 Saindo do programa...")  # Mensagem de saída
            break  # Encerra o loop e finaliza o programa
        else:
            print("⚠️ Opção inválida. Tente novamente.")  # Mensagem de erro se a opção for inválida


# Chama a função principal para iniciar o programa
menu()