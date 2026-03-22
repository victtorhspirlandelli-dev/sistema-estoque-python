import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

# carregar dados
try:
    with open("dados.json", "r") as f:
        dados = json.load(f)
        estoque = dados["estoque"]
        historico = dados["historico"]
except:
    estoque = {}
    historico = []

# salvar tudo
def salvar():
    with open("dados.json", "w") as f:
        json.dump({"estoque": estoque, "historico": historico}, f)
    status("Dados salvos!", "blue")

def status(msg, cor="white"):
    lbl_status.config(text=msg, fg=cor)

# atualizar tabela
def atualizar_tabela():
    for i in tabela.get_children():
        tabela.delete(i)

    for produto, qtd in estoque.items():
        alerta = "⚠️" if qtd <= 5 else ""
        tabela.insert("", "end", values=(produto, qtd, alerta))

# adicionar
def adicionar():
    nome = entry_nome.get().strip().lower()
    qtd = entry_qtd.get()

    if nome == "" or qtd == "":
        status("Preencha os campos!", "red")
        return

    qtd = int(qtd)

    estoque[nome] = estoque.get(nome, 0) + qtd
    status("Produto adicionado!", "green")

    atualizar_tabela()
    entry_nome.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)

# vender
def vender():
    nome = entry_nome.get().strip().lower()
    qtd = entry_qtd.get()

    if nome not in estoque:
        status("Produto não encontrado", "red")
        return

    qtd = int(qtd)

    if estoque[nome] < qtd:
        status("Estoque insuficiente", "red")
        return

    estoque[nome] -= qtd

    data = datetime.now().strftime("%d/%m %H:%M")
    historico.append(f"{data} - Venda: {nome} - {qtd}")

    status("Venda realizada!", "green")
    atualizar_tabela()

# remover
def remover():
    selecionado = tabela.selection()
    if not selecionado:
        status("Selecione um produto!", "red")
        return

    item = tabela.item(selecionado)
    nome = item["values"][0]

    del estoque[nome]
    status("Produto removido!", "orange")
    atualizar_tabela()

# ver histórico
def ver_historico():
    janela_hist = tk.Toplevel(janela)
    janela_hist.title("Histórico")

    txt = tk.Text(janela_hist, width=40, height=15)
    txt.pack()

    for item in historico:
        txt.insert(tk.END, item + "\n")

# janela principal
janela = tk.Tk()
janela.title("Sistema de Estoque")
janela.geometry("500x500")
janela.configure(bg="#1e1e1e")

# título
tk.Label(janela, text="📦 Sistema de Estoque", bg="#1e1e1e",
         fg="white", font=("Arial", 16, "bold")).pack(pady=10)

# inputs
frame_inputs = tk.Frame(janela, bg="#1e1e1e")
frame_inputs.pack()

entry_nome = tk.Entry(frame_inputs)
entry_nome.grid(row=0, column=0, padx=5, pady=5)

entry_qtd = tk.Entry(frame_inputs)
entry_qtd.grid(row=0, column=1, padx=5, pady=5)

# botões
frame_btn = tk.Frame(janela, bg="#1e1e1e")
frame_btn.pack()

tk.Button(frame_btn, text="Adicionar", bg="green", fg="white", command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Vender", bg="orange", command=vender).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Remover", bg="red", fg="white", command=remover).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Histórico", bg="blue", fg="white", command=ver_historico).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Salvar", bg="purple", fg="white", command=salvar).grid(row=0, column=4, padx=5)

# tabela
tabela = ttk.Treeview(janela, columns=("Produto", "Qtd", "Alerta"), show="headings")
tabela.heading("Produto", text="Produto")
tabela.heading("Qtd", text="Quantidade")
tabela.heading("Alerta", text="")

tabela.pack(pady=10, fill="both", expand=True)

# status
lbl_status = tk.Label(janela, text="", bg="#1e1e1e", fg="white")
lbl_status.pack()

atualizar_tabela()

janela.mainloop()