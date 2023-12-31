import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os, random
from observe import _plot

# 關閉隨機性
seed = 4222
random.seed(seed)
np.random.seed(seed)

def random_select(df):
    df0 = df[df['label'] == 0].copy()
    df0_zero_percentage = ((df0 == 0).sum(axis=1)-1) / df0.shape[1]
    df0['zero'] = df0_zero_percentage
    df1 = df[df['label'] == 1].copy()
    df1_zero_percentage = (df1 == 0).sum(axis=1) / df1.shape[1]
    df1['zero'] = df1_zero_percentage

    label_0_indices = df0.index.tolist()
    label_1_indices = df1.index.tolist()
    random_indices = random.sample(label_0_indices, len(label_1_indices))
    return pd.concat([df0[df0.index.isin(random_indices)], df1]), df0[~df0.index.isin(random_indices)]

def antizero_select(df):
    df0 = df[df['label'] == 0].copy()
    _plot(df0, '', '0')
    df0_zero_percentage = ((df0 == 0).sum(axis=1)-1) / df0.shape[1]
    df0['zero'] = df0_zero_percentage
    
    df1 = df[df['label'] == 1].copy()
    _plot(df1, '', '1')
    df1_zero_percentage = (df1 == 0).sum(axis=1) / df1.shape[1]
    df1['zero'] = df1_zero_percentage

    last = df0.tail(df0.shape[0]-df1.shape[0])
    df0 = df0.head(df1.shape[0])
    return pd.concat([df0, df1]), last

def preprocess(filepath, savepath, filename):
    dataframe = pd.read_csv(os.path.join(filepath, filename), encoding = "ISO-8859-1")
    dataframe.fillna(value=0, inplace=True)
    print(dataframe.shape)

    # 特徵選擇
    print("----------preprocess-----------")
    '''刪除欄位：
    1 IPDAT 輸入日期
    2 IDCODE 歸戶代號
    3 OPDNO 門診號
    5 RGSDPT 掛號科別
    6 EMGADMDAT 急診入院日期
    7 EMGDGDAT 急診出院日期
    8 CSN 住院號
    9 ITID 離院動態代號
    82 EMGDEAD 急診死亡
    83 HSPDEAD 住院死亡
    84 DEADDAT 死亡時間
    85 DEADSINCEEMG 自急診入院死亡時間
    86 Dead within 24hr
    87 Dead within 72hr
    88 Dead within 168hr
    90 Dead within 6hr
    91 Dead within 12hr
    92 Dead within 48hr
    95 HSPADMDAT 住院日期
    96 HSPDGDAT 住院出院日期
    都是0的資料:
    31 Peptic ulcer disease
    40 AIDS/HIV
    50 RDWSD (%) /B
    74 EMGCRTICAL
    '''
    column=[1,2,3,5,6,7,8,9,31,40,50,74,82,83,84,85,86,87,88,90,91,92,95,96]
    dataframe.drop(dataframe.columns[column], inplace=True, axis=1)

    # 將bool改為int
    dataframe[dataframe.columns[56:70]] = dataframe[dataframe.columns[56:70]].astype('int')
    dataframe.rename(columns={'Finally dead':'label'}, inplace=True)
    dataframe['label']=dataframe['label'].astype('int')

    # column rename
    columns = dataframe.columns.tolist()
    for i, col in enumerate(columns):
        try:
            columns[i] = col.replace('/', '.')
        except:
            pass

    # 將label移至最後面
    dataframe.columns = columns
    columns.remove('label')
    columns.append('label')
    dataframe = dataframe[columns]

    # label 取出
    df_label = dataframe['label']
    dataframe.drop(columns=['label'], inplace=True)

    # 计算每个列的最小值和最大值
    min_values = dataframe.min()
    max_values = dataframe.max()

    # Min-Max 标准化到 0~1 范围
    normalized_df = (dataframe - min_values) / (max_values - min_values)
    del dataframe

    # label 放回
    normalized_df['label'] = df_label

    # 確認資料型態
    print('normalized dataframe')
    print(normalized_df.info())
    print(normalized_df['label'].value_counts())

    # 平衡label 

    # random選取label為0的 
    balanced_df, last_df = random_select(normalized_df)

    # 選取採樣資料內 0比較少的
    # 會增加一個欄位 : zero 
    # balanced_df, last_df = antizero_select(normalized_df)
    del normalized_df

    #分割訓練、測試
    train_df, test_df = train_test_split(balanced_df, test_size=0.2, random_state=seed)
    test_df = pd.concat([test_df, last_df])

    # 確認資料型態
    print('training set')
    print(train_df.shape)
    print(train_df['label'].value_counts())
    print('testing set')
    print(test_df.shape)
    print(test_df['label'].value_counts())

    # 儲存
    train_df.to_csv(os.path.join(savepath, 'train.csv'), index=None)
    test_df.to_csv(os.path.join(savepath, 'test.csv'), index=None)

if __name__ == '__main__':
    filepath = os.path.join('data', '0_ori')
    savepath = os.path.join('data', '1_preprocess')
    os.makedirs(savepath, exist_ok=True)
    filename = 'Hospital.csv'
    preprocess(filepath, savepath, filename)