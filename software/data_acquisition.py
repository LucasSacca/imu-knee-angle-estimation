import pandas as pd
import numpy as np
import serial
import time
import os
# from tabulate import tabulate
# def dfprint(df):
#     print(tabulate(df, headers='keys', tablefmt="fancy_grid", showindex= False))


# ==========================
#   Parâmetros fixos
# ==========================
porta_com = 'COM6'
coletas_dir = 'coletas'
baudrate = 115200 
T_amostragem = 0.008



df_raw = pd.DataFrame(columns=[
    'tempo_mcu',

    'acel_x_coxa',
    'acel_y_coxa',
    'acel_z_coxa',
    
    'giro_x_coxa',
    'giro_y_coxa',
    'giro_z_coxa',
    
    'acel_x_perna',
    'acel_y_perna',
    'acel_z_perna',

    'giro_x_perna',
    'giro_y_perna',
    'giro_z_perna',

])

df_raw_cols = list(df_raw.columns)

# ==========================
#   Funções
# ==========================
def connect_to_serial(port, baudrate):
    i=1
    while True:
        try:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            print(f"Sensor conectado com sucesso (porta {port})\n")
            return ser
        except serial.SerialException as error:
            print(f"[{i}] Erro ao conectar ao sensor: {error}")
            time.sleep(1)
            i +=1


def receive_data(ser):
    data_raw = ser.readline().decode("utf-8").strip().split(',')
    print('raw:', data_raw)

    if len(data_raw) != len(df_raw_cols):  # linha incompleta ou de texto
            return None
    
    new_line = dict()
    for i in range(len(df_raw_cols)):

        new_line[df_raw_cols[i]] = data_raw[i]

    return pd.DataFrame([new_line])


# ==========================
#   Coleta e armazenamento
# ==========================

# Classificação da Coleta
nome_voluntario = input('\nNome do voluntário: ')
categoria_coleta = input('\nSelecione a categoria da leitura: \n(1) Calibração\n(2) Coleta\nResposta (responda com 1 ou 2): ')

# nome_voluntario = 'teste'
# categoria_coleta = '1'

while categoria_coleta != '1' and categoria_coleta != '2':
    print('\nESCOLHA INVÁLIDA. DIGITE "1" ou "2".')
    categoria_coleta = input('\n(1) Calibração\n(2) Coleta\nResposta (responda com 1 ou 2): ')

categoria_coleta = 'calibracao' if categoria_coleta == '1' else 'coleta'
tempo_coleta = 10 if categoria_coleta == 'calibracao' else 30 

file_path = os.path.join(coletas_dir, f"{nome_voluntario.replace(' ', '_').lower()}_{categoria_coleta}.csv")

if not os.path.exists(coletas_dir):
    os.makedirs(coletas_dir, exist_ok=True)


# Conexão com a ESP:
ser = connect_to_serial(port=porta_com, baudrate= baudrate)
ser.reset_input_buffer()  # descarta tudo que chegou antes de começar a coletar


# Recebimento dos dados dentro do tempo de coleta:
t0 = time.time()
linhas_vazias = 0
while (time.time() - t0) < tempo_coleta:
    df_new_line = receive_data(ser)

    try:
        if df_new_line == None:
            linhas_vazias += 1
            continue
    except:
        None

    df_raw = pd.concat([df_raw, df_new_line])
    print(list(df_new_line.iloc[0]))

    df_raw.to_csv(path_or_buf=file_path, index=False)

# Diferenciação entre o tempo marcado pelo Clock do MCU (tempo_mcu) 
# e uma coluna com nosso período de amostragem vetorizado (tempo_vetorizado)
df_raw[df_raw.columns] = df_raw[df_raw.columns].apply(pd.to_numeric)
amostragem_array = np.linspace(start=0, stop= (T_amostragem * len(df_raw)), num=len(df_raw))

df_raw['tempo_mcu'] = ((df_raw['tempo_mcu'] - df_raw['tempo_mcu'].iloc[0])/1000) + T_amostragem    
df_raw.insert(loc=0, column='tempo_vetorizado', value= amostragem_array)

df_raw.to_csv(path_or_buf=file_path, index=False)
print(f'QTD. linhas vazias: {linhas_vazias}')
