import os

from corpus import read_corpus
from src.inverted_index import build_inverted_index
from src.positional_index import build_positional_index
from search import search_free_text, find_phrase, find_proximity


def main():
    corpus=read_corpus("corpus_100.txt")

    inverted_index=build_inverted_index(corpus)
    positional_index=build_positional_index(corpus)

    os.makedirs("report",exist_ok=True)

    free_queries=[
        "cotton shirt",
        "black t shirt",
        "women dress",
        "blue jeans",
        "winter jacket",
        "formal shirt",
        "summer dress",
        "hoodie",
        "cotton kurta",
        "denim pants",
        "xyzabc123"
    ]

    phrase_queries=[
        "cotton shirt",
        "stretch denim",
        "festive wear",
        "winter wear",
        "regular fit"
    ]

    proximity_queries=[
        ("cotton shirt",3),
        ("stretch denim",4),
        ("winter wear",3)
    ]

    with open("report/free_text_results.txt","w") as file:
        for query in free_queries:
            file.write("QUERY: "+query+"\n")
            results=search_free_text(query,inverted_index,corpus)

            if not results:
                file.write("No results\n\n")
                continue

            for result in results:
                file.write(
                    f"{result['docid']} | "
                    f"{result['title']} | "
                    f"{result['category']} | "
                    f"{result['score']:.4f}\n"
                )

            file.write("\n")

    with open("report/phrase_results.txt","w") as file:
        for query in phrase_queries:
            file.write("QUERY: "+query+"\n")
            results=find_phrase(query,positional_index,corpus)

            if not results:
                file.write("No results\n\n")
                continue

            for result in results:
                file.write(
                    f"{result['docid']} | "
                    f"{result['title']} | "
                    f"{result['category']} | "
                    f"{result['positions']}\n"
                )

            file.write("\n")

    with open("report/proximity_results.txt","w") as file:
        for query,k in proximity_queries:
            file.write(f"QUERY: {query} | k={k}\n")
            results=find_proximity(query,k,positional_index,corpus)

            if not results:
                file.write("No results\n\n")
                continue

            for result in results:
                file.write(
                    f"{result['docid']} | "
                    f"{result['title']} | "
                    f"{result['category']} | "
                    f"{result['positions']}\n"
                )

            file.write("\n")


if __name__=="__main__":
    main()