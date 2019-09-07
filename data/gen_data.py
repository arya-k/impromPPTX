"""

Simply generate the data

TODO: Consider determining title based on whether the slide is blank
      or based on the length of the content itself.

"""
import csv
import spacy
import inflect
import requests
import fasttext
from tqdm import tqdm
from random import choice, randint
from collections import namedtuple

# these are the datatype labels for fasttext.
TYPES = ["image", "summarize"]

# create a data type
Data = namedtuple("Data", "type content")

#############
# FUNCTIONS #
#############


def gather_image_subjects():
    """ Returns a random noun from Google Open Images"""
    response = requests.get(
        "https://storage.googleapis.com/openimages/v5/class-descriptions.csv"
    )
    raw_labels = [x.split(",")[1] for x in response.text.splitlines() if "," in x]
    return [x for x in raw_labels if all(d.isalpha() or d.isspace() for d in x)]


# ['', 'id', 'title', 'publication', 'author', 'date', 'year', 'month', 'url', 'content']
nlp = spacy.load("en")


def predict_images(num_examples):
    sentences = [
        "here we have a picture of {}",
        "as you can see it is a picture of {}",
        "one example is the {}, which you can see here",
        "you can see that {} looks like this.",
        "as you can see there is {}",
        "next we'll look at {}",
        "we will look at {}",
        "here we can see that {} looks like this.",
        "this is a picture of {}",
        "this is an image of {}",
        "here are some examples of {}",
    ]

    p = inflect.engine()
    subjects = gather_image_subjects()

    for _ in range(num_examples):
        subject = choice(subjects)
        possibles = [
            "a {}".format(subject),
            "the {}".format(subject),
            "several {}".format(p.plural(subject)),
            "some {}".format(p.plural(subject)),
        ]

        yield choice(sentences).format(choice(possibles))


def predict_summarize(num_examples):
    """ Generates predictions for the summarize function. """

    # start by gathering a large number of sentences:
    count = 0
    with open("articles1.csv", "r") as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader)  # header
        for article in (a[9] for a in datareader):
            doc = nlp(article)
            valid_sentences = [s.text for s in doc.sents if len(s.text) > 100]

            # get 10 random ranges in valid_sentences:
            for _ in range(int(len(valid_sentences) / 2)):
                bottom_bound = randint(0, len(valid_sentences) - 5)
                yield " ".join(
                    valid_sentences[bottom_bound : bottom_bound + randint(1, 4)]
                )
                count += 1
                if count > num_examples:
                    return


VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789.?! ")


def preprocess_text(text):
    """ simplify the text before fasttext processing. """
    return "".join(c for c in text.lower() if c in VALID_CHARS)


def main():
    print("GANERATING TRAINING DATA.")
    num_samples = int(100000)

    # generate the fasttext data:
    with open("data.train.txt", "w") as f:
        for line in tqdm(predict_images(num_samples), total=num_samples):
            f.write("__label__image {}\n".format(line))
        for line in tqdm(predict_summarize(num_samples), total=num_samples):
            f.write("__label__summarize {}\n".format(line))

    print("TRAINING MODEL.")
    model = fasttext.train_supervised("data.train.txt")

    print("QUANTIZING MODEL.")
    model.quantize(input="data.train.txt", retrain=True)

    print("SAVING MODEL.")
    model.save_model("model_{}.ftz".format(num_samples))


if __name__ == "__main__":
    main()
