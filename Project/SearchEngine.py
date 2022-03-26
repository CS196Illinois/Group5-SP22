from typing import Dict, List, Sequence

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh.filedb.filestore import RamStorage
from whoosh.analysis import StemmingAnalyzer

import json

class SearchEngine:
    def __init__(self, schema):
        self.schema = schema
        schema.add('raw', TEXT(stored=True))
        self.ix = RamStorage().create_index(self.schema)

    def index_documents(self, docs: Sequence):
        writer = self.ix.writer()
        for doc in docs:
            d = {k: v for k,v in doc.items() if k in self.schema.stored_names()}
            d['raw'] = json.dumps(doc) # raw version of all of doc
            writer.add_document(**d)
        writer.commit(optimize=True)

    def get_index_size(self) -> int:
        return self.ix.doc_count_all()

    def query(self, q: str, fields: Sequence, highlight: bool=True) -> List[Dict]:
        search_results = []
        with self.ix.searcher() as searcher:
            results = searcher.search(MultifieldParser(fields, schema=self.schema).parse(q))
            for r in results:
                d = json.loads(r['raw'])
                if highlight:
                    for f in fields:
                        if r[f] and isinstance(r[f], str):
                            d[f] = r.highlights(f) or r[f]

                search_results.append(d)

        return search_results



def main(path_to_file: str):
    schema = Schema(
        id=ID(stored=True),
        sentence=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        start=NUMERIC(stored=True),
        end=NUMERIC(stored=True)
    )


    try:

        file = open(path_to_file)
        docs = json.loads(file.read())
        file.close()

        engine = SearchEngine(schema)
        engine.index_documents(docs)



        fields_to_search = ["sentence"]

        for q in ["left child", "node"]:
            print(f"Query:: {q}")
            print("\t", engine.query(q, fields_to_search, highlight=True))
            print("-"*70)


        for idx, item in enumerate(docs):
            item['id'] = str(idx)

    except:
        print("File not found!")


if __name__ == "__main__":
    main("./225.json")

