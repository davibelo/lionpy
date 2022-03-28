import pandas as pd
df_extrato = pd.read_excel("extrato.xls", engine="xlrd")
df_cadastro = pd.read_excel("cadastro.xls", engine="xlrd")

EXTRATO_SIZE = df_extrato.shape[0]

# declaring lists to receive information
data_lancamento = []
cod_rendimento = []
cod_ocupacao = []
valor_recebido = []
valor_deducao = []
historico = []
ind_recebido_de = []
cpf_titular = []
cpf_beneficiario = []
ind_cpf_nao_informado = []
cnpj = []
ind_irrf = []

for i in range(EXTRATO_SIZE):
    if df_extrato.loc[i,"Tipo"] == "RECEITA":
        data_lancamento.append(df_extrato.loc[i,"Dt. de Pagamento"])
        cod_rendimento.append("R01.001.001")
        cod_ocupacao.append("255")
        valor_recebido.append(str(df_extrato.loc[i,"Valor Pago (R$)"]).replace(".",","))
        valor_deducao.append("0,00")
        historico.append("Consulta")
        ind_recebido_de.append("PF")
        cnpj.append("")
        ind_irrf.append("")

        # generating a cadastro dataframe that contains the same name from extrato dataframe
        df_cadastro_query = df_cadastro[df_cadastro.loc[:, "Nome Completo"] == df_extrato.loc[i, "Descrição"]]
        cpf = str(df_cadastro_query["CPF"].values[0])
        # purging "." and "-" from cpf string and appending on cpf list
        cpf = cpf.replace(".", "").replace("-", "")
        cpf_titular.append(cpf)
        ind_cpf_nao_informado.append("")

#FIXIT: some rows contains nan when supposed to be ""
for cpf in cpf_titular:    
    if cpf == "nan":
        cpf = " "
    print(cpf)

cpf_beneficiario = cpf_titular

# mounting dict with lists information
escrituracao = {
    "Data do lançamento": data_lancamento,
    "Código do rendimento": cod_rendimento,
    "Código da ocupação": cod_ocupacao,
    "Valor recebido": valor_recebido,
    "Valor da dedução": valor_deducao,
    "Histórico": historico,
    'Indicador "recebido de"': ind_recebido_de,
    "CPF do titular pagamento": cpf_titular,
    "CPF do beneficiário serviço": cpf_beneficiario,
    'Indicador "CPF não informado"': ind_cpf_nao_informado,
    "CNPJ":cnpj,
    "Indicador de IRRF": ind_irrf
}

df_escrituracao = pd.DataFrame.from_dict(escrituracao)
df_escrituracao.to_csv("escrituracao.csv", index=False)