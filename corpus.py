import re


def read_corpus(filename):
    with open(filename,"r",encoding="utf-8") as file:
        data=file.read()

    documents=re.findall(r"<DOC>(.*?)</DOC>",data,re.DOTALL)

    corpus={}

    for doc in documents:
        docid=re.search(r"<DOCID>(.*?)</DOCID>",doc).group(1)
        category=re.search(r"<CATEGORY>(.*?)</CATEGORY>",doc).group(1)
        title=re.search(r"<TITLE>(.*?)</TITLE>",doc).group(1)
        text=re.search(r"<TEXT>(.*?)</TEXT>",doc,re.DOTALL).group(1)

        corpus[docid]={
            "category":category,
            "title":title,
            "text":text
        }

    return corpus