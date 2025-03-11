import pandas as pd
#web クロール   #2
#syori  #1
#output #1

#x x:数字　の順番で優先

#web

#syori
    #input motoni tikan toka seikei
    #input browser dev tool kara element copy
    #zokusei1 zokusei2 syutyrokuwo pg de jissou sitai

    #flow
    #1 input wo sitei(2file 2024/12/24 jiten)
    #2 set card name, ruby,(kind of card 1 and 2)
#output
    #excel ni syuturyoku yotei
#jissou    
#syori1

##card name, ruby, attribute same pg
with open("./input/01_cardInfo.txt",encoding='utf-8') as f:
    lines = f.readlines()

lines_srtip = [line.replace('\t','') for line in lines]

##save card name
lines_card_name = [line for line in lines_srtip if '<span class="card_name">' in line]

lines_card_name_replace = [item.replace('<span class="card_name">','') for item in lines_card_name]
lines_card_name_replace = [item.replace('</span>','') for item in lines_card_name_replace]


with open("./work/01_card_name.txt",mode='w',encoding='utf-8') as f:
    f.writelines(lines_card_name_replace)

##save card ruby
lines_card_ruby = [line for line in lines_srtip if '<span class="card_ruby">' in line]

lines_card_ruby_replace = [item.replace('<span class="card_ruby">','') for item in lines_card_ruby]
lines_card_ruby_replace = [item.replace('</span>','') for item in lines_card_ruby_replace]


with open("./work/02_card_ruby.txt",mode='w',encoding='utf-8') as f:
    f.writelines(lines_card_ruby_replace)

##save card kinds stream
lines_card_kinds = [line for line in lines_srtip if 'img class="icon_img ui-draggable' in line]
lines_card_kinds_replace = [item.replace('<img class="icon_img ui-draggable ui-draggable-handle" src="external/image/parts/attribute/','') for item in lines_card_kinds]
lines_card_kinds_replace = [item.replace('<img class="icon_img ui-draggable ui-draggable-handle" src="external/','') for item in lines_card_kinds_replace]
lines_card_kinds_replace = [item.replace('\n','★') for item in lines_card_kinds_replace]

str_lines_card_kinds = ','.join(lines_card_kinds_replace)
str_lines_card_kinds = str_lines_card_kinds.replace("★,image","\timage")

lines_card_kinds_replace = str_lines_card_kinds.split(',')
lines_card_kinds_replace = [item.replace('★','\n') for item in lines_card_kinds_replace]

with open("./work/03_card_attribute.txt",mode='w',encoding='utf-8') as f:
    f.writelines(lines_card_kinds_replace)


##save card effects or etc info (XYZ or sokko .etc)
with open("./input/02_cardInfo_text.txt",encoding='utf-8') as f:
    lines_2 = f.readlines()

lines_srtip_2 = [line.replace('\t','') for line in lines_2]

lines_card_effect = [line for line in lines_srtip_2 if '<img src="external/image/parts/card/card_icon_' in line]

with open("./work/04_card_effect.txt",mode='w',encoding='utf-8') as f:
    f.writelines(lines_card_effect)


#########################################
# set zokusei and excel out put
#########################################

monster_syurui_dic = {
                      "エクシーズ/モンスター":"エクシーズ",
                      "シンクロ/モンスター":"シンクロ",
                      "リンク/モンスター":"リンク",
                      "効果/モンスター":"効果",
                      "融合/モンスター":"融合",
                      "ペンデュラム/効果/モンスター":"ペンデュラム",
                      "儀式/モンスター":"儀式",
                      "シンクロ/ペンデュラム/効果":"シンクロ/ペンデュラム",
                      "ペンデュラム/通常/モンスター":"ペンデュラム",
                      "通常/モンスター":"通常"
                      }
"儀式/ペンデュラム/効果"
"効果/モンスター"
##zokusei wakeru syori
df = pd.read_csv('./work/01_card_name.txt', names=('card','ruby','attribute1','attribute2','effect'))
print (df)

df['ruby'] = pd.read_csv('./work/02_card_ruby.txt',header=None)
print("ruby set OK")
tab_df = pd.read_csv('./work/03_card_attribute.txt',delimiter='\t',names=('Column1','Column2','column3'))
print("tab_df set OK")
df['attribute1'] = tab_df['Column1']
df['attribute2'] = tab_df['Column2']
df['effect'] = pd.read_csv('./work/04_card_effect.txt',header=None)
df.insert(0,'属性2',"")
df.insert(0,'属性1',"")
print(df)
df.to_csv('tmp.csv')

#属性1の分類
for index, row in df.iterrows():
    print(row['attribute1'].find("魔法"))
    if(row['attribute1'].find("魔法") >= 0):
        df.iat[index,0] = '魔法'
    elif(row['attribute1'].find("罠") >= 0):
        df.iat[index,0] = '罠'
    else:
        df.iat[index,0] = 'モンスター'
df.to_csv('tmp.csv')

#属性2の分類
    #魔法or罠=>attribute2の～～を見て設定
    #モンスター=>抽出したdictionaryで値を設定
for index, row in df.iterrows():
    if(row['属性1'].find("魔法") >= 0):
        target = str(row["attribute2"])
        start_index = target.find('alt="')
        end_index =  target.find('" title=')
        zokusei2 = str(row['attribute2'])[start_index+len('alt="'):end_index]
        df.iat[index,1] = zokusei2 or '通常'
    elif(row['属性1'].find("罠") >= 0):
        target = str(row["attribute2"])
        start_index = target.find('alt="')
        end_index =  target.find('" title=')
        zokusei2 = str(row['attribute2'])[start_index+len('alt="'):end_index]
        df.iat[index,1] = zokusei2 or '通常'
    elif(row['属性1'].find("モンスター") >= 0):
        target = str(row["effect"])
        start_index = target.find('alt="')
        end_index =  target.find('" title=')
        zokusei2 = str(row['effect'])[start_index+len('alt="'):end_index]
        # print("df.iat[index,1] = monster_syurui_dic[zokusei2] or '不明な属性'で落ちる場合、dicにkeyの種族を設定して、valueいれて")
        df.iat[index,1] = monster_syurui_dic[zokusei2] or '不明な属性'
df.to_csv('tmp.csv')
df.to_excel('./output/pandas_excel.xlsx',columns=['属性1','属性2','card','ruby'],index=False)