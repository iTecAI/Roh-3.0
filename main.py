import json, random, threading, time

class Roh:
    def __init__(self,data,interval=60,store=True):
        self.data_path = data
        with open(data,'r') as f:
            self.data = json.load(f)
        self.previous = None
        if store:
            self.interval = 60
            self.stor_thread = threading.Thread(name='store_thread',target=self._store)
            self.stor_thread.start()
    def _store(self):
        time.sleep(self.interval)
        with open(self.data_path,'w') as f:
            json.dump(self.data,f)

    def interpret(self,text):
        parts = ''.join([n for n in text.lower() if n in 'qwertyuiopasdfghjklzxcvbnm ']).split(' ')
        results = []
        for part in parts:
            if part in self.data.keys():
                for item in self.data[part]:
                    match_percent = int(len([x for x in parts if x in item[0]])/len(item[0])*100)
                    for res in item[1]:
                        results.append([res,match_percent])
        
        choices = []
        for result in results:
            choices.extend([result[0] for i in range(result[1]) if result[1] > 40])
        if len(choices) == 0:
            output = random.choice(random.choice(self.data[random.choice(list(self.data.keys()))])[1])
        else:
            output = random.choice(choices)
        if not self.previous == None:
            for part in self.previous:
                if len(part) >= 2:
                    if not part in self.data.keys():
                        self.data[part] = []
                    found = False
                    for i in range(len(self.data[part])):
                        if [x for x in list(set(self.previous)) if len(x) >= 2] == self.data[part][i][0]:
                            self.data[part][i][1].append(text)
                            found = True
                            break
                    if not found:
                        self.data[part].append([
                            [x for x in list(set(self.previous)) if len(x) >= 2],
                            [text]
                        ])
        
        self.previous = ''.join([n for n in output.lower() if n in 'qwertyuiopasdfghjklzxcvbnm ']).split(' ')
        return output
        

r = Roh('data.json')
while True:
    print(r.interpret(input('>> ')))