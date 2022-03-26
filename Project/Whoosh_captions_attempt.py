import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser
import json

schema = Schema(index=NUMERIC(stored=True), word=TEXT(stored=True), 
                        start=NUMERIC(stored = True))
if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
ix = create_in("indexdir",schema)
writer = ix.writer()


f = open(r"C:\users\sbyro\hello\225_captions.json")  # I used a Physics 225 lecture I watched last semester
g = f.read()
f.close()


g = g[1:-2]  # remove beginnning and ending brackets
g = g.split("},")  #split into mini documents to parse

for i in range(len(g)):
    g[i] = g[i] + "}"  # add back the } I used to split it

print(len(g))  # 7504 words it kind of a lot to search through. It takes a while.

for i in range(len(g)):
    h = json.loads(g[i])   # turn json file into a python dictionary
    g[i] = h
    writer.add_document(index = int(h['i']), word = h['w'], start = int(h['s']))
writer.commit()



input = "pure time dilation"
input = input.split(" ")
with ix.searcher() as searcher:
     query = QueryParser("word", ix.schema).parse(input[0])
     results = searcher.search(query, terms=True)
     count = 0
     real_results = []
     for r in results:
         real_results.append(r)
         for l in range(1, len(input)):
             index = l + r['index']
             next_word = (g[index]['w'][0:len(input[l])])
             if (next_word != input[l]):
                 real_results.remove(r)
                 count -= 1
                 break
         count += 1
     print(f'You have {count} matches for "{" ".join(input)}" at: ')
for i in range(len(real_results)):
    print(real_results[i]['start'])