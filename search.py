import math
from src.preprocessing import preprocess
from collections import Counter

def get_query_terms(query):
    return preprocess(query)


def search_free_text(query,index,corpus):
    print(list(index.keys())[:50])
    print(preprocess("cotton shirt"))
    query_terms=preprocess(query)
    if len(query_terms)==0:
        return []

    query_tf=Counter(query_terms)
    query_weights={}
    query_length=0

    for term,tf in query_tf.items():
        if term not in index:
            continue
        df=index[term]["df"]
        weight=(1+math.log10(tf))*math.log10(100/df)
        query_weights[term]=weight
        query_length+=weight*weight

    if len(query_weights)==0:
        return []

    query_length=math.sqrt(query_length)

    document_lengths={}

    for term,data in index.items():
        for posting in data["postings"]:
            docid=posting["docid"]
            tf=posting["tf"]
            weight=1+math.log10(tf)

            if docid not in document_lengths:
                document_lengths[docid]=0

            document_lengths[docid]+=weight*weight

    for docid in document_lengths:
        document_lengths[docid]=math.sqrt(document_lengths[docid])

    scores={}

    for term,q_weight in query_weights.items():
        for posting in index[term]["postings"]:
            docid=posting["docid"]
            tf=posting["tf"]
            d_weight=1+math.log10(tf)

            if docid not in scores:
                scores[docid]=0

            scores[docid]+=d_weight*q_weight

    results=[]

    for docid,dot_product in scores.items():
        denominator=document_lengths[docid]*query_length

        if denominator!=0:
            score=dot_product/denominator
            results.append({
                "docid":docid,
                "title":corpus[docid]["title"],
                "category":corpus[docid]["category"],
                "score":score
            })

    results.sort(key=lambda x:(-x["score"],x["docid"]))

    return results[:10]


def find_phrase(query,corpus,positional_index):
    terms=get_query_terms(query)

    if len(terms)==0:
        return []

    results=[]

    for docid in corpus:
        positions=[]

        for i in range(len(terms)):
            term=terms[i]

            if term not in positional_index:
                positions=[]
                break

            if docid not in positional_index[term]:
                positions=[]
                break

            positions.append(positional_index[term][docid])

        if len(positions)!=len(terms):
            continue

        matches=[]

        for start in positions[0]:
            found=True

            for i in range(1,len(positions)):
                if start+i not in positions[i]:
                    found=False
                    break

            if found:
                matches.append(list(range(start,start+len(terms))))

        if len(matches)>0:
            results.append({
                "docid":docid,
                "title":corpus[docid]["title"],
                "category":corpus[docid]["category"],
                "positions":matches
            })

    return results


def find_proximity(query,k,corpus,positional_index):
    terms=get_query_terms(query)

    if len(terms)<2:
        return []

    results=[]

    for docid in corpus:
        positions=[]

        for i in range(len(terms)):
            term=terms[i]

            if term not in positional_index:
                positions=[]
                break

            if docid not in positional_index[term]:
                positions=[]
                break

            positions.append(positional_index[term][docid])

        if len(positions)!=len(terms):
            continue

        matches=[]

        for start in positions[0]:
            current=start
            match=[start]

            for i in range(1,len(positions)):
                valid_positions=[]

                for position in positions[i]:
                    if position>current and position-current<=k:
                        valid_positions.append(position)

                if len(valid_positions)==0:
                    match=[]
                    break

                current=min(valid_positions)
                match.append(current)

            if len(match)==len(terms):
                matches.append(match)

        if len(matches)>0:
            results.append({
                "docid":docid,
                "title":corpus[docid]["title"],
                "category":corpus[docid]["category"],
                "positions":matches
            })

    return results