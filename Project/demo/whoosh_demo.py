# Reference: Tutoiral from Whoosh 2.7 Quick Start Doc:
# https://whoosh.readthedocs.io/en/latest/quickstart.html

# Import lib

from whoosh.index import create_in
from whoosh.fields import *
import os

# Indexing
# The keyword arguments map field names to the values to index/store:

if not os.path.exists("index"):
    os.mkdir("index")
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()

writer.add_document(title=u"First document", path=u"/a", 
                    content=u"This is the first doc")
writer.add_document(title=u"Second document", path=u"/b", 
                    content=u"This is the second doc")

writer.commit()

# Searching

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("first")
    results = searcher.search(query)
    print(results[0])

# Indexing using Metadata Example: indexing Chinese Character
# jieba is a Chinese Words Segementation Utilities

from whoosh.fields import TEXT, SchemaClass
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()
class ArticleSchema(SchemaClass):
    title = TEXT(stored=True, analyzer=analyzer)
    content = TEXT(stored=True, analyzer=analyzer)
    author = TEXT(stored=True, analyzer=analyzer)

# Adding data

schema = ArticleSchema()
ix = create_in("indexdir", schema, indexname='article_index')
writer = ix.writer()
writer.add_document(title="登鹳雀楼", author="王之涣",content="白日依山尽,黄河入海流,欲穷千里目,更上一层楼")
writer.add_document(title="登高", author="杜甫", content="风急天高猿啸哀,渚清沙白鸟飞回")
writer.add_document(title="胡乱写的", author="黄河恋", content="展示效果")
writer.commit()

# Searching

from whoosh.qparser import QueryParser
from whoosh.index import open_dir

ix = open_dir("indexdir", indexname='article_index')
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("一层")
    results = searcher.search(query)
    print(results[0])

# Highlighting
# You can use HTML to customize the match and term0

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("黄河")
    results = searcher.search(query)
    data = results[0]
    text = data.highlights("content")
    print("Demo for highlighting effect:")
    print(text)

# Search multiple index with MultifieldParser

from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.index import open_dir

ix = open_dir("indexdir", indexname='article_index')
with ix.searcher() as searcher:
    query = MultifieldParser(["content", 'author'], ix.schema).parse("黄河")
    results = searcher.search(query)
    print("There will be two results here:")
    for data in results:
        print(data)

# Exploring multiple keywords...
# Note that Whoosh will split the word and run them as condition:
# It means that MATCHING ONLY IF ALL THE WORDS ARE MATCHED!

# Example:
query = MultifieldParser(["content", 'author'], ix.schema).parse("黄河 杜甫")
# It will be split to:
# ((content:黄河 OR author:黄河) AND (content:杜甫 OR author:杜甫))

# Thus we need to staighten the logic:

from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.index import open_dir
from whoosh.query import compound, Term

ix = open_dir("indexdir", indexname='article_index')
with ix.searcher() as searcher:
    author_query = [Term('author', '黄河'), Term('author', '杜甫')]
    content_query = [Term('content', '黄河'), Term('content', '杜甫')]
    query = compound.Or([compound.Or(author_query), compound.Or(content_query)])
    print(query)
    results = searcher.search(query)
    for data in results:
        print(data)





