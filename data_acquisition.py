import pandas as pd
import serial
import numpy as np
import time
# from tabulate import tabulate
# def dfprint(df):
#     print(tabulate(df, headers='keys', tablefmt="fancy_grid", showindex= False))


# ==========================
#   Parâmetros fixos
# ==========================
porta_com = 'COM5'
baudrate = 115200
T_amostragem = 0.025
tempo_coleta = 3


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
    # print('ser:', ser.readline())
    # print('raw:', data_raw)
    
    new_line = dict()
    for i in range(len(df_raw_cols)):

        new_line[df_raw_cols[i]] = data_raw[i]

    return pd.DataFrame([new_line])



# ==========================
#   Coleta e armazenamento
# ==========================

# Conexão com a ESP:
ser = connect_to_serial(port=porta_com, baudrate= baudrate)

# Recebimento dos dados dentro do tempo de coleta:
t0 = time.time()
while (time.time() - t0) < tempo_coleta:
    df_new_line = receive_data(ser)
    df_raw = pd.concat([df_raw, df_new_line])
    print(list(df_new_line.iloc[0]))

# Diferenciação entre o tempo marcado pelo Clock do MCU (tempo_mcu) 
# e uma coluna com nosso período de amostragem vetorizado (tempo_vetorizado)
df_raw[df_raw.columns] = df_raw[df_raw.columns].apply(pd.to_numeric)
amostragem_array = np.linspace(start=T_amostragem, stop= (T_amostragem * len(df_raw)), num=len(df_raw))

df_raw['tempo_mcu'] = ((df_raw['tempo_mcu'] - df_raw['tempo_mcu'].iloc[0])/1000) + T_amostragem    
df_raw.insert(loc=0, column='tempo_vetorizado', value= amostragem_array)
df_raw.to_csv(path_or_buf= 'raw_data.csv', index=False)