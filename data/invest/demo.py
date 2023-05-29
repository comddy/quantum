import pandas as pd
import os
df = pd.read_excel("A股股票.xlsx", converters={'code':str})

t = ['create', 'main', 'mas', 'sc']
for filename in ['create', 'main', 'mas', 'sc']:
    idx = 1
    data = []
    for file in os.listdir(f'./{filename}'):
        path = f'./{filename}/{file}'
        name = df.loc[df['code'] == file[:6]]['name'].values[0]
        f = pd.read_excel(path)
        earning_rate = round((f['close'].iloc[-1] - f['close'][0]) / f['close'][0] * 100, 2)
        data.append([idx, file[:6], name, earning_rate])
        idx+=1

    save_df = pd.DataFrame(data, columns=['序号', '股票代码', '股票名称', '涨幅'])
    save_df.to_excel(f'{filename}.xlsx', index=False)
# if __name__ == '__main__':
#     f = pd.read_excel('./create/300002.xlsx')
#     print(type(f['close']))
#     print()
    