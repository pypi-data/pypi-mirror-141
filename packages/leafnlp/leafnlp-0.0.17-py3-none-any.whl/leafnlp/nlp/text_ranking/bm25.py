# Copyright 2021 The LeafNLP Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The codes in this file are modified based on 
https://github.com/dorianbrown/rank_bm25.
Paper: Trotmam et al, Improvements to BM25 and Language Models Examined
"""

import math
from multiprocessing import Pool, cpu_count
from typing import List

import numpy as np


class BM25(object):
    """A Basic BM25.

    Args:
        * ``corpus`` (**List**): Corpus.
        * ``tokenizer`` (_type_, optional): _description_. Defaults to None.
    """

    def __init__(self,
                 corpus: List,
                 tokenizer=None):

        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.tokenizer = tokenizer

        if tokenizer:
            corpus = self._tokenize_corpus(corpus)

        nd = self._initialize(corpus)
        self._calc_idf(nd)

    def _initialize(self,
                    corpus: List):
        """_summary_

        Args:
            * ``corpus`` (List): _description_

        Returns:
            _type_: _description_
        """
        nd = {}  # word -> number of documents with word
        num_doc = 0
        for document in corpus:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                try:
                    nd[word] += 1
                except KeyError:
                    nd[word] = 1

        self.avgdl = num_doc / self.corpus_size

        return nd

    def _tokenize_corpus(self,
                         corpus: List):
        """_summary_

        Args:
            * ``corpus`` (**List**)

        Returns:
            _type_: _description_
        """
        pool = Pool(cpu_count())
        tokenized_corpus = pool.map(self.tokenizer, corpus)

        return tokenized_corpus

    def _calc_idf(self, nd):
        """_summary_

        Args:
            * ``nd`` (_type_): _description_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    def get_scores(self,
                   query: str):
        """Calculate bm25 scores between query and all documents.

        Args:
            * ``query`` (**str**)
        """
        raise NotImplementedError()

    def get_batch_scores(self,
                         query: str,
                         doc_ids: List):
        """Calculate bm25 scores between query and subset of all documents.

        Args:
            * ``query`` (**str**)
            * ``doc_ids`` (**List**)
        """
        raise NotImplementedError()

    def get_top_n(self,
                  query: str,
                  documents: List,
                  n: int = 5):
        """Get the most n relevant documents.

        Args:
            * ``query`` (**str**)
            * ``documents`` (**List**)
            * ``n`` (**int**, optional). Defaults to 5.

        Returns:
            * documents
        """
        assert self.corpus_size == len(documents)

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [documents[i] for i in top_n]


class BM25Okapi(BM25):
    """Okapi BM25

    Args:
        * ``corpus`` (**List**): Corpus
        * ``tokenizer`` (_type_, optional). Defaults to None.
        * ``k1`` (**float**, optional). Defaults to 1.5.
        * ``b`` (**float**, optional). Defaults to 0.75.
        * ``epsilon`` (**float**, optional). Defaults to 0.25.
    """

    def __init__(self,
                 corpus: List,
                 tokenizer=None,
                 k1: float = 1.5,
                 b: float = 0.75,
                 epsilon: float = 0.25):

        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__(corpus, tokenizer)

    def _calc_idf(self, nd):
        """Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf

        Args:
            * ``nd`` (_type_): _description_
        """

        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - \
                math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_scores(self,
                   query: str):
        """Calculate bm25 scores between query and all documents.

        Args:
            * ``query`` (**str**)

        Returns:
            * scores
        """

        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score

    def get_batch_scores(self,
                         query: str,
                         doc_ids: List):
        """Calculate bm25 scores between query and subset of all documents.

        Args:
            * ``query`` (**str**)
            * ``doc_ids`` (**List**)

        Returns:
            * scores
        """

        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0)
                               for di in doc_ids])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score.tolist()


class BM25L(BM25):
    """_summary_

    Args:
        * ``corpus`` (**List**): _description_
        * ``tokenizer`` (_type_, optional): _description_. Defaults to None.
        * ``k1`` (**float**, optional): _description_. Defaults to 1.5.
        * ``b`` (**float**, optional): _description_. Defaults to 0.75.
        * ``delta`` (**float**, optional): _description_. Defaults to 0.5.
    """

    def __init__(self,
                 corpus: List,
                 tokenizer=None,
                 k1: float = 1.5,
                 b: float = 0.75,
                 delta: float = 0.5):

        # Algorithm specific parameters
        self.k1 = k1
        self.b = b
        self.delta = delta
        super().__init__(corpus, tokenizer)

    def _calc_idf(self, nd):
        """_summary_

        Args:
            * ``nd`` (_type_): _description_
        """

        for word, freq in nd.items():
            idf = math.log(self.corpus_size + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf

    def get_scores(self,
                   query: str):
        """Calculate bm25 scores between query and all documents.

        Args:
            * ``query`` (**str**)

        Returns:
            * scores
        """

        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            ctd = q_freq / (1 - self.b + self.b * doc_len / self.avgdl)
            score += (self.idf.get(q) or 0) * q_freq * (self.k1 + 1) * (ctd + self.delta) / \
                     (self.k1 + ctd + self.delta)

        return score

    def get_batch_scores(self,
                         query: str,
                         doc_ids: List):
        """Calculate bm25 scores between query and subset of all documents.

        Args:
            * ``query`` (**str**)
            * ``doc_ids`` (**List**)

        Returns:
            * scores
        """

        assert all(di < len(self.doc_freqs) for di in doc_ids)

        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0)
                               for di in doc_ids])
            ctd = q_freq / (1 - self.b + self.b * doc_len / self.avgdl)
            score += (self.idf.get(q) or 0) * q_freq * (self.k1 + 1) * (ctd + self.delta) / \
                     (self.k1 + ctd + self.delta)

        return score.tolist()


class BM25Plus(BM25):
    """_summary_

    Args:
        * ``corpus`` (**List**): _description_
        * ``tokenizer`` (_type_, optional): _description_. Defaults to None.
        * ``k1`` (**float**, optional): _description_. Defaults to 1.5.
        * ``b`` (**float**, optional): _description_. Defaults to 0.75.
        * ``delta`` (**float**, optional): _description_. Defaults to 1.
    """

    def __init__(self,
                 corpus: List,
                 tokenizer=None,
                 k1: float = 1.5,
                 b: float = 0.75,
                 delta: float = 1):
        # Algorithm specific parameters
        self.k1 = k1
        self.b = b
        self.delta = delta
        super().__init__(corpus, tokenizer)

    def _calc_idf(self, nd):
        """_summary_

        Args:
            * ``nd`` (_type_): _description_
        """
        for word, freq in nd.items():
            idf = math.log(self.corpus_size + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf

    def get_scores(self,
                   query: str):
        """Calculate bm25 scores between query and all documents.

        Args:
            * ``query`` (**str**)

        Returns:
            * scores
        """
        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
                                               (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
        return score

    def get_batch_scores(self,
                         query: str,
                         doc_ids: List):
        """Calculate bm25 scores between query and subset of all documents.

        Args:
            * ``query`` (**str**)
            * ``doc_ids`` (**List**)

        Returns:
            * scores
        """

        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0)
                               for di in doc_ids])
            score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
                                               (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
        return score.tolist()
