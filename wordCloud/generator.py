# Imports
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from collections import Counter
from scipy.sparse import coo_matrix

# Collectively worked by all the Group Members
# Structure of the project and Control Flow by Hithesh
# Word Info Generation by Dilip
# Feature Extraction and Core Logic by Alexandra


# Hithesh
class CreateMappings:
    def __init__(self):
        try:
            nltk.download("stopwords")
            nltk.download("wordnet")
        except Exception as e:
            print("Encountered Package Errors: ", e)

        self.movies = pd.read_csv("./wordCloud/wiki_movie_plots_deduped.csv")
        self.movies["Plot_word_count"] = self.movies["Plot"].apply(
            lambda x: len(str(x).split(" "))
        )
        self.movies.drop(
            self.movies[self.movies["Genre"] == "unknown"].index, inplace=True
        )

        # Important Genres : Sci-Fi, Action, Drama, Comedy, Biography, Adventure, Romance, Musical
        root_genres = ["sci", "act", "dra", "com", "bio", "adv", "rom", "music"]
        self.mappings = dict()
        start_year = 1900
        year_range = str(start_year) + "-" + str(start_year + 10)
        self.mappings[year_range] = dict()

        # create mappings
        for row in self.movies.itertuples():
            r = row._asdict()

            if r["_1"] > (start_year + 10):
                start_year += 10
                year_range = str(start_year) + "-" + str(start_year + 10)
                self.mappings[year_range] = dict()

            tmp = dict()

            for genre in root_genres:
                if genre in r["Genre"].lower():
                    tmp["title"] = r["Title"]
                    tmp["director"] = r["Director"]
                    tmp["wiki"] = r["_7"]
                    tmp["plot"] = r["Plot"]
                    tmp["releasedIn"] = r["_1"]
                    tmp["plot_word_count"] = r["Plot_word_count"]
                    if genre in self.mappings[year_range].keys():
                        self.mappings[year_range][genre].append(tmp)
                    else:
                        self.mappings[year_range][genre] = [tmp]


# Hithesh
class Generator:
    def __init__(self, mappings):
        self.mappings = mappings

    # Text Processing
    def process(self, year_range, genre, query_type, num_words):

        ##Creating a list of stop words and adding custom stopwords
        self.stop_words = set(stopwords.words("english"))
        ##Creating a list of custom stopwords
        new_words = [
            "using",
            "show",
            "result",
            "large",
            "also",
            "iv",
            "one",
            "two",
            "new",
            "previously",
            "shown",
        ]
        self.stop_words = self.stop_words.union(new_words)

        corpus = Generator.Corpus_Generator(self, year_range, genre)

        if query_type == "top_words":
            if len(corpus) == 0:
                return {
                    "top_words": [],
                    "top_words_freq": [],
                    "movie_list": [],
                }
            top_words = Generator.get_top_n_words(self, corpus, n=int(num_words))
            top_df = pd.DataFrame(top_words)
            top_df.columns = ["Word", "Freq"]
            wList = top_df["Word"].to_list()
            wList = " ".join(wList)
            wList = wList.split(" ")
            hover_data = Generator.getInfo(self, wList, year_range, genre)

            return {
                "top_words": top_df["Word"].to_list(),
                "top_words_freq": top_df["Freq"].to_list(),
                "movie_list": hover_data,
            }

        elif query_type == "bi_grams":
            if len(corpus) == 0:
                return {
                    "bi_grams": [],
                    "bi_grams_freq": [],
                    "movie_list": [],
                }
            top2_words = Generator.get_top_n2_words(self, corpus, n=int(num_words))
            top2_df = pd.DataFrame(top2_words)
            top2_df.columns = ["bi_grams", "Freq"]
            wList = top2_df["bi_grams"].to_list()
            wList = " ".join(wList)
            wList = wList.split(" ")
            hover_data = Generator.getInfo(self, wList, year_range, genre)

            return {
                "bi_grams": top2_df["bi_grams"].to_list(),
                "bi_grams_freq": top2_df["Freq"].to_list(),
                "movie_list": hover_data,
            }

        if len(corpus) == 0:
            return {
                "tri_gram": [],
                "tri_gram_freq": [],
                "movie_list": [],
            }
        top3_words = Generator.get_top_n3_words(self, corpus, n=int(num_words))
        top3_df = pd.DataFrame(top3_words)
        top3_df.columns = ["Tri-gram", "Freq"]
        wList = top3_df["Tri-gram"].to_list()
        wList = " ".join(wList)
        wList = wList.split(" ")
        hover_data = Generator.getInfo(self, wList, year_range, genre)

        return {
            "tri_gram": top3_df["Tri-gram"].to_list(),
            "tri_gram_freq": top3_df["Freq"].to_list(),
            "movie_list": hover_data,
        }

    # Dilip
    def getInfo(self, words, year_range, genre):
        info = dict()
        for movie in self.mappings[year_range][genre]:
            for i in words:
                if i in movie["plot"].lower():
                    if i in info.keys():
                        if (
                            movie["title"],
                            movie["wiki"],
                            movie["releasedIn"],
                        ) not in info[i]:
                            info[i].append(
                                (movie["title"], movie["wiki"], movie["releasedIn"])
                            )
                    else:
                        info[i] = [(movie["title"], movie["wiki"], movie["releasedIn"])]
        return info

    # Alexandra
    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    # Alexandra
    def topKeywords(self, feature_names, sorted_items, topn):
        cv = CountVectorizer(
            max_df=0.8,
            stop_words=self.stop_words,
            max_features=10000,
            ngram_range=(1, 3),
        )

        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:

            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    # Alexandra
    def Corpus_Generator(self, year_range, genre):
        corpus = []
        if genre not in self.mappings[year_range].keys():
            return []
        for i in self.mappings[year_range][genre]:
            # Remove punctuations
            text = re.sub("[^a-zA-Z]", " ", i["plot"])

            # Convert to lowercase
            text = text.lower()

            # remove tags
            text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

            # remove special characters and digits
            text = re.sub("(\\d|\\W)+", " ", text)

            ##Convert to list from string
            text = text.split()

            ##Stemming
            ps = PorterStemmer()
            # Lemmatisation
            lem = WordNetLemmatizer()
            text = [lem.lemmatize(word) for word in text if not word in self.stop_words]
            text = " ".join(text)
            corpus.append(text)

        return corpus

    # Alexandra
    def get_top_n_words(self, corpus, n=None):
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [
            (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
        ]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        return words_freq[:n]

    # Alexandra
    def get_top_n2_words(self, corpus, n=None):
        vec1 = CountVectorizer(ngram_range=(2, 2), max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [
            (word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()
        ]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        return words_freq[:n]

    # Alexandra
    def get_top_n3_words(self, corpus, n=None):
        vec1 = CountVectorizer(ngram_range=(3, 3), max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [
            (word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()
        ]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        return words_freq[:n]
