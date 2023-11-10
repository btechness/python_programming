# a program to create a low level conlang by jumbling the latin languages and transliterating that to Russian. English grammar rules as conlangs grammar since it is a tedius task and use translate to get the part of speeches of other languages

import nltk
import traceback
from translate import Translator
from transliterate import translit

# nltk tags and their meanings
pos_tags_nltk = {
  "CC":"conjunction",
  "DT":"determiner",
  "IN":"preposition, conjunction",
  "JJ":"adjective",
  "JJR":"adjective",
  "JJS":"adjective",
  "NN":"noun",
  "PRP":"pronoun",
  "PRP":"pronoun",
  "NNP":"noun",
  "NNS":"noun",
  "RB":"adverb",
  "RBR":"adverb",
  "RBS":"adverb",
  "TO":"preposition",
  "VB":"verb",
  "VBD":"verb",
  "VBG":"verb",
  "VBN":"verb",
  "VBP":"verb",
  "VBZ":"verb",
  "UH": "interjection"
}


sentence = "I can write some code in Python language. I'm considering writing a sentence which can have all the parts of the speech so that I can analyse my colang programme written in python on a windows machine which runs on latest intel processors."
# intermediate output - I can schrijven algumas code en Pythactivar langue. IM cactivarsidereng writeng a phrase which can zijn todos . aux de . discours entactivarces que I can Analyse my colang programmes en en pythactivar activar a wendows machene which Run activar aktuellste, entel procesentactivarcesrs.
# output - И цан счрийвен алгумас цоде ен Пытхацтивар лангуе. ИМ цацтиварсидеренг wритенг а пхрасе wхич цан зийн тодос . ауx де . дисцоурс ентацтиварцес qуе И цан Аналысе мы цоланг программес ен ен пытхацтивар ацтивар а wендоwс мачене wхич Рун ацтивар актуеллсте, ентел процесентацтиварцесрс.

# tokenize
words = nltk.word_tokenize(sentence)
# use part of speech tagging to tag the sentence
pos_tags = nltk.pos_tag(words)
# store the sentence in a new variable
original_sentence = sentence

# jumble up the sentence with other latin languages
for pos in pos_tags:
    try:
        partofspeech = pos_tags_nltk[pos[1]]
        if partofspeech == "noun" or partofspeech == "pronoun":
            translator_french = Translator(to_lang="fr")
            translation_french = translator_french.translate(pos[0]).split()[0]
            sentence = sentence.replace(pos[0],translation_french)
        elif partofspeech == "interjection" or partofspeech == "adjective":
            translator_german = Translator(to_lang="de")
            translation_german = translator_german.translate(pos[0]).split()[0]
            sentence = sentence.replace(pos[0],translation_german)
        elif partofspeech == "verb"or partofspeech == "adverb":
            translator_dutch = Translator(to_lang="nl")
            translation_dutch = translator_dutch.translate(pos[0]).split()[0]
            sentence = sentence.replace(pos[0],translation_dutch)    
        elif "preposition" in partofspeech or "conjunction" in partofspeech:
            translator_spanish = Translator(to_lang="es")
            translation_spanish = translator_spanish.translate(pos[0]).split()[0]
            sentence = sentence.replace(pos[0],translation_spanish)          
        elif "determiner" in partofspeech:
            translator_portuguese = Translator(to_lang="pt")
            translation_portuguese = translator_portuguese.translate(pos[0]).split()[0]
            sentence = sentence.replace(pos[0],translation_portuguese)          
    except KeyError:
        pass
    except:
        traceback.print_exc()

# transliterate to Russian
rooski = translit(sentence,'ru')
print(rooski)
