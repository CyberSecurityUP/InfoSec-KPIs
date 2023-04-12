import pandas as pd
from powerbiclient import Report, models
from powerbiclient.authentication import DeviceCodeLoginAuthentication

# Função para ler os dados do arquivo Excel
def read_excel_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    return df

# Substitua os valores abaixo pelos detalhes do seu aplicativo do Power BI
client_id = "YOUR_APP_CLIENT_ID"
group_id = "YOUR_GROUP_ID"
report_id = "YOUR_REPORT_ID"

# Autenticando com a API do Power BI
device_auth = DeviceCodeLoginAuthentication(client_id)

# Substitua os valores abaixo pelo caminho do arquivo Excel e o nome da planilha
file_path = "your_file.xlsx"
sheet_name = "your_sheet_name"

# Lendo os dados do arquivo Excel
data = read_excel_data(file_path, sheet_name)

# Atualizando o dataset do Power BI com os novos dados
# Substitua "YourTableName" pelo nome da tabela que você deseja atualizar no Power BI
# Substitua "YourDatasetID" pelo ID do conjunto de dados que você deseja atualizar no Power BI
table_name = "YourTableName"
dataset_id = "YourDatasetID"

rows = data.to_dict(orient='records')
body = models.PushDatasetRows(dataset_id, table_name, rows)

try:
    response = device_auth.power_bi_client.datasets.push_rows(body)
    print("Dados enviados com sucesso!")
except Exception as e:
    print(f"Erro ao enviar os dados: {e}")
