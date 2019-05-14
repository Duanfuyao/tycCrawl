import cpca
import json
import numpy as np
import pandas as pd
file='data_ggzy3/千童公园室外广播和网络视频监控系统、凤凰公园管理办公室、盐山县城区果皮箱采购项目招标公告.html'
with open(file, encoding='UTF-8') as f:
    js=json.load(f)['text'].split('\n')#sep=['\n',',',' '])
    df=cpca.transform(js, cut=False, pos_sensitive=True)
    df=np.array(df[df['省']!='']).tolist()
    df2=[]
    for i in range (len(df)):
        d=[]
        d.append(df[i][0]+df[i][1]+df[i][0])
        df2.append(d)
    df=pd.DataFrame(df2,columns=['省市区']).groupby('省市区').size()
    #df=pd.DataFrame(np.array(df).tolist(),columns=['省市区','frequence'])
    print(df)
    df=np.array(df)
    print(df)



