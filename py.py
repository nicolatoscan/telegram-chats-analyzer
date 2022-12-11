# %% imports
import json
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
import pandas as pd

# %% load json file
def getData():
    with open('data/result.json') as f:
        return json.load(f)
data = getData()
chats = data['chats']['list']

# %%
def activeUserNumber(chat):
    return len( set([m['from'] for m in chat['messages'] if 'from' in m ]) )
def findNameIds(name):
    return [
        (c['name'], c['id'], len(c['messages']))
        for c in chats if ('name' in c) and c['name'] and c['name'].lower().startswith(name.lower())
    ]
def getChatFromId(chatId):
    return [c for c in chats if c['id'] == chatId][0]
def getTimestampsFromChat(chatId):
    chat = getChatFromId(chatId)
    return sorted([m['date'] for m in chat['messages']])

# chats stuff
types = Counter()
for c in chats:
    types.update([c['type']])
print(types)
pChats = [c for c in chats if c['type'] == 'personal_chat']
groups = [c for c in chats if c['type'] == 'private_group']
sGroups = [c for c in chats if c['type'] == 'private_supergroup']
sm = [c for c in chats if c['type'] == 'saved_messages']
pChats = [c for c in pChats if activeUserNumber(c) == 2]
# %% plot hist of chats lengths
# plt.hist([len(c['messages']) for c in pChats], bins=20)
# plt.show()



# %%
findNameIds('Name')

# %% plot chat
def plotIntensity(chatId):
    times = getTimestampsFromChat(chatId)
    months = Counter([t[:7] + '-01T00:00:00' for t in times])
    sortedMonths = sorted(months.keys())
    rangeMonth = pd.date_range(sortedMonths[0], sortedMonths[-1], freq='MS').strftime("%Y-%m-01T00:00:00").tolist()
    freqMonths = [months[m] if m in months else 0 for m in rangeMonth]
    print(months)
    print(freqMonths)

    plt.plot([ datetime.fromisoformat(m) for m in rangeMonth], freqMonths)
    plt.show()
# plotIntensity(1)

# %% plot chat
def plotIntensityAllChats():
    months = Counter()
    for c in tqdm(pChats):
        times = getTimestampsFromChat(c['id'])
        m = Counter([datetime.fromisoformat(t[:7] + '-01T00:00:00') for t in times])
        months.update(m)
    sortedM = sorted(list(zip(months.keys(), months.values())))
    plt.plot([x[0] for x in sortedM], [x[1] for x in sortedM])
    plt.show()


# %% ration of messages
def ratio(chat):
    messages = chat['messages']
    froms = Counter([m['from'] for m in messages if 'from' in m])
    return (froms['Nicola Toscan'] / len(messages), list(froms.keys()))
ratioList = [ratio(c) for c in pChats]

def totalRatio(fromName='Nicola Toscan'):
    messages = [m for c in pChats for m in c['messages'] if 'from' in m]
    froms = Counter([m['from'] for m in messages])
    if fromName == 'Nicola Toscan':
        return froms[fromName] / len(messages)
    else:
        return froms[fromName] / ( len(messages) - froms['Nicola Toscan'] )
print('Total Ratio: ', totalRatio())
# %%

def ratioList():
    messages = [m for c in pChats for m in c['messages'] if 'from' in m and m['from'] is not None]
    froms = Counter([m['from'] for m in messages])
    return [
        (froms[f] / ( len(messages) - froms['Nicola Toscan']), f)
        for f in froms
    ]
df = pd.DataFrame(ratioList(), columns=['ratio', 'name'])
df = df.sort_values(by=['ratio'], ascending=False)
# print each line as table
for i, row in df.iterrows():
    print(f'{row["name"].rjust(35, " ")}\t\t{row["ratio"]:.5f} ')




# %%
