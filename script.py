import os, json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

my_name = "John X"
path_to_json = '.../messages/inbox/...'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

data = {}

# we need both the json and an index number so use enumerate()
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)

        participants = json_text['participants']
        for p in participants:
            if p['name'] not in data:
                data[p['name']] = []

        messages = json_text['messages']
        for m in messages:
            if 'content' in m:
                data[m['sender_name']].append({
                    'message': m['content'],
                    # 'timestamp': int(datetime.fromtimestamp(m['timestamp_ms'] / 1000).strftime("%Y")) * 100 + int(datetime.fromtimestamp(m['timestamp_ms'] / 1000).strftime("%V")) *100/ 52
                    'timestamp': datetime.fromtimestamp(m['timestamp_ms'] / 1000).strftime("%Y %V")
                })

print(data.keys())

ks = list(data.keys())
ks.remove(my_name)
name = list(data.keys())[0]

print(len(data[my_name]))
print(len(data[name]))

times_m = [x['timestamp'] for x in data[my_name]]
times_a = [x['timestamp'] for x in data[name]]
msgl_m = [len(x['message']) for x in data[my_name]]
msgl_a = [len(x['message']) for x in data[name]]
msg_m = [1 for x in data[my_name]]
msg_a = [1 for x in data[name]]

df = pd.DataFrame({
    'timestamp': times_m,
    'msgl': msg_m
})

ax = df.groupby('timestamp').sum().plot(figsize=(20,10))
df2 = pd.DataFrame({
    'timestamp': times_a,
    'msgl': msg_a
})
df2.groupby('timestamp').sum().plot(ax=ax)
ax.legend([my_name, name])
ax.set_xlim(right=202300)
plt.show()
