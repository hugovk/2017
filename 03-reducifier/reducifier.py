#!/usr/bin/env python
# encoding: utf-8
"""
TODO

An entry for NaNoGemMo ("write code that writes a novel") 2017.

https://github.com/hugovk/NaNogenMo/2017
https://github.com/NaNoGenMo/2017/issues/79

Notes:
https://aparrish.neocities.org/textblob.html
"""
from __future__ import print_function

import argparse
import math
import random
import re
# import sys
import textwrap

from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
# from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words
from textblob import TextBlob

# https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
CONTRACTIONS = [
    ["'d've", " would have"],
    ["'d've", " would've"],
    ["'d've", " woulda"],

    ["ain't", "am not"],
    ["aren't", "are not"],
    # ["can't", "cannot"],
    ["could've", "could have"],
    ["couldn't", "could not"],
    ["didn't", "did not"],
    ["doesn't", "does not"],
    ["don't", "do not"],
    ["gonna", "going to"],
    ["gotta", "got to"],
    ["hadn't", "had not"],
    ["hasn't", "has not"],
    ["haven't", "have not"],
    ["he'd", "he had"],
    ["he'd", "he would"],
    ["he'll", "he will"],
    ["he'll", "he shall"],
    ["he's", "he is"],
    ["he's", "he has"],
    ["how'd", "how would"],
    ["how'd", "how did"],
    ["how'll", "how will"],
    ["how's", "how does"],
    ["how's", "how has"],
    ["how's", "how is"],
    ["I'd", "I would"],
    ["I'd", "I would"],
    ["I'll", "I will"],
    ["I'll", "I shall"],
    # ["I'm", "I am"],
    ["I've", "I have"],
    ["isn't", "is not"],
    ["it'd", "it would"],
    ["it'll", "it will"],
    ["it'll", "it shall"],
    # ["it's", "it is"],
    ["it's", "it has"],
    ["mayn't", "may not"],
    ["may've", "may have"],
    ["mightn't", "might not"],
    ["might've", "might have"],
    ["mustn't", "must not"],
    ["must've", "must have"],
    ["needn't", "need not"],
    ["o'clock", "of the clock"],
    # ["ol'", "old"],
    ["oughtn't", "ought not"],
    ["shan't", "shall not"],
    ["she'd", "she would"],
    ["she'd", "she had"],
    ["she'll", "she will"],
    ["she'll", "she shall"],
    ["she's", "she is"],
    ["she's", "she has"],
    ["should've", "should have"],
    ["shouldn't", "should not"],
    ["somebody's", "somebody is"],
    ["somebody's", "somebody has"],
    ["someone's", "someone is"],
    ["someone's", "someone has"],
    ["something's", "something is"],
    ["something's", "something has"],
    ["that'll", "that will"],
    ["that'll", "that shall"],
    ["that're", "that are"],
    ["that's", "that is"],
    ["that's", "that has"],
    ["that'd", "that had"],
    ["that'd", "that would"],
    ["there'd", "there would"],
    ["there'd", "there had"],
    ["there're", "there are"],
    ["there's", "there is"],
    ["there's", "there has"],
    ["these're", "these are"],
    ["they'd", "they would"],
    ["they'd", "they had"],
    ["they'll", "they will"],
    ["they'll", "they shall"],
    ["they're", "they are"],
    ["they've", "they have"],
    ["this's", "this is"],
    ["this's", "this has"],
    ["those're", "those are"],
    ["'tis", "it is"],
    ["'twas", "it was"],
    ["'twasn't", "it was not"],
    ["wasn't", "was not"],
    ["we'd", "we would"],
    ["we'd", "we had"],
    ["we'd've", "we would have"],
    ["we'll", "we will"],
    ["we're", "we are"],
    ["we've", "we have"],
    ["weren't", "were not"],
    ["what'd", "what did"],
    ["what'll", "what will"],
    ["what'll", "what shall"],
    ["what're", "what are"],
    ["what's", "what does"],
    ["what's", "what has"],
    ["what's", "what is"],
    ["what've", "what have"],
    ["when's", "when is"],
    ["when's", "when has"],
    ["where'd", "where did"],
    ["where're", "where are"],
    ["where's", "where does"],
    ["where's", "where has"],
    ["where's", "where is"],
    ["where've", "where have"],
    ["which's", "which is"],
    ["which's", "which has"],
    ["who'd", "who did"],
    ["who'd", "who would"],
    ["who'd", "who had"],
    ["who'd've", "who would have"],
    ["who'll", "who will"],
    ["who'll", "who shall"],
    ["who're", "who are"],
    ["who's", "who does"],
    ["who's", "who has"],
    ["who's", "who is"],
    ["who've", "who have"],
    ["why'd", "why did"],
    ["why're", "why are"],
    ["why's", "why does"],
    ["why's", "why has"],
    ["why's", "why is"],
    ["won't", "will not"],
    ["would've", "would have"],
    ["wouldn't", "would not"],
    ["y'all", "you all"],
    ["you'd", "you would"],
    ["you'd", "you had"],
    ["you'll", "you will"],
    ["you'll", "you shall"],
    ["you're", "you are"],
    ["you've", "you have"],

    ["doesn't she", "does she not"],
    ["doesn't he", "does he not"],
    ["don't I", "do I not"],
    ["don't you", "do you not"],
    ["don't we", "do we not"],

    ["'d ", " had "],
]


