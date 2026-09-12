from src.preprocessing import preprocess


def build_positional_index(corpus):
    index={}

    for docid,document in corpus.items():
        tokens=preprocess(document["text"])

        for i in range(len(tokens)):
            token=tokens[i]

            if token not in index:
                index[token]={}

            if docid not in index[token]:
                index[token][docid]=[]

            index[token][docid].append(i)

    return index