"""

Simply generate the data

TODO: Consider determining title based on whether the slide is blank
      or based on the length of the content itself.

"""
import csv
import inflect
import requests
import fasttext

from tqdm import tqdm
from random import choice
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
        "take a look at these pictures of {} that i took.",
        "check out this image of {}",
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

    # load the sentences into memory:
    count = 0
    all_sentences = []
    with open("sentences.csv", "r") as csvfile:
        datareader = csv.reader(csvfile, delimiter="\t")
        for num, lang, sent in datareader:
            if lang == "eng":
                all_sentences.append(sent)

    for _ in range(num_examples):
        yield choice(all_sentences)


VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789.?! ")


def preprocess_text(text):
    """ simplify the text before fasttext processing. """
    return "".join(c for c in text.lower() if c in VALID_CHARS)


def main():
    print("GANERATING TRAINING DATA.")
    num_samples = int(1000000)

    # generate the fasttext data:
    with open("data.train.txt", "w") as f:
        for line in tqdm(predict_images(num_samples), total=num_samples):
            f.write("__label__image {}\n".format(preprocess_text(line)))
        for line in tqdm(predict_summarize(num_samples), total=num_samples):
            f.write("__label__summarize {}\n".format(preprocess_text(line)))

    print("TRAINING MODEL.")
    model = fasttext.train_supervised("data.train.txt")

    print("QUANTIZING MODEL.")
    model.quantize(input="data.train.txt", retrain=True)

    print("SAVING MODEL.")
    model.save_model("model_{}.ftz".format(num_samples))


if __name__ == "__main__":
    main()