def word_count(blob, orig_count=None, summary=None):
    count = len(blob.words)

    if orig_count:
        out = "word count: {:,}\tdiff: {:.3%}".format(count, count/orig_count)
    else:
        out = "word count: {:,}".format(count)

    if summary:
        out = "{}\t{}".format(out, summary)

    print(out)
    return count


def all_case_replace(blob, old, new):
    blob = blob.replace(old, new)
    blob = blob.replace(old.upper(), new.upper())
    blob = blob.replace(old.capitalize(), new.capitalize())
    return blob


def deveryify(blob):
    # Substitute ‘damn’ every time you’re inclined to write ‘very’;
    # your editor will delete it and the writing will be just as it should be.
    # William Allen White
    blob = all_case_replace(blob, " very ", " ")
    blob = all_case_replace(blob, " damn ", " ")

    # Headlines ditch "and", so do we
    blob = all_case_replace(blob, ", and ", ", ")
    blob = all_case_replace(blob, "; and ", "; ")
    blob = all_case_replace(blob, "! and ", "! ")
    blob = all_case_replace(blob, "? and ", "? ")
    blob = all_case_replace(blob, ": and ", ": ")
    blob = all_case_replace(blob, " and ", ", ")

    # No more "or"
    blob = all_case_replace(blob, " or ", "/")

    # Fillers
    blob = all_case_replace(blob, ", however, ", " ")

    blob = all_case_replace(blob, ", indeed, ", ", ")
    blob = all_case_replace(blob, "indeed", "")

    blob = all_case_replace(blob, "I dare say, ", " ")
    blob = all_case_replace(blob, "I dare say ", " ")

    redundancies = [
        # http://editingandwritingservices.com/redundant-words-phrases/
        ["both of them", "both"],

        # https://www.thoughtco.com/common-redundancies-in-english-1692776
        ["absolutely essential", "essential"],
        ["absolutely necessary", "necessary"],
        ["actual facts", "facts"],
        ["advance forward", "advance"],
        ["advance planning", "planning"],
        ["advance preview", "preview"],
        ["advance reservations", "reservations"],
        ["advance warning", "warning"],
        ["add an additional", "add"],
        ["add up", "add"],
        ["added bonus", "bonus"],
        ["affirmative yes", "yes"],
        ["aid and abet", "abet"],
        ["all-time record", "record"],
        ["alternative choice", "alternative"],
        ["A.M. in the morning", "A.M."],
        ["and etc.", "etc."],
        ["anonymous stranger", "stranger"],
        ["annual anniversary", "anniversary"],
        ["armed gunman", "gunman"],
        ["artificial prosthesis", "prosthesis"],
        ["ascend up", "ascend"],
        ["ask the question", "ask"],
        ["assemble together", "assemble"],
        ["attach together", "attach"],
        ["ATM machine", "ATM"],
        ["autobiography of his or her own life", "autobiography"],
        ["bald-headed", "bald"],
        ["balsa wood", "balsa"],
        ["basic fundamentals", "fundamentals"],
        ["basic necessities", "necessities"],
        ["best ever", "best"],
        ["biography of his--or her--life", "biography"],
        ["blend together", "blend"],
        ["boat marina", "marina"],
        ["bouquet of flowers", "bouquet"],
        ["brief in duration", "brief"],
        ["brief moment", "moment"],
        ["brief summary", "summary"],
        ["burning embers", "embers"],
        ["cacophony of sound", "cacophony"],
        ["cameo appearance", "cameo"],
        ["cancel out", "cancel"],
        ["careful scrutiny", "scrutiny"],
        ["cash money", "cash"],
        ["cease and desist", "cease"],
        ["circle around", "circle"],
        ["circulate around", "circulate"],
        ["classify into groups", "classify"],
        ["close proximity", "proximity"],
        ["closed fist", "fist"],
        ["collaborate together", "collaborate"],
        ["combine together", "combine"],
        ["commute back and forth", "commute"],
        ["compete with each other", "compete"],
        ["completely annihilate", "annihilate"],
        ["completely destroyed", "destroyed"],
        ["completely eliminate", "eliminate"],
        ["completely engulfed", "engulfed"],
        ["completely filled", "filled"],
        ["completely surround", "surround"],
        ["component parts", "parts"],
        ["confer together", "confer"],
        ["connect together", "connect"],
        ["connect up", "connect"],
        ["confused state", "confused"],
        ["consensus of opinion", "consensus"],
        ["constantly maintained", "maintained"],
        ["cooperate together", "cooperate"],
        ["could possibly", "could"],
        ["crisis situation", "crisis"],
        ["curative process", "curative"],
        ["current incumbent", "incumbent"],
        ["current trend", "trend"],
        ["depreciate in value", "depreciate"],
        ["descend down", "descend"],
        ["desirable benefits", "benefits"],
        ["different kinds", "kinds"],
        ["disappear from sight", "disappear"],
        ["drop down", "drop"],
        ["during the course of", "during"],
        ["dwindle down", "dwindle"],
        ["each and every", "each"],
        ["earlier in time", "earlier"],
        ["eliminate altogether", "eliminate"],
        ["emergency situation", "emergency"],
        ["empty hole", "hole"],
        ["empty out", "empty"],
        ["empty space", "space"],
        ["enclosed herein", "enclosed"],
        ["end result", "result"],
        ["enter in", "enter"],
        ["entirely eliminate", "eliminate"],
        ["equal to one another", "equal"],
        ["eradicate completely", "eradicate"],
        ["estimated at about", "estimated at"],
        ["evolve over time", "evolve"],
        ["exact same", "same"],
        ["exposed opening", "opening"],
        ["extradite back ", "extradite "],
        ["face mask", "mask"],
        ["fall down", "fall"],
        ["favorable approval", "approval"],
        ["fellow classmates", "classmates"],
        ["fellow colleague", "colleague"],
        ["few in number", "few"],
        ["filled to capacity", "filled"],
        ["final conclusion", "conclusion"],
        ["final end", "end"],
        ["final outcome", "outcome"],
        ["final ultimatum", "ultimatum"],
        ["first and foremost", "foremost"],
        ["first conceived", "conceived"],
        ["first of all", "first"],
        ["fly through the air", "fly"],
        ["follow after", "follow"],
        ["foreign imports", "imports"],
        ["former graduate", "graduate"],
        ["former veteran", "veteran"],
        ["free gift", "gift"],
        ["from whence", "whence"],
        ["frozen ice", "ice"],
        ["frozen tundra", "tundra"],
        ["full to capacity", "full"],
        ["full satisfaction", "satisfaction"],
        ["fuse together", "fuse"],
        ["future plans", "plans"],
        ["future recurrence", "recurrence"],
        ["gather together", "gather"],
        ["general public", "public"],
        ["GOP party", "GOP"],
        ["GRE exam", "GRE"],
        ["in color", ""],
        ["in colour", ""],
        ["grow in size", "grow"],
        ["had done previously", "had done"],
        ["harmful injuries", "injuries"],
        ["head honcho", "honcho"],
        ["heat up", "heat"],
        ["HIV virus", "HIV"],
        ["hoist up", "hoist"],
        ["hollow tube", "tube"],
        ["hurry up", "hurry"],
        ["illustrated drawing", "drawing"],
        ["incredible to believe", "incredible"],
        ["indicted on a charge", "indicted"],
        ["input into", "input"],
        ["integrate together", "integrate"],
        ["integrate with each other", "integrate"],
        ["interdependent on each other", "interdependent"],
        ["introduced a new", "introduced"],
        ["introduced for the first time", "introduced"],
        ["ISBN number", "ISBN"],
        ["join together", "join"],
        ["joint collaboration", "collaboration"],
        ["kneel down", "kneel"],
        ["knowledgeable experts", "experts"],
        ["lag behind", "lag"],
        ["later time", "later"],
        ["LCD display", "LCD"],
        ["lift up", "lift"],
        ["little baby", "baby"],
        ["live studio audience", "studio audience"],
        ["live witness", "witness"],
        ["local residents", "residents"],
        ["look ahead to the future", "look to the future"],
        ["look back in retrospect", "look back"],
        ["made out of", "made of"],
        ["major breakthrough", "breakthrough"],
        ["major feat", "feat"],
        ["manually by hand", "manually"],
        ["may possibly", "may"],
        ["meet together", "meet"],
        ["meet with each other", "meet"],
        ["mental telepathy", "telepathy"],
        ["merge together", "merge"],
        ["might possibly", "might"],
        ["minestrone soup", "minestrone"],
        ["mix together", "mix"],
        ["mutual cooperation", "cooperation"],
        ["mutually interdependent", "interdependent"],
        ["mutual respect for each other", "mutual respect"],
        ["number-one leader in", "leader in"],
        ["nape of her neck", "nape"],
        ["native habitat", "habitat"],
        ["natural instinct", "instinct"],
        ["never before", "never"],
        ["new beginning", "beginning"],
        ["new construction", "construction"],
        ["new innovation", "innovation"],
        ["new invention", "invention"],
        ["new recruit", "recruit"],
        ["none at all", "none"],
        ["nostalgia for the past", "nostalgia"],
        ["now pending", "pending"],
        ["off of", "off"],
        ["old adage", "adage"],
        ["old cliche", "cliche"],
        ["old custom", "custom"],
        ["old proverb", "proverb"],
        ["open trench", "trench"],
        ["open up", "open"],
        ["oral conversation", "conversation"],
        ["originally created", "created"],
        ["output out of", "output"],
        ["outside in the yard", "in the yard"],
        ["outside of", "outside"],
        ["over exaggerate", "exaggerate"],
        ["over with", "over"],
        ["overused cliche", "cliche"],
        ["pair of twins", "twins"],
        ["palm of the hand", "palm"],
        ["passing fad", "fad"],
        ["past experience", "experience"],
        ["past history", "history"],
        ["past memories", "memories"],
        ["past records", "records"],
        ["penetrate into", "penetrate"],
        ["period of time", "period"],
        ["personal friend", "friend"],
        ["personal opinion", "opinion"],
        ["pick and choose", "pick"],
        ["PIN number", "PIN"],
        ["pizza pie", "pizza"],
        ["plan ahead", "plan"],
        ["plan in advance", "plan"],
        ["Please RSVP", "RSVP"],
        ["plunge down", "plunge"],
        ["polar opposites", "opposites"],
        ["positive identification", "identification"],
        ["postpone until later", "postpone"],
        ["pouring down rain", "pouring rain"],
        ["private industry", "industry"],
        ["present incumbent", "incumbent"],
        ["present time", "present"],
        ["previously listed above", "previously listed"],
        ["proceed ahead", "proceed"],
        ["proposed plan", "plan"],
        ["protest against", "protest"],
        ["pursue after", "pursue"],
        ["raise up", "raise"],
        ["RAM memory", "RAM"],
        ["reason is because", "reason is"],
        ["reason why", "reason"],
        ["recur again", "recur"],
        ["re-elect for another term", "re-elect"],
        ["refer back", "refer"],
        ["reflect back", "reflect"],
        ["regular routine", "routine"],
        ["repeat again", "repeat"],
        ["reply back", "reply"],
        ["retreat back", "retreat"],
        ["revert back", "revert"],
        ["rise up", "rise"],
        ["round in shape", "round"],
        ["safe haven", "haven"],
        ["safe sanctuary", "sanctuary"],
        ["same exact", "same"],
        ["sand dune", "dune"],
        ["scrutinize in detail", "scrutinize"],
        ["separated apart from each other", "separated"],
        ["serious danger", "danger"],
        ["share together", "share"],
        ["sharp point", "point"],
        ["shiny in appearance", "shiny"],
        ["shut down", "shut"],
        ["single unit", "unit"],
        ["skipped over", "skipped"],
        ["slow speed", "slow"],
        ["small size", "small"],
        ["small speck", "speck"],
        ["soft in texture", "soft"],
        ["soft to the touch", "soft"],
        ["sole of the foot", "sole"],
        ["spell out in detail", "spell out"],
        ["spliced together", "spliced"],
        ["start off", "start"],
        ["start out", "start"],
        ["still persists", "persists"],
        ["still remains", "remains"],
        ["sudden impulse", "impulse"],
        ["sum total", "total"],
        ["surrounded on all sides", "surrounded"],
        ["tall in height", "tall"],
        ["tall in stature", "tall"],
        ["temper tantrum", "tantrum"],
        ["ten in number", "ten"],
        ["a.m. in the morning", "a.m."],
        ["three-way love triangle", "love triangle"],
        ["time period", "time"],
        ["tiny bit", "bit"],
        ["total destruction", "destruction"],
        ["true facts", "facts"],
        ["truly sincere", "sincere"],
        ["tuna fish", "tuna"],
        ["twelve noon or midnight", "noon or midnight"],
        ["two equal halves", "halves"],
        ["ultimate goal", "goal"],
        ["undergraduate student", "undergraduate"],
        ["underground subway", "subway"],
        ["unexpected emergency", "emergency"],
        ["unexpected surprise", "surprise"],
        ["unintentional mistake", "mistake"],
        ["universal panacea", "panacea"],
        ["unnamed anonymous", "anonymous"],
        ["UPC code", "UPC"],
        ["usual custom", "custom"],
        ["vacillate back and forth", "vacillate"],
        ["veiled ambush", "ambush"],
        ["very pregnant", "pregnant"],
        ["very unique", "unique"],
        ["visible to the eye", "visible"],
        ["wall mural", "mural"],
        ["warn in advance", "warn"],
        ["weather conditions", "weather"],
        ["weather situation", "weather"],
        ["whether or not", "whether"],
        ["white snow", "snow"],
        ["write down", "write"],
    ]
    for r in redundancies:
        blob = all_case_replace(blob, r[0], r[1])

    return blob


