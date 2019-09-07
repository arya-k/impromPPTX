"""

Main code, to process text and do stuff with it.

"""

__author__ = "Arya Kumar"
__email__ = "thearyaskumar@gmail.com"
__date__ = "09/07/19"

import fasttext

#####################
# Class definitions #
#####################

VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789.?! ")


class Image:
    def __init__(self, rawtext):
        self._url = self._gather_url(self._gather_keyword(rawtext))

    def _gather_keyword(self, rawtext):
        # TODO: Process the keyword from the rawtext.
        pass

    def _gather_url(self, keyword):
        # TODO: Return the URL found from an image searching through google images
        pass

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


def preprocess_text(text):
    """ simplify the text before fasttext processing. """
    return "".join(c for c in text.lower() if c in VALID_CHARS)


def gen_element(speech, slide_is_blank=False):
    """ Process the speech and generate the relevant element. """

    # if it is an image, then return an image immediately:
    cleaned_text = preprocess_text(speech)
    if model.predict(cleaned_text)[0][0] == "__label__image":
        print("I THINK THIS IS AN IMAGE")
    else:
        print("I THINK THIS IS SOME TEXT")


model = fasttext.load_model("model_100000.ftz")
if __name__ == "__main__":
    gen_element("you can see a platypuss here")
