# Importação de bibliotecas necessárias
import os  # Para verificar a existência do arquivo
import json  # Para salvar as tarefas em formato estruturado

# Nome do arquivo onde as tarefas serão armazenadas
arquivo_tarefas = "tarefas.json"

# Dicionário que mapeia níveis de prioridade e números para ordenação
prioridades = {
    "Alta": 3,
    "Média": 2,
    "Baixa": 1
}

# Tupla com opções válidas de prioridade
opcoes_prioridade = ("Alta", "Média", "Baixa")

def carregar_tarefas():
    """Carrega as tarefas salvas no arquivo JSON."""
    # Verifica se o arquivo de tarefas existe
    if not os.path.exists(arquivo_tarefas):
        return []  # Retorna uma lista vazia se o arquivo não existir
    # Abre o arquivo e carrega as tarefas em formato JSON
    with open(arquivo_tarefas, "r", encoding="utf-8") as file:
        return json.load(file)  # Retorna a lista de tarefas

def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON."""
    # Abre o arquivo para escrita e salva as tarefas em formato JSON
    with open(arquivo_tarefas, "w", encoding="utf-8") as file:
        json.dump(tarefas, file, indent=4, ensure_ascii=False)  # Salva as tarefas com formatação

def obter_duracao_tarefa():
    """Solicita ao usuário a duração da tarefa no formato hh:mm."""
    while True:
        duracao = input("Insira a duração da tarefa (hh:mm): ")  # Solicita a duração
        try:
            horas, minutos = map(int, duracao.split(':'))  # Divide a entrada em horas e minutos
            if minutos < 0 or minutos > 59:
                raise ValueError  # Verifica se os minutos estão no intervalo válido
            return horas, minutos  # Retorna as horas e minutos
        except ValueError:
            print("⚠️ Formato inválido. Insira a duração no formato hh:mm (ex: 01:30).")  # Mensagem de erro

def adicionar_tarefa():
    """Permite que o usuário adicione uma nova tarefa."""
    descricao = input("Digite a nova tarefa: ")  # Solicita a descrição da tarefa

    horas, minutos = obter_duracao_tarefa()  # Obtém a duração da tarefa
    duracao_total = horas * 60 + minutos  # Converte a duração total em minutos

    while True:
        prioridade = input("Defina a prioridade (Alta, Média, Baixa): ").capitalize()  # Solicita a prioridade
        if prioridade in opcoes_prioridade:
            break  # Sai do loop se a prioridade for válida
        print("⚠️ Prioridade inválida. Escolha entre: Alta, Média ou Baixa.")  # Mensagem de erro

    tarefas = carregar_tarefas()  # Carrega as tarefas existentes
    nova_tarefa = {
        "descricao": descricao,
        "tempo_estimado": duracao_total,
        "prioridade": prioridade,
    }

    tarefas.append(nova_tarefa)  # Adiciona a nova tarefa à lista
    salvar_tarefas(tarefas)  # Salva a lista atualizada de tarefas
    print("✅ Tarefa adicionada com sucesso!")  # Mensagem de sucesso
    print(f'Descrição: {descricao} || Duração: {duracao_total} min || Prioridade: {prioridade}')  # Exibe detalhes da tarefa

def listar_tarefas_prioridade():
    """Lista todas as tarefas ordenadas por prioridade."""
    tarefas = carregar_tarefas()  # Carrega as tarefas
    if not tarefas:
        print("📂 Nenhuma tarefa encontrada.")  # Mensagem se não houver tarefas
        return

    # Ordena as tarefas pela prioridade
    tarefas_ordenadas = sorted(tarefas, key=lambda x: prioridades[x["prioridade"]], reverse=True)
    
    print("\n📌 Lista de Tarefas (Ordenadas por Prioridade):")
    for i, tarefa in enumerate(tarefas_ordenadas, 1):
        # Converte o tempo estimado em horas e minutos
        horas, minutos = divmod(tarefa['tempo_estimado'], 60)  
        print(f"{i}. {tarefa['descricao']} - 🕒 {horas}h {minutos}m - 🔥 {tarefa['prioridade']}")  # Exibe a tarefa

def remover_tarefa():
    """Permite que o usuário remova uma tarefa pelo número correspondente."""
    tarefas = carregar_tarefas()  # Carrega as tarefas
    listar_tarefas_prioridade()  # Lista as tarefas para o usuário

    if not tarefas:
        return  # Se não houver tarefas, sai da função

    while True:
        try:
            num_tarefa = int(input("\nDigite o número da tarefa a remover: "))  # Solicita o número da tarefa
            if 1 <= num_tarefa <= len(tarefas):
                tarefa_removida = tarefas.pop(num_tarefa - 1)  # Remove a tarefa da lista
                salvar_tarefas(tarefas)  # Salva a lista atualizada
                print(f"🗑️ Tarefa '{tarefa_removida['descricao']}' removida com sucesso!")  # Mensagem de sucesso
                break
            else:
                print("❌ Número inválido. Tente novamente.")  # Mensagem de erro
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número válido.")  # Mensagem de erro

def visualizar_estatisticas():
    """Exibe estatísticas sobre as tarefas cadastradas."""
    tarefas = carregar_tarefas()  # Carrega as tarefas
    if not tarefas:
        print("📊 Nenhuma estatística disponível.")  # Mensagem se não houver tarefas
        return
    
    total_tarefas = len(tarefas)  # Conta o total de tarefas
    tempo_total = sum(tarefa["tempo_estimado"] for tarefa in tarefas)  # Soma o tempo total das tarefas
    media = tempo_total / total_tarefas if total_tarefas > 0 else 0  # Calcula a média de tempo

    print("\n📊 Estatísticas das Tarefas:")
    print(f"📌 Total de tarefas: {total_tarefas}")  # Exibe o total de tarefas
    print(f"🕒 Tempo total estimado: {tempo_total // 60}h {tempo_total % 60}m")  # Exibe o tempo total em horas e minutos
    print(f'Média da carga horária das atividades: {media} minutos')  # Exibe a média de carga horária

def menu():
    """Exibe o menu principal e gerencia as opções do usuário."""
    while True:
        print("\n📌 GERENCIADOR DE TAREFAS")
        print("1️⃣ Adicionar Tarefa")
        print("2️⃣ Listar Tarefas por Prioridade")
        print("3️⃣ Remover Tarefa")
        print("4️⃣ Visualizar Estatísticas")
        print("5️⃣ Sair")
        opcao = input("Escolha uma opção: ")  # Solicita a opção do usuário
        if opcao == "1":
            adicionar_tarefa()  # Chama a função para adicionar tarefa
        elif opcao == "2":
            listar_tarefas_prioridade()  # Chama a função para listar tarefas
        elif opcao == "3":
            remover_tarefa()  # Chama a função para remover tarefa
        elif opcao == "4":
            visualizar_estatisticas()  # Chama a função para visualizar estatísticas
        elif opcao == "5":
            print("Saindo...")  # Mensagem de saída
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")  # Mensagem de erro

# Chama o menu
menu()
