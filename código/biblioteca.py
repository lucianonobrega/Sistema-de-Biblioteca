import sqlite3
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class Biblioteca():
    def __init__(self):
        self.conn = sqlite3.connect("minha_biblioteca.db")
        self.cursor = self.conn.cursor()

    def criar_tabela(self) -> None:
        comando = """CREATE TABLE IF NOT EXISTS livros(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    autor TEXT,
                    ano INTEGER,
                    genero TEXT)"""

        self.cursor.execute(comando)
        self.conn.commit()

    def ler_tabela(self) -> None:
        comando = """SELECT * FROM livros"""
        self.cursor.execute(comando)
        livros = self.cursor.fetchall()

        if not livros:
            console.print("[bold red]Nenhum livro cadastrado![/bold red]")
            sleep(3)
            return

        tabela = Table(title="LISTA DE LIVROS", style="bold #03f8fc", show_lines=True, title_style="bold white", title_justify="center")
        tabela.add_column("ID", style="bold white", justify="center", no_wrap=False)
        tabela.add_column("Título", style="bold #03fc07", justify="center", no_wrap=False)
        tabela.add_column("Autor", style="italic #03fc07", justify="center", no_wrap=False)
        tabela.add_column("Ano", style="#03fc07", justify="center", no_wrap=False)
        tabela.add_column("Gênero", style="#03fc07", justify="center", no_wrap=False)
        for livro in livros:
            tabela.add_row(f"{livro[0]}",
                           f"{livro[1]}",
                           f"{livro[2]}",
                           f"{livro[3]}",
                           f"{livro[4]}")
        console.print(tabela)
        Prompt.ask("Pressione [bold green]ENTER[/bold green] para continuar...")

    def cadastrar_livro(self, titulo:str, autor:str, ano:int, genero:str) -> None:
        try:
            comando = """INSERT INTO livros(titulo, autor, ano, genero)
                        VALUES(?,?,?,?)"""
            self.cursor.execute(comando,(titulo,autor,ano,genero))
            self.conn.commit()
            console.print("[bold green]Livro cadastrado com sucesso![/bold green]")
            sleep(3)
        except sqlite3.OperationalError as OE:
            console.print(f"[bold red]Aconteceu um erro:[/bold red] {OE}.")
            sleep(10)

    def atualizar_livro(self, id:int, titulo:str, autor:str, ano:int, genero:str) -> None:
        try:
            comando = """UPDATE livros set titulo = ?, autor = ?, ano = ?, genero = ? WHERE id = ?"""

            self.cursor.execute(comando, (titulo, autor, ano, genero, id))
            self.conn.commit()
            console.print("[bold green]Dados atualizados com sucesso![/bold green]")
            sleep(3)
        except sqlite3.OperationalError as OE:
            console.print(f"[bold red]Aconteceu um erro:[/bold red] {OE}.")
            sleep(10)

    def deletar_livro(self, id:int) -> None:
        try:
            comando = """DELETE FROM livros WHERE id = ?"""

            self.cursor.execute(comando, (id,))
            self.conn.commit()
            console.print("[bold green]Livro deletado com sucesso![/bold green]")
            sleep(3)
        except sqlite3.OperationalError as OE:
            console.print(f"[bold red]Aconteceu um erro:[/bold red] {OE}.")
            sleep(10)

    def fechar_conexao(self):
        self.conn.close()