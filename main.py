from src.gerenciador import GerenciadorTarefas

def exibir_menu():
    print("\n=== GERENCIADOR DE TAREFAS ACADÊMICAS ===")
    print("1 - Criar tarefa")
    print("2 - Listar tarefas")
    print("3 - Buscar tarefa por ID")
    print("4 - Editar tarefa")
    print("5 - Remover tarefa")
    print("6 - Concluir tarefa")
    print("7 - Filtrar por disciplina")
    print("8 - Filtrar por prioridade")
    print("9 - Filtrar por status")
    print("0 - Sair")


def main():
    gerenciador = GerenciadorTarefas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                titulo = input("Título: ")
                disciplina = input("Disciplina: ")
                descricao = input("Descrição: ")
                prioridade = input("Prioridade (baixa/media/alta): ")
                prazo = input("Prazo: ")

                id_tarefa = gerenciador.criar_tarefa(
                    titulo, disciplina, descricao, prioridade, prazo
                )
                print(f"Tarefa criada com ID: {id_tarefa}")

            elif opcao == "2":
                tarefas = gerenciador.listar_tarefas()
                for id_tarefa, tarefa in tarefas.items():
                    print(id_tarefa, tarefa)

            elif opcao == "3":
                id_tarefa = int(input("ID da tarefa: "))
                tarefa = gerenciador.buscar_tarefa(id_tarefa)
                print(tarefa)

            elif opcao == "4":
                id_tarefa = int(input("ID da tarefa: "))
                titulo = input("Novo título (enter para manter): ")
                disciplina = input("Nova disciplina (enter para manter): ")
                descricao = input("Nova descrição (enter para manter): ")
                prioridade = input("Nova prioridade (baixa/media/alta): ")
                prazo = input("Novo prazo: ")

                gerenciador.editar_tarefa(
                    id_tarefa,
                    titulo or None,
                    disciplina or None,
                    descricao or None,
                    prioridade or None,
                    prazo or None
                )
                print("Tarefa atualizada")

            elif opcao == "5":
                id_tarefa = int(input("ID da tarefa: "))
                confirmacao = input("Tem certeza que deseja remover? (s/n): ")

                if confirmacao.lower() == "s":
                    gerenciador.remover_tarefa(id_tarefa)
                    print("Tarefa removida")

            elif opcao == "6":
                id_tarefa = int(input("ID da tarefa: "))
                gerenciador.concluir_tarefa(id_tarefa)
                print("Tarefa concluída")

            elif opcao == "7":
                disciplina = input("Disciplina: ")
                tarefas = gerenciador.filtrar_por_disciplina(disciplina)
                print(tarefas)

            elif opcao == "8":
                prioridade = input("Prioridade (baixa/media/alta): ")
                tarefas = gerenciador.filtrar_por_prioridade(prioridade)
                print(tarefas)

            elif opcao == "9":
                status = input("Status (pendente/em andamento/concluida): ")
                tarefas = gerenciador.filtrar_por_status(status)
                print(tarefas)

            elif opcao == "0":
                print("Encerrando sistema...")
                break

            else:
                print("Opção inválida")

        except ValueError as e:
            print(f"Erro: {e}")
        except Exception:
            print("Erro inesperado")


if __name__ == "__main__":
    main()