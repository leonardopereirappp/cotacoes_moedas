import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
import os
import numpy as np
from datetime import datetime

all_coins = requests.get(url=f"https://economia.awesomeapi.com.br/json/all").json()
lista_moedas = list(all_coins.keys())

janela = tk.Tk()
janela.rowconfigure(0, weight=1)  # O weight = 1 é um boolean para => app responsivo? 1: True; 0 (Default): False
janela.columnconfigure(0, weight=1)  # weight (width(comprimento) + height(altura))  É meio óbvio mas é legal dizer


# Funções dos botões
def pegar_cot_1():
    moeda = rconsulta_1_1.get()
    data_s = rconsulta_1_2.get()
    data = data_s.split('/')
    dia, mes, ano = data[0], data[1], data[2]
    cotacao = requests.get(url=f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}").json()  # Insira aqui a API com as informações de moeda e data
    resposta_1['text'] = f"A cotação do {moeda} na data {data_s} é de: {cotacao[0]['bid']}"
    resposta_1.grid(row=3, column=0, sticky='NESW')


def selecionar_arquivo():
    caminho_arquivo = askopenfilename(title="Selecione um arquivo em excel para abrir")
    nome_imagem, extensao = os.path.splitext(caminho_arquivo)
    if extensao == ".xlsx" or extensao == "xls":
        arquivo_caminho['text'] = f"{caminho_arquivo}"
        return caminho_arquivo
    else:
        arquivo_caminho['text'] = "Formato de arquivo incompatível com nosso sistema!"


def atualizar_cotacao():
    try:
        caminho_arquivo = arquivo_caminho['text']
        df_excel = pd.read_excel(io=caminho_arquivo)
        moedas = df_excel.iloc[:, 0]
        data_is = sdata_inicial.get()
        datai = data_is.split('/')
        diai, mesi, anoi = datai[0], datai[1], datai[2]
        data_fs = sdata_final.get()
        dataf = data_fs.split('/')
        diaf, mesf, anof = dataf[0], dataf[1], dataf[2]
        for moeda in moedas:
            cotacao = requests.get(url=f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={anoi}{mesi}{diai}&end_date={anof}{mesf}{diaf}").json()
            for cotacoes in cotacao:
                print(cotacoes)
                timestamp = int(cotacoes['timestamp'])
                data = datetime.fromtimestamp(timestamp)
                data = data.strftime('%d/%m/%Y')
                bid = float(cotacoes['bid'])
                if data not in df_excel:
                    df_excel[data] = np.nan
                df_excel.loc[df_excel.iloc[:, 0] == moeda, data] = bid
        df_excel.to_excel('teste.xlsx', index=False)
        mensagem['text'] = "Banco de dados atualizado com sucesso"
    except FileNotFoundError:
        mensagem['text'] = "Selecione um arquivo válido"


def fechar():
    janela.destroy()


# Botões a serem criados
# Como vimos no protótipo, o visual é baseado em 3 colunas e 11 linhas
# Uma moeda
titulo_1 = tk.Label(text="Cotação de uma moeda específica", fg='black', borderwidth=2, relief='solid')
consulta_1_1 = tk.Label(text="Selecione a moeda que deseja consultar: ")
rconsulta_1_1 = ttk.Combobox(values=lista_moedas)
consulta_1_2 = tk.Label(text="Selecione o dia que deseja pegar a cotação: ")
rconsulta_1_2 = DateEntry(year=2022, locale='pt_br')
resposta_1 = tk.Label(text="Sem resposta")
botao_pegar_cot_1 = tk.Button(text="Pegar Cotação", command=pegar_cot_1, fg='white', bg='gray')

# Várias moedas
titulo_2 = tk.Label(text="Cotação de uma moeda específica", fg='black', borderwidth=2, relief='solid')
consulta_2_1 = tk.Label(text="Selecione um arquivo excel com as moedas na coluna A: ")
rconsulta_2_1 = tk.Button(text="Selecionar", command=selecionar_arquivo)
mostrar_arquivo = tk.Label(text="Arquivo Selecionado: ")
arquivo_caminho = tk.Label(text="Nenhum arquivo selecionado!")
data_inicial = tk.Label(text="Data inicial: ")
sdata_inicial = DateEntry(year=2022, locale='pt_br')
data_final = tk.Label(text="Data Final: ")
sdata_final = DateEntry(year=2022, locale='pt_br')
botao_pegar_cot_2 = tk.Button(text="Atualizar Cotação", command=atualizar_cotacao, fg='white', bg='gray')
mensagem = tk.Label(text="")
botao_fechar = tk.Button(text="Fechar", fg='black', borderwidth=2, relief='solid', command=fechar)

# Botões a serem plotados
# Uma moeda
titulo_1.grid(row=0, column=0, columnspan=3, sticky='NESW', padx=10, pady=10)
consulta_1_1.grid(row=1, column=0, sticky='NESW')
rconsulta_1_1.grid(row=1, column=2, sticky='NESW')
consulta_1_2.grid(row=2, column=0, sticky='NESW')
rconsulta_1_2.grid(row=2, column=2, sticky='NESW')
resposta_1.grid(row=3, column=0, sticky='NESW')
botao_pegar_cot_1.grid(row=3, column=2, sticky='NESW')

# Várias moedas
titulo_2.grid(row=4, column=0, columnspan=3, sticky='NESW', padx=10, pady=10)
consulta_2_1.grid(row=5, column=0, sticky='NESW', padx=10, pady=10)
rconsulta_2_1.grid(row=5, column=2, sticky='NESW', padx=10, pady=10)
mostrar_arquivo.grid(row=6, column=0, sticky='WNS', padx=10, pady=10)
arquivo_caminho.grid(row=6, column=1, sticky='WNS', padx=10, pady=10)
data_inicial.grid(row=7, column=0, sticky='WNS', padx=10, pady=10)
sdata_inicial.grid(row=7, column=1, sticky='WNS', padx=10, pady=10)
data_final.grid(row=8, column=0, sticky='WNS', padx=10, pady=10)
sdata_final.grid(row=8, column=1, sticky='WNS', padx=10, pady=10)
botao_pegar_cot_2.grid(row=9, column=0, sticky='NESW', padx=10, pady=10)
mensagem.grid(row=9, column=1, sticky='NESW', columnspan=2)
botao_fechar.grid(row=10, column=2, sticky='NESW', columnspan=2)

# Exibir o app
janela.mainloop()
