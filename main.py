from flet import *
import sqlite3


# Conectando a Base de Dados
conexão = sqlite3.connect('dados.db', check_same_thread=False)
cursor = conexão.cursor()


# Criar tabelad na Base de Dados
def tabelas():
    cursor.execute(
        'create table if not exists clientes (id integer primary key autoincrement, nome text)'
    )


class App(UserControl):
    def __init__(self):
        super().__init__()

        self.todos_dados = Column(
            auto_scroll=True,
        )
        self.adicionar_dados = TextField(
            label='Dado',
        )
        self.editar_dado = TextField(
            label='Editar'
        )


    # Função de deletar dado
    def deletar(self, x, y):
        cursor.execute(
            'delete from clientes where id = ?', [x]
        )
        y.open = False
        # Chamar a função de renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()


    def atualizar(self, x, y, z):
        cursor.execute(
            'update clientes set nome = ? where id = ?', (y, x)
        )
        conexão.commit()
        z.open = False
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()


    # Criando função para abrir ações
    def abrir_ações(self, e):
        id_user = e.control.subtitle.value
        self.editar_dado.value = e.control.title.value
        self.update()
        alerta_dialogo = AlertDialog(
            title=Text(f'Editar ID {id_user}'),
            content=self.editar_dado,
            # Botões de ação
            actions=[
                ElevatedButton(
                    'Deletar',
                    color='white',
                    bgcolor='red',
                    on_click=lambda e:self.deletar(id_user, alerta_dialogo)
                ),
                ElevatedButton(
                    'Atualizar',
                    on_click=lambda e:self.atualizar(id_user, self.editar_dado.value, alerta_dialogo)

                )
            ],
            actions_alignment='spaceBetween'
        )
        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        # Atualizat a página
        self.page.update()


    # READ - Mostrar todos os dados da base de dados
    def renderizar_todos(self):
        cursor.execute(
            'select * from clientes'
        )
        conexão.commit()
        meus_dados = cursor.fetchall()
        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_ações,
                )
            )
        self.update()


    def ciclo_vida(self):
        self.renderizar_todos()

    
    # Inserir um dado na Base de Dados
    def inserir_dado(self, e):
        cursor.execute(
            'insert into clientes (nome) values (?)',
            [
                self.adicionar_dados.value
            ]
        )
        conexão.commit()
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()


    def build(self):
        return Column(
            [
                Text(
                    'Crud com SQLite',
                    size=20,
                    weight='bold',
                ),
                self.adicionar_dados,
                ElevatedButton(
                    'Adicionar dado',
                    on_click=self.inserir_dado,
                ),
                self.todos_dados
            ]
        )


def main(page: Page):
    page.update()
    tabelas()
    minha_aplicação = App()
    page.add(
        minha_aplicação,
    )


app(target=main)
