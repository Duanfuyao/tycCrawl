# -*- coding: utf-8 -*-
import json
import os

def getAllfiles(path):
    files = os.listdir(path)
    allfiles = []
    for file in files:
        if os.path.isdir(path+file):
            allfiles.extend(getAllfiles(path+file+"/"))
        else:
            allfiles.append(path+file)
    return allfiles


def main():
    with open("testBaseline.config") as configfile:
        config = json.load(configfile)

    global trainDataPath
    trainDataPath = config["train_data_path"]

    files = getAllfiles(trainDataPath)
    texts = []
    titles= []
    times=[]
    tenderers=[]
    num=0
    for file in files:
        if not os.path.isdir(file):
            with open(file, encoding='UTF-8') as f:
                lines = f.readlines()
                str = ""
                tenderer=[]
                for line in lines:
                    str = str+line
                    if line.find("招标人：") != -1 or line.find("招 标 人：") != -1 or line.find("项目地点：") != -1:
                        tenderer.append(line)
                texts.append(str)
                titles.append(lines[1])
                times.append(lines[3])
                tenderers.append(tenderer)
                if len(str) == 0:
                    print("length is 0: ", file)
                if len(tenderer) == 0:
                    print("tenderer is 0: ", file)
                    num+=1

    lengths=[len(str) for str in texts]
    print("max length:", max(lengths))
    print("min length:", min(lengths))
    print("num of documents:", len(texts))
    print("num of titles:", len(titles))
    print("num of times:", len(times))
    tenderer_num = [len(tenderer) for tenderer in tenderers]
    print("min tenderer_num:", min(tenderer_num))
    print(num)
if __name__=="__main__":
    main()