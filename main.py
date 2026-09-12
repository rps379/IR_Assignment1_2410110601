from corpus import read_corpus
from src.preprocessing import preprocess
from src.inverted_index import build_inverted_index
from src.positional_index import build_positional_index
from search import search_free_text,find_phrase,find_proximity


def print_free_text_results(results):
    if len(results)==0:
        print("No results found.")
        return

    for i in range(len(results)):
        result=results[i]

        print(
            result["docid"],"|",
            result["title"],"|",
            result["category"],"| Score:",
            round(result["score"],4)
        )


def print_positional_results(results):
    if len(results)==0:
        print("No results found.")
        return

    for i in range(len(results)):
        result=results[i]

        print(
            result["docid"],"|",
            result["title"],"|",
            result["category"],"| Positions:",
            result["positions"]
        )


def main():
    corpus=read_corpus("corpus_100.txt")

    print("Total documents:",len(corpus))

    processed_corpus={}

    for docid,document in corpus.items():
        processed_corpus[docid]=preprocess(document["text"])

    print("Preprocessing completed.")

    print("\nSample preprocessed document:")
    first_docid=list(processed_corpus.keys())[0]

    print(first_docid)
    print(processed_corpus[first_docid][:30])

    index=build_inverted_index(corpus)

    print("\nInverted index completed.")
    print("Unique terms:",len(index))

    positional_index=build_positional_index(corpus)

    print("Positional index completed.")
    print("Positional terms:",len(positional_index))

    print("\nSample inverted index entries:")

    count=0

    for term,data in index.items():
        print(term,":",data)

        count+=1

        if count==5:
            break

    while True:
        print("\n===== CLOTHING SEARCH ENGINE =====")
        print("1. Free-text search")
        print("2. Exact phrase search")
        print("3. Proximity search")
        print("4. Exit")

        choice=input("Enter choice: ").strip()

        if choice=="1":
            query=input("Enter query: ")

            results=search_free_text(query,index,corpus)

            print("\nResults:")
            print_free_text_results(results)

        elif choice=="2":
            query=input("Enter phrase: ")

            results=find_phrase(query,corpus,positional_index)

            print("\nPhrase results:")
            print_positional_results(results)

        elif choice=="3":
            query=input("Enter proximity query: ")

            k=int(input("Enter maximum distance k: "))

            results=find_proximity(query,k,corpus,positional_index)

            print("\nProximity results:")
            print_positional_results(results)

        elif choice=="4":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


if __name__=="__main__":
    main()