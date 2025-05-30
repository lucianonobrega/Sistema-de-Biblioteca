from time import sleep
from biblioteca import Biblioteca
from datetime import datetime
import os
from rich.console import Console
from rich.align import Align
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def ler_titulo() -> str:
    while True:
        titulo = str(Prompt.ask("[bold white]Título do livro[/bold white]")).title()
        if titulo.strip():
            return titulo
        else:
            console.print("[bold red]Por favor, escreva o título do livro![/bold red]")
            sleep(1)

def ler_autor() -> str:
    while True:
        autor = str(Prompt.ask("[bold white]Nome do autor[/bold white]")).title()
        if autor:
            return autor
        else:
            console.print("[bold red]Por favor, escreva o nome do autor do livro![/bold red]")
            sleep(1)

def ler_ano() -> int:
    while True:
        try:
            ano = int(Prompt.ask("[bold white]Ano de publicação[/bold white]"))
            if 1500 <= ano <= datetime.now().year:
                return ano
            else:
                console.print("[bold red]Ano de publicação inválido. Por favor, tente novamente![/bold red]")
                sleep(1)
        except ValueError:
            console.print("[bold red]Ano de publicação inválido. Por favor, tente novamente![/bold red]")
            sleep(1)

def ler_genero() -> str:
    while True:
        genero = str(Prompt.ask("[bold white]Gênero do livro[/bold white]")).title()
        if genero:
            return genero
        else:
            console.print("[bold red]Por favor, escreva o gênero do livro![/bold red]")

def info_livro() -> tuple[str,str,int,str]:
    while True:
        titulo = ler_titulo()
        autor = ler_autor()
        ano = ler_ano()
        genero = ler_genero()
        while True:
            confirmar = str(Prompt.ask(f"[bold green]-----INFORMAÇÕES DO LIVRO-----[/bold green]\n"
                                  f"[bold white]Título[/bold white]: {titulo}.\n"
                                  f"[bold white]Autor[/bold white]: {autor}.\n"
                                  f"[bold white]Ano[/bold white]: {ano}.\n"
                                  f"[bold white]Gênero[/bold white]: {genero}.\n"
                                  f"[bold white]Deseja confirmar os dados?[/bold white][[bold green]S[/bold green]/[bold red]N[/bold red]]")).lower()
            if confirmar == "s":
                return (titulo, autor, ano, genero)
            elif confirmar == "n":
                console.print("[bold green]Voltando para reinserir dados...[/bold green]")
                sleep(1)
                break
            else:
                console.print("[bold red]Opção inválida. Por favor, tente novamente![/bold red]")
                sleep(1)
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    biblioteca = Biblioteca()
    biblioteca.criar_tabela()

    while True:
        try:
            conteudo = Align.center("BIBLIOTECA", vertical="middle")
            console.print(Panel(conteudo, width=30, style="bold white", border_style="bright_cyan"))
            sleep(1)
            opcao = int(Prompt.ask("[bold white]Escolha uma das opções abaixo:[/bold white]\n"
                              "[bold yellow][1]Ler tabela.[/bold yellow]\n"
                              "[bold green][2]Cadastrar livro.[/bold green]\n"
                              "[bold blue][3]Atualizar livro.[/bold blue]\n"
                              "[bold red][4]Deletar livro.[/bold red]\n"
                              "[bold orange3][0]Sair.[/bold orange3]\n"
                              "[bold white]Opção[/bold white]"))
            match (opcao):
                case 1:
                    biblioteca.ler_tabela()
                    limpar_terminal()
                case 2:
                    biblioteca.cadastrar_livro(*info_livro())
                    limpar_terminal()
                case 3:
                    while True:
                        try:
                            id = int(Prompt.ask("[bold orange3]Se não quiser atualizar um livro, apenas digite um id inválido.[/bold orange3]\n"
                                           "[bold white]Informe o id do livro que deseja atualizar[/bold white]"))
                            if id <= 0:
                                console.print("[bold red]O ID deve ser um número positivo![/bold red]")
                                continue
                            biblioteca.atualizar_livro(id, *info_livro())
                            limpar_terminal()
                            break
                        except ValueError:
                            console.print("[bold red]Digite um valor válido para o id! Letras e palavras não são permitidas![/bold red]")
                            sleep(1)
                case 4:
                    while True:
                        try:
                            id = int(Prompt.ask("[bold orange3]Se não quiser deletar um livro, apenas digite um id inválido[/bold orange3].\n"
                                           "[bold white]Informe o id do livro que deseja deletar[/bold white]"))
                            if id <= 0:
                                console.print("[bold red]O ID deve ser um número positivo![/bold red]")
                                continue
                            biblioteca.deletar_livro(id)
                            limpar_terminal()
                            break
                        except ValueError:
                            console.print("[bold red]Digite um valor válido para o id! Letras e palavras não são permitidas![/bold red]")
                            sleep(1)
                case 0:
                    biblioteca.fechar_conexao()
                    break
                case _:
                    console.print("[bold red]Opção inválida. Por favor, tente novamente![/bold red]")
                    sleep(1)
        except ValueError as VE:
            console.print("[bold red]Opção inválida. Por favor, tente novamente![/bold red]")