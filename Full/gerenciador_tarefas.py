# Importação de bibliotecas necessárias
import os  # Para verificar a existência do arquivo
import json  # Para salvar as tarefas em formato estruturado
from datetime import datetime

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
    """Carrega as tarefas salvas no arquivo JSON."""
    if not os.path.exists(arquivo_tarefas):
        return []
    with open(arquivo_tarefas, "r", encoding="utf-8") as file:
        return json.load(file)


def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON."""
    with open(arquivo_tarefas, "w", encoding="utf-8") as file:
        json.dump(tarefas, file, indent=4, ensure_ascii=False)


def obter_duracao_tarefa():
    """Solicita ao usuário a duração da tarefa no formato hh:mm."""
    while True:
        duracao = input("Insira a duração da tarefa (hh:mm): ")
        try:
            horas, minutos = map(int, duracao.split(':'))
            if minutos < 0 or minutos > 59:
                raise ValueError
            return horas, minutos
        except ValueError:
            print("⚠️ Formato inválido. Insira a duração no formato hh:mm (ex: 01:30).")


def validar_data():
    """Solicita uma data ao usuário e valida se é futura e no formato correto."""
    while True:
        data_inserida = input("Data de conclusão (dd/mm/yyyy): ")
        try:
            data_formatada = datetime.strptime(data_inserida, "%d/%m/%Y")
            if data_formatada < datetime.now():
                print("🚫 Data inválida. Insira uma data futura.")
            else:
                return data_inserida
        except ValueError:
            print("⚠️ Formato inválido. Insira a data no formato dd/mm/yyyy.")


def adicionar_tarefa():
    """Permite que o usuário adicione uma nova tarefa."""
    descricao = input("Digite a nova tarefa: ")

    horas, minutos = obter_duracao_tarefa()
    duracao_total = horas * 60 + minutos

    while True:
        prioridade = input("Defina a prioridade (Alta, Média, Baixa): ").capitalize()
        if prioridade in opcoes_prioridade:
            break
        print("⚠️ Prioridade inválida. Escolha entre: Alta, Média ou Baixa.")

    data_conclusao = validar_data()

    tarefas = carregar_tarefas()
    nova_tarefa = {
        "descricao": descricao,
        "tempo_estimado": duracao_total,
        "prioridade": prioridade,
        "data_conclusao": data_conclusao
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print("✅ Tarefa adicionada com sucesso!")
    print(f'Descrição: {descricao} || Duração: {duracao_total} min || Prioridade: {prioridade} || Data: {data_conclusao}')


def listar_tarefas_prioridade():
    """Lista todas as tarefas ordenadas por prioridade."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("📂 Nenhuma tarefa encontrada.")
        return

    tarefas_ordenadas = sorted(tarefas, key=lambda x: prioridades[x["prioridade"]], reverse=True)
    
    print("\n📌 Lista de Tarefas (Ordenadas por Prioridade):")
    for i, tarefa in enumerate(tarefas_ordenadas, 1):
        horas, minutos = divmod(tarefa['tempo_estimado'], 60)
        print(f"{i}. {tarefa['descricao']} - 🕒 {horas}h {minutos}m - 🔥 {tarefa['prioridade']}")


def listar_tarefas_date():
    """Lista todas as tarefas ordenadas por data de conclusão."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("📂 Nenhuma tarefa encontrada.")
        return

    tarefas_ordenadas = sorted(tarefas, key=lambda x: datetime.strptime(x["data_conclusao"], "%d/%m/%Y"))
    
    print("\n📌 Lista de Tarefas (Ordenadas por Data):")
    for i, tarefa in enumerate(tarefas_ordenadas, 1):
        horas, minutos = divmod(tarefa['tempo_estimado'], 60)
        print(f"{i}. {tarefa['descricao']} - 🕒 {horas}h {minutos}m - 📅 {tarefa['data_conclusao']}")


def remover_tarefa():
    """Permite que o usuário remova uma tarefa pelo número correspondente."""
    tarefas = carregar_tarefas()
    listar_tarefas_prioridade()

    if not tarefas:
        return

    while True:
        try:
            num_tarefa = int(input("\nDigite o número da tarefa a remover: "))
            if 1 <= num_tarefa <= len(tarefas):
                tarefa_removida = tarefas.pop(num_tarefa - 1)
                salvar_tarefas(tarefas)
                print(f"🗑️ Tarefa {tarefa_removida['descricao']} removida com sucesso!")
                break
            else:
                print("❌ Número inválido. Tente novamente.")
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número válido.")


def visualizar_estatisticas():
    """Exibe estatísticas sobre as tarefas cadastradas."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("📊 Nenhuma estatística disponível.")
        return

    total_tarefas = len(tarefas)
    tempo_total = sum(tarefa["tempo_estimado"] for tarefa in tarefas)
    prioridades_unicas = set(tarefa["prioridade"] for tarefa in tarefas)

    print("\n📊 Estatísticas das Tarefas:")
    print(f"📌 Total de tarefas: {total_tarefas}")
    print(f"🕒 Tempo total estimado: {tempo_total // 60}h {tempo_total % 60}m")
    print(f"🔥 Prioridades presentes: {', '.join(prioridades_unicas)}")


def menu():
    """Exibe um menu interativo para o usuário."""
    while True:
        print("\n📌 GERENCIADOR DE TAREFAS")
        print("1️⃣ Adicionar Tarefa")
        print("2️⃣ Listar Tarefas por Prioridade")
        print("3️⃣ Listar Tarefas por Data")
        print("4️⃣ Remover Tarefa")
        print("5️⃣ Visualizar Estatísticas")
        print("6️⃣ Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa()
        elif opcao == "2":
            listar_tarefas_prioridade()
        elif opcao == "3":
            listar_tarefas_date()
        elif opcao == "4":
            remover_tarefa()
        elif opcao == "5":
            visualizar_estatisticas()
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")


# Inicia o programa
menu()
