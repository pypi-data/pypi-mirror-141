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


def count_tokens(tokens: list):
    """count frequency of tokens.

    Args:
        * ``tokens`` (**list**): _description_

    Returns:
        **int**: counter
    """

    counter = {}
    for t in tokens:
        if t in counter.keys():
            counter[t] += 1
        else:
            counter[t] = 1

    return counter


def string_matching_f1_score(text_a: str, text_b: str):
    """Some codes and ideas are borrowed from 
    https://github.com/microsoft/unilm

    Args:
        * ``text_a`` (**str**): text A
        * ``text_b`` (**str**): text B

    Returns:
        **float**: score
    """

    tokens_a = text_a.lower().split()
    tokens_b = text_b.lower().split()
    if len(tokens_a) == 0 or len(tokens_b) == 0:
        return 1 if len(tokens_a) == len(tokens_b) else 0
    set_a = count_tokens(tokens_a)
    set_b = count_tokens(tokens_b)
    match = 0
    for token in set_a.keys():
        if token in set_b.keys():
            match += min(set_a[token], set_b[token])
    p = match / len(tokens_a)
    r = match / len(tokens_b)

    return 2.0 * p * r / (p + r + 1e-5)
