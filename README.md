# Hospital
檔案放在data/0_ori  
先跑preprocess.py  

前處理:  
刪除無用ID特徵ID、dead相關特徵   
min-max normalize  
新增zero欄位，為每筆資料內有多少0的百分比  

原始特徵：  
生:死 = 589848:14765  
平衡後：  
生:死 = 14765:14765  
訓練集：  
生:死 = 11838:11786  
測試集：  
生:死 = 578010:2979  

處理好的資料儲存在data/0_ori/preprocessed  
8:2拆分訓練資料、測試資料放在data/1_preprocess  

跑run.py  
(需要使用https://github.com/nervouswizard/ct-value)  

跑training_model.py可以執行DNN
