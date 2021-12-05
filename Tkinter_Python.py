from tkinter import *
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
from tkcalendar import Calendar, DateEntry

root = tix.Tk()

class validadores:
    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100

class relatorio():
    def printcliente(self):
        webbrowser.open("cliente.pdf")

    def gerarelatoriocliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigorel = self.codigo_entry.get()
        self.nomerel = self.nome_entry.get()
        self.telefonerel = self.telefone_entry.get()
        self.cidaderel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'Telefone: ')
        self.c.drawString(50, 610, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(122, 700, self.codigorel)
        self.c.drawString(110, 670, self.nomerel)
        self.c.drawString(133, 640, self.telefonerel)
        self.c.drawString(120, 610, self.cidaderel)

        self.c.rect(20, 550, 550, 5, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printcliente()

class funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close(); print("Desconectando do banco de dados")

    def montatabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS clientes (
                 cod INTEGER PRIMARY KEY,
                 nome_cliente CHAR(40) NOT NULL,
                 telefone INTEGER(20),
                 cidade CHAR(40)
             );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        self.variaveis()
        if self.nome_entry.get() == "":
            msg = "Para cadastrar um novo criente é necessário \n"
            msg += "que seja digitado pelo menos um nome"
            messagebox.showinfo("Cadastro de clientes - Aviso!!!", msg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                VALUES (?, ?, ?) """, (self.nome, self.telefone, self.cidade))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()
    
    def select_lista(self):
        self.listacli.delete(*self.listacli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY cod ASC; """)
        for i in lista:
            self.listacli.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listacli.selection()

        for n in self.listacli.selection():
            col1, col2, col3, col4 = self.listacli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def buscar_cliente(self):
        self.conecta_bd()
        self.listacli.delete(*self.listacli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome)
        buscanomecli = self.cursor.fetchall()
        for i in buscanomecli:
            self.listacli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()

    def calendario(self):
        self.calendario1 = Calendar(self.aba2, fg="gray75", bg="blue", font=("Times", '9', 'bold'), locale='pt_br')
        self.calendario1.place(relx=0.5, rely=0.1)
        self.calData = Button(self.aba2, text="Inserir Data", command=self.print_cal)
        self.calData.place(relx=0.55, rely=0.85, height=25, width=100)

    def print_cal(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_data.delete(0, END)
        self.entry_data.insert(END, dataIni)
        self.calData.destroy()

class Application(funcs, relatorio, validadores):
    def __init__(self):
        self.root = root
        self.valida_entradas()
        self.tela()
        self.frames_de_tela()
        self.widgets_flame1()
        self.lista_flame2()
        self.montatabelas()
        self.select_lista()
        self.menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background="#1e3743")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_de_tela(self):
        self.flame_1 = Frame(self.root, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=3)
        self.flame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.flame_2 = Frame(self.root, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=3)
        self.flame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_flame1(self):
        ###Abas####
        self.abas = ttk.Notebook(self.flame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background="#dfe3ee")
        self.aba2.configure(background="lightgray")

        self.abas.add(self.aba1, text="Aba 1")
        self.abas.add(self.aba2, text="Aba 2")

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        ###Quadro por trás dos botões###
        self.canvas_bt = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground='gray', highlightthickness=5)
        self.canvas_bt.place(relx=0.19, rely=0.08, relwidth=0.22, relheight=0.19)

        ### Criação do botão limpar
        self.bt_limpar = Button(self.aba1, text="Limpar", bd=2, bg="#107db2", fg="white", font=("verdana", 8, "bold"), activebackground='#108ecb', activeforeground='white', command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão buscar
        self.bt_buscar = Button(self.aba1, text="Buscar", bd=2, bg="#107db2", fg="white", font=("verdana", 8, "bold"), command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        texto_balao_buscar = "Digite no campo nome o cliente que deseja pesquisar."
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg=texto_balao_buscar)

        ### Criação do botão novo
        self.bt_novo = Button(self.aba1, text="Novo", bd=2, bg="#107db2", fg="white", font=("verdana", 8, "bold"), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão alterar
        self.bt_alterar = Button(self.aba1, text="Alterar", bd=2, bg="#107db2", fg="white", font=("verdana", 8, "bold"), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão apagar
        self.bt_apagar = Button(self.aba1, text="Apagar", bd=2, bg="#107db2", fg="white", font=("verdana", 8, "bold"), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação da label e entrada do código
        self.lb_codigo = Label(self.aba1, text="Código", bg="#dfe3ee", fg="#107db2")
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.aba1, validate="key", validatecommand=self.vcmd2)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        ### Criação da label e entrada do nome
        self.lb_nome = Label(self.aba1, text="Nome", bg="#dfe3ee", fg="#107db2")
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.aba1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

        ### Criação da label e entrada do telefone
        self.lb_telefone = Label(self.aba1, text="Telefone", bg="#dfe3ee", fg="#107db2")
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.aba1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        ### Criação da label e entrada da cidade
        self.lb_cidade = Label(self.aba1, text="Cidade", bg="#dfe3ee", fg="#107db2")
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.aba1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

        ### drop down button
        self.Tipvar = StringVar(self.aba2)
        self.TipV = ("Solterio(a)", "Casado(a)", "Divorciado(a)", "Viuvo(a)")
        self.Tipvar.set("Solterio(a)")
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.2)
        self.estado_civil = self.Tipvar.get()
        print(self.estado_civil)

        ### Calendario
        self.bt_calendario = Button(self.aba2, text="Data", command=self.calendario)
        self.bt_calendario.place(relx=0.5, rely=0.02)
        self.entry_data = Entry(self.aba2, width=10)
        self.entry_data.place(relx=0.5, rely=0.2)

    def lista_flame2(self):
        self.listacli = ttk.Treeview(self.flame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listacli.heading('#0', text="")
        self.listacli.heading('#1', text="Código")
        self.listacli.heading('#2', text="Nome")
        self.listacli.heading('#3', text="Telefone")
        self.listacli.heading('#4', text="Cidade")

        self.listacli.column('#0', width=1)
        self.listacli.column('#1', width=50)
        self.listacli.column('#2', width=200)
        self.listacli.column('#3', width=125)
        self.listacli.column('#4', width=125)

        self.listacli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroollista = Scrollbar(self.flame_2, orient='vertical')
        self.listacli.configure(yscroll=self.scroollista.set)
        self.scroollista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listacli.bind("<Double-1>", self.OnDoubleClick)

    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu =  Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit(): self.root.destroy()

        menubar.add_cascade(label = "Opções", menu= filemenu)
        menubar.add_cascade(label = "Relatórios", menu= filemenu2)

        filemenu.add_command(label="Sair", command=quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente", command=self.gerarelatoriocliente)

    def janela2(self):
        self.root2 = Toplevel()
        self.root2.title("Janela 2")
        self.root2.configure(background='lightblue')
        self.root2.geometry("400x200")
        self.root2.resizable(False, False)
        self.root2.transient(self.root)
        self.root2.focus_force()         ###sobrepoe a janela anterior
        self.root2.grab_set()         ###impede a utilização da janela anterior

    def valida_entradas(self):
        self.vcmd2 = (self.root._register(self.validate_entry2), "%P")

Application()