"""

Main code, to process text and do stuff with it.

"""

__author__ = "Arya Kumar"
__email__ = "thearyaskumar@gmail.com"
__date__ = "09/07/19"

import json
import spacy
import fasttext
import urllib.request
from time import time
from bs4 import BeautifulSoup

# load things:
VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789.?! ")
nlp = spacy.load("en")
model = fasttext.load_model("model_100000.ftz")

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
        self._url = self._gather_url(self._gather_keyword(rawtext))

    def _gather_keyword(self, rawtext):
        # just pick out the sentence that is most likely to be an image call:
        doc = nlp(preprocess_text(rawtext))
        sentences = [s.text for s in doc.sents]
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

        # TODO: some smarter keyword gathering.
        return "iphone vs android"

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

    def genre(self):
        return "image"

    def url(self):
        return self._url


class Summary:
    def __init__(self, rawtext):
        self._summary = self._generate_summary(rawtext)

    def _generate_summary(self, rawtext):
        # TODO: Generate a summary from the larger rawtext.
        pass

    def genre(self):
        return "summary"

    def summarized_text(self):
        return self._summary


class Title:
    def __init__(self, rawtext):
        self._title = self._generate_title(rawtext)

    def _generate_title(self, rawtext):
        # TODO: Generate a Title from the larger rawtext
        pass

    def genre(self):
        return "title"

    def title(self):
        return self._title


def gen_element(speech, slide_is_blank=False):
    """ Process the speech and generate the relevant element. """

    if slide_is_blank:
        return print("I THINK I SHOULD RETURN A TITLE")

    # if it is an image, then return an image immediately:
    cleaned_text = preprocess_text(speech)
    if model.predict(cleaned_text)[0][0] == "__label__image":
        print("I THINK THIS IS AN IMAGE")
        return Image(speech).url()
    else:
        return print("I THINK I SHOULD RETURN SOME BULLET POINTS.")


if __name__ == "__main__":
    start = time()
    print(gen_element("you can see a picture of a tree"))
    print(time() - start)
