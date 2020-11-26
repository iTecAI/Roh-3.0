import json

with open('raw_data.json','r') as f:
    raw = json.load(f)

dialogs = []
for item in raw:
    if len(item['dialog']) > 3:
        dialog = []
        for d in item['dialog']:
            dialog.append(d['text'])
        dialogs.append(dialog)
print(len(dialogs))

processed = {}
last = None
c = 0
for dialog in dialogs:
    for item in dialog:
        if not last == None:
            for part in last:
                if len(part) >= 2:
                    if not part in processed.keys():
                        processed[part] = []
                    found = False
                    for i in range(len(processed[part])):
                        if [x for x in list(set(last)) if len(x) >= 2] == processed[part][i][0]:
                            processed[part][i][1].append(item)
                            found = True
                            break
                    if not found:
                        processed[part].append([
                            [x for x in list(set(last)) if len(x) >= 2],
                            [item]
                        ])
        last = ''.join([n for n in item.lower() if n in 'qwertyuiopasdfghjklzxcvbnm ']).split(' ')
    c+=1
    print(c,'/',len(dialogs),'-',len(dialog))

with open('data.json','w') as f:
    json.dump(processed,f,indent=4)
