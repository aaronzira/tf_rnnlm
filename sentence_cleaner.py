import re
import nltk


def clean(text,word_to_id):

    unknown_token="UNK"
    sentence_start_token="START"
    sentence_end_token="END"

    # metas, punctuation (keeping hyphens), and non-word fillers
    timestamps = "\d+:\d+:\d+(\.\d+)*"
    speakers = "S\d*:"
    metas = "\[.{5,24}\]"
    punctuation = "[\"\.\!\?\:]+"
    new_line = "\n"
    pattern = "|".join([timestamps,speakers,metas,punctuation,new_line])

    # non-lexical utterances
    fillers = "mm-hmm|uh-huh"

    # numbers not part of a word like CO2, mp3, etc.
    numbers = "(?<!\w)\d+"

    # only dealing with one line at a time at this point
    line = text.decode("utf-8")

    # remove timestamps, speakers, metas, and punctuation. then lower and strip, then sub numbers
    cleaned = re.sub(pattern,"",line).lower()
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
    cleaned = re.sub(fillers, "", cleaned)
    sentence = re.sub(numbers,"N",cleaned).strip()

    # was != "", but there were a number of sentences of just "s"
    sentence = "{} {} {}".format(sentence_start_token,sentence,sentence_end_token)

    # word tokenize
    word_tokenized = nltk.word_tokenize(sentence)

    out_sentence = [word_to_id[word] if word in word_to_id else word_to_id[unknown_token] for word in word_tokenized]

    #-#return out_sentence
    return word_tokenized,out_sentence
    #-#