def deboilerplatify(blob):
    """PG boilerplates off"""
    end_of_top_boilerplate = "Produced by Anonymous Volunteers"
    pos = blob.find(end_of_top_boilerplate)
    if pos:
        blob = blob[pos+len(end_of_top_boilerplate):].strip()

    start_of_end_boilerplate = "End of the Project Gutenberg EBook"
    pos = blob.rfind(start_of_end_boilerplate)
    if pos:
        blob = blob[:pos].strip()

    return blob


def contractify(blob):

    # Those underscores get in the way
    blob = blob.replace("_", "")

    for c in CONTRACTIONS:
        blob = all_case_replace(blob, c[1], c[0])

    return blob


def dehonorify(blob):

    # https://github.com/dariusk/corpora/blob/master/data/humans/prefixes.json
    honorifics = [
        "Mr.",
        "Mrs.",
        "Ms.",
        "Miss",
        "Dr.",
        "A.V.M",
        "AB",
        "Adm.",
        "Amb",
        "AMN",
        "Archbishop",
        "Baron",
        "Baroness",
        "Bishop",
        "Brig. Gen.",
        "Bigadier",
        "Bro.",
        "Cantor",
        "Capt.",
        "Cardinal",
        "Chaplain",
        "Cmdr.",
        "CMSGT",
        "Col.",
        "Consul",
        "Count",
        "Countess",
        "Cpl.",
        "CPO",
        "CWO",
        "Dean",
        "Duchess",
        "Duke",
        "Earl",
        "Ens.",
        "Eur Eng",
        "Father",
        "Fr.",
        "Gen.",
        "Gov.",
        "H. E.",
        "Herr",
        "Hon",
        "HRH",
        "Lady",
        "Lord",
        "Lt.",
        "Lt. Cmdr.",
        "Lt. Col.",
        "Lt. Gen.",
        "M.",
        "Maj.",
        "Maj. Gen",
        "Master",
        "Mile.",
        "Mme.",
        "Mother",
        "MSGT",
        "Pastor",
        "PFC",
        "Pres.",
        "Prince",
        "Princess",
        "Prof.",
        "Rabbi",
        "Radm",
        "Rev.",
        "Rt. Hon.",
        "Senator",
        "Sgt.",
        "Sgt. Maj.",
        "Sir",
        "Sister",
        "SMSGT",
        "Speaker",
        "Squad. Ldr.",
        "Sr.",
        "SrA",
        "Sra",
        "Srta",
        "SSGT",
        "Swami",
        "STSGT"
    ]
    for h in honorifics:
        blob = blob.replace("{} ".format(h), "")
        blob = blob.replace("{}".format(h), "")

    blob = all_case_replace(blob, "the ", "t'")
    blob = all_case_replace(blob, "to ", "t'")

    return blob


