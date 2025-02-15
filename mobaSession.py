import json
import csv

def excelToJson(folder, fileName = 'session', passWord = ''):
    strStart = """[Bookmarks]
SubRep=
ImgNum=600"""
    # name = #109#0%ipAddress%22%loginName%%-1%-1%%%%%0%0%0%passWord%%-1%0%0%0%%1080%%0%0%1%%0%%%%0%-1%-1%0#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%0%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%0%-1%0%#0# #-1'
    sessionItem = f"""
name = #109#0%ipAddr%22%userName%%-1%-1%%%%%0%0%0%password%%-1%0%0%0%%1080%%0%0%1%%0%%%%0%-1%-1%0#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%0%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%0%-1%0%#0# #-1"""
    strEnd = """
"""

    scpItem = """scp -r ubuntu@ipAddr:/home/ubuntu/nillion/verifier/credentials.json """

    print(strStart + sessionItem + strEnd)
    index = 0
    p = strStart
    scp = ""
    with open(f'{folder}/{fileName}.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if passWord == '':
                passWord = row[8]
            if index != 0 and index % 10 == 0:
                p += strEnd
                # data=json.dumps(p, ensure_ascii=False)
                # print(data.replace("\\",""))
                with open(f'{folder}/{fileName}_{index}.mxtsessions',"w",encoding='utf-8') as f:
                    f.write(p)

                p = strStart

            index += 1

            item = sessionItem.replace('name', row[2])
            item = item.replace('ipAddr', row[3])
            item = item.replace('userName', 'ubuntu')
            item = item.replace('password', passWord)
            p += item
            print(p)
            scp += scpItem.replace('ipAddr', row[3]) + row[2] + """.json
            """

    if (index - 1) % 10 != 0:
        p += strEnd
        # data=json.dumps(p, ensure_ascii=False)
        # print(data.replace("\\",""))
        with open(f'{folder}/{fileName}_{index}.mxtsessions',"w",encoding='utf-8') as f:
            f.write(p)

    with open(f'{folder}/{fileName}_scp.sh',"w") as f:
        f.write(scp)


if __name__ == "__main__":
    excelToJson("ld", "nillion_ld200", 'Buymail001++')