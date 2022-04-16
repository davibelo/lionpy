import pandas as pd

df_cadastro = pd.read_excel("cadastro.xls", engine="xlrd")
df_extrato = pd.read_excel("extrato.xls", engine="xlrd")
#print(df_cadastro)
#print(df_extrato)

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
ind_cpf_benef_nao_informado = []
cnpj = []
ind_irrf = []

for i in range(EXTRATO_SIZE):
    if df_extrato.loc[i, "Tipo"] == "RECEITA":
        data_lancamento.append(df_extrato.loc[i, "Dt. de Pagamento"])
        cod_rendimento.append("R01.001.001")
        cod_ocupacao.append("255")
        valor_recebido.append(
            str(df_extrato.loc[i, "Valor Pago (R$)"]).replace(".", ","))
        valor_deducao.append("0,00")
        historico.append("Consulta")
        ind_recebido_de.append("PF")

        # generating a cadastro dataframe that contains the same name from extrato dataframe
        df_cadastro_query = df_cadastro[df_cadastro.loc[:, "Nome Completo"] == df_extrato.loc[i, "Descrição"]]
        if df_cadastro_query.empty:
            cpf = ""
        else:
            cpf = str(df_cadastro_query["CPF"].values[0])
            cpf = cpf.replace(".", "").replace("-", "")
        # purging "." and "-" from cpf string and appending on cpf list
        cpf_titular.append(cpf)

        cpf_beneficiario = ""
        ind_cpf_benef_nao_informado.append("S")
        cnpj.append("")
        ind_irrf.append("")


# substituting cpf = "nan" for ""
cpf_titular = ["" if cpf == "nan" else cpf for cpf in cpf_titular]

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
    'Indicador "CPF não informado"': ind_cpf_benef_nao_informado,
    "CNPJ": cnpj,
    "Indicador de IRRF": ind_irrf
}

# mounting dataframe from dict
df_escrituracao = pd.DataFrame.from_dict(escrituracao)

# exporting dateframe as csv
df_escrituracao.to_csv("escrituracao.csv", sep=";", index=False, header=False)