def remove_quote_things(blob):
    """
    “She had better have stayed at home,” cried Elizabeth; “perhaps she
    ->
    “She had better have stayed at home, perhaps she

    “I am exceedingly gratified,” said Bingley, “by your converting what my
    ->
    “I am exceedingly gratified, by your converting what my

    “Oh!” said she, “I heard you before, but I could not immediately
    ->
    “Oh! I heard you before, but I could not immediately
    """
    text = str(blob)
    text = re.sub(r",” .+ “", " ", text)
    text = re.sub(r"!” .+ “", "!", text)
    return TextBlob(text)


def summarise(blob):

    ratio = math.ceil(len(blob.words)/50000)  # round up
    print("Ratio (words/50k):\t", ratio)

    LANGUAGE = "english"
    SENTENCES_COUNT = int(len(blob.sentences)/ratio)
    print("Number of sentences:\t", len(blob.sentences))
    print("Number to keep:\t\t", SENTENCES_COUNT)

    parser = PlaintextParser.from_string(str(blob), Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    new_sentences = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        new_sentences.append(str(sentence))
        # We've lost paragraph breaks, throw some back in
        if random.random() < 0.5:
            new_sentences.append("\n\n")

    return TextBlob(" ".join(new_sentences))


def do_stuff(blob, original_count):

    blob = deboilerplatify(blob)
    word_count(blob, original_count, "deboilerplatify")

    blob = remove_quote_things(blob)
    word_count(blob, original_count, "remove_quote_things")

    blob = deveryify(blob)
    word_count(blob, original_count, "deveryify")

    blob = contractify(blob)
    word_count(blob, original_count, "contractify")

    blob = dehonorify(blob)
    word_count(blob, original_count, "dehonorify")

    return blob


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--infile', default="1342-0.txt",
        help="Input filename")
    args = parser.parse_args()

    print("open")
    with open(args.infile) as f:
        blob = TextBlob(f.read())

    original_count = word_count(blob)
    blob = do_stuff(blob, original_count)

    with open("output.txt", "w") as f:
        f.write(str(blob))

    blob = summarise(blob)
    word_count(blob, original_count, "summarise")

    # Split by paragraphs
    # paragraphs = str(blob).split("\n\n")

    with open("output2.txt", "w") as f:
        # for paragraph in paragraphs:
            # f.write(str(blob))
        f.write("\n".join(textwrap.wrap(str(blob), width=74,
                                        replace_whitespace=False)))


# End of file
