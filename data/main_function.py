"""

Main code, to process text and do stuff with it.

"""

__author__ = "Arya Kumar"
__email__ = "thearyaskumar@gmail.com"
__date__ = "09/07/19"

import json
import os
import spacy
import fasttext
import urllib.request
from time import time
from bs4 import BeautifulSoup
from collections import deque
from deepsegment import DeepSegment
from django.conf import settings

# load things:
VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789. ")
nlp = spacy.load("en_core_web_md")
merge_ncs = nlp.create_pipe("merge_noun_chunks")
merge_ents = nlp.create_pipe("merge_entities")
nlp.add_pipe(merge_ents)
nlp.add_pipe(merge_ncs)

model = fasttext.load_model(
    os.path.join(settings.BASE_DIR, "data", "model_1000000.ftz")
)
segmenter = DeepSegment("en")

########################
# Function definitions #
########################


def preprocess_text(text):
    """ simplify the text before fasttext processing. """
    return "".join(c for c in text.lower() if c in VALID_CHARS)


#####################
# Class definitions #
#####################


class Image:
    def __init__(self, rawtext):
        self.OPTIMAL_LENGTH = 3.9
        self._phrase = self._gather_keyword(rawtext)
        self._url = self._gather_url(self._phrase)

    def _gather_keyword(self, rawtext):
        # just pick out the sentence that is most likely to be an image call:
        doc = nlp(rawtext)
        sentences = [s.text for s in doc.sents]
        best_text = None
        if len(sentences) > 1:
            # pick the most important sentence
            predictions = [model.predict(s) for s in sentences]
            print([(p, s) for p, s in zip(predictions, sentences)])
            best_prediction = 0
            for i, p in enumerate(predictions):
                if p[0][0] == "__label__image":
                    if (
                        p[1][0] > predictions[best_prediction][1][0]
                        or predictions[best_prediction][0][0] != "__label__image"
                    ):
                        best_prediction = i
            best_text = sentences[best_prediction]
        else:
            best_text = preprocess_text(rawtext)

        return get_keyphrase(best_text, OPTIMAL_LENGTH=self.OPTIMAL_LENGTH)

    def _gather_url(self, keyword):
        soup = BeautifulSoup(
            urllib.request.urlopen(
                urllib.request.Request(
                    "http://www.bing.com/images/search?q="
                    + "+".join(keyword.split())
                    + "&FORM=HDRSC2",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
                    },
                )
            ),
            "html.parser",
        )

        return json.loads(soup.find("a", {"class": "iusc"})["m"])["murl"]

    def json(self):
        return {"genre": "image", "content": self._url}


class Summary:
    def __init__(self, rawtext):
        self._summary = self._generate_summary(rawtext)

    def _generate_summary(self, rawtext):
        doc = nlp(rawtext)

        roots = sorted(
            filter(lambda t: t.pos_ == "VERB", doc), key=lambda t: len(list(t.children))
        )
        already_covered = frozenset()

        def build_phrase(root):
            phrase = []
            processed_verbs = frozenset([root])
            added = False
            for child in root.children:
                if child in already_covered:
                    return -1, -1
                if child.i > root.i and not added:
                    phrase.append(root)
                    added = True
                if child.pos_ in ("VERB", "ADP"):
                    phrase_segment, new_processed_verbs = build_phrase(child)
                    if phrase_segment == -1:
                        return -1, -1
                    phrase.extend(phrase_segment)
                    processed_verbs |= new_processed_verbs
                elif child.pos_ not in ("PART", "INTJ", "DET") and (
                    child.pos_ != "ADV" or child.text in ("never", "not")
                ):
                    phrase.append(child)
            if not added:
                phrase.append(root)
            if len(phrase) <= 1:
                phrase = []
            return phrase, processed_verbs

        phrases = []
        while roots:
            root = roots.pop()
            broken = False
            phrase, processed_verbs = build_phrase(root)
            if phrase != -1:
                if phrase:
                    phrases.append(phrase)
                already_covered |= processed_verbs
                roots = list(filter(lambda t: t not in processed_verbs, roots))

        phrases.sort(key=lambda t: t[0].i)
        unsanitized = [" ".join(map(str, xs)) for xs in phrases]
        kindasanitized = [
            "".join(
                c for c in bullet.lower() if c.isdigit() or c.isalpha() or c.isspace()
            )
            for bullet in unsanitized
        ]
        mostlysanitized = [
            " ".join(c for c in bullet.split(" ") if c) for bullet in kindasanitized
        ]
        return [b.capitalize() for b in mostlysanitized]

    def json(self):
        return {"genre": "summary", "content": self._summary}


class Title:
    def __init__(self, rawtext):
        self.OPTIMAL_LENGTH = 2.9
        self._title = get_keyphrase(rawtext, OPTIMAL_LENGTH=self.OPTIMAL_LENGTH).title()

    def json(self):
        return {"genre": "title", "content": self._title}


class Graph:
    def json(self):
        return {"genre": "image", "content": "/graph/"}


def get_keyphrase(rawtext, OPTIMAL_LENGTH=2.9):
    def _from_verb(verb):
        phrase = []
        current = []
        for child in verb.children:
            if child.pos_ in ("NOUN", "VERB", "CCONJ", "ADP") and child.dep_ in (
                "cc",
                "pobj",
                "dobj",
                "conj",
                "xcomp",
                "pcomp",
                "advcl",
            ):
                current.extend(child.subtree)
            if child.pos_ in ("NOUN", "VERB"):
                phrase.extend(current)
                current = []
        return phrase if phrase else list(verb.subtree)

    doc = nlp(rawtext)

    candidate = None
    for verb in filter(lambda x: x.pos_ in ("VERB", "ADP"), doc):
        phrase = _from_verb(verb)
        if (
            phrase
            and any(
                token.pos_ in "NOUN" or token.dep_.endswith("comp") for token in phrase
            )
            and (
                not candidate
                or (
                    abs(len(phrase) - OPTIMAL_LENGTH)
                    < abs(len(candidate) - OPTIMAL_LENGTH)
                    and phrase
                )
            )
        ):
            candidate = phrase
    return " ".join(map(str, candidate))


def gen_element(speech, slide_is_blank=False):
    """ Process the speech and generate the relevant element. """
    # first, split the text into multiple sentences if possible:
    proc_speech = "".join(c for c in speech.lower() if c in VALID_CHARS)
    proc_speech = ". ".join(segmenter.segment(proc_speech))

    if slide_is_blank:
        return Title(proc_speech)

    # if it is a graph:
    if "correlat" in proc_speech or " graph" in proc_speech or "chart" in proc_speech:
        return Graph()

    # if it is an image, then return an image immediately:
    if model.predict(proc_speech)[0][0] == "__label__image":
        return Image(proc_speech)
    else:
        return Summary(proc_speech)


if __name__ == "__main__":
    print("\n\n\n\n\n\n\n\n\n\n")
    start = time()
    gen_element("you can tell there is a photograph".lower())
    print(time() - start)
