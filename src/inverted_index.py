from src.preprocessing import preprocess


def build_inverted_index(corpus):
    index={}

    for docid,document in corpus.items():
        tokens=preprocess(document["text"])

        frequencies={}

        for i in range(len(tokens)):
            token=tokens[i]

            if token not in frequencies:
                frequencies[token]=0

            frequencies[token]+=1

        for term,tf in frequencies.items():
            if term not in index:
                index[term]={
                    "df":0,
                    "postings":[]
                }

            index[term]["df"]+=1

            index[term]["postings"].append({
                "docid":docid,
                "tf":tf
            })

    return index