import re
import nltk


def clean(text,word_to_id):

    unknown_token = "UNK"
    sentence_start_token = "START"
    sentence_end_token = "END"

    # timestamps, speakers, metas, punctuation, newlines
    timestamps = "\d+:\d+:\d+(\.\d+)*"
    speakers = "[Ss]\d*:"
    metas = "\[.{5,24}\]"
    punctuation = "[\"\.\!\?\:]+"
    new_line = "\n"
    pattern = "|".join([timestamps,speakers,metas,punctuation,new_line])
    # non-lexical utterances
    fillers = "mm-hm+|uh-huh" #uh+|um+|hm+ later
    # numbers not part of a word like CO2, 3D, etc.
    # still possible for things like 3-D to cause issues
    numbers = "(?<!\w)\d+(?!\w)"

    # subs
    # timestamps, speakers, metas, punctuation, newlines
    cleaned = re.sub(pattern,"",text).lower()
    # common Commonwealth spellings
    cleaned = re.sub("\\bbehaviour", "behavior", cleaned)
    cleaned = re.sub("\\btumour\\b","tumor",cleaned)
    cleaned = re.sub("honour", "honor", cleaned)
    cleaned = re.sub("labour", "labor", cleaned)
    cleaned = re.sub("colour", "color", cleaned)
    cleaned = re.sub("flavour", "flavor", cleaned)
    cleaned = re.sub("centre\\b", "center", cleaned)
    cleaned = re.sub("centred\\b", "centered", cleaned)
    cleaned = re.sub("\\bstorey\\b", "story", cleaned)
    cleaned = re.sub("\\bcancell", "cancel", cleaned)
    cleaned = re.sub("\\btravell", "travel", cleaned)
    cleaned = re.sub("labell", "label", cleaned) # names like labelle, but should be unk either way
    cleaned = re.sub("modell", "model", cleaned)
    # fillers
    cleaned = re.sub(fillers, "", cleaned)
    # hyphens
    cleaned = re.sub("-", " ", cleaned)
    # numbers
    sentence = re.sub(numbers,"N",cleaned)

    sentence = "{} {} {}".format(sentence_start_token,sentence,sentence_end_token)

    # word tokenize
    word_tokenized = nltk.word_tokenize(sentence)

    word_indices = [word_to_id[word] if word in word_to_id else word_to_id[unknown_token] for word in word_tokenized]

    return word_tokenized,word_indices


