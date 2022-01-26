import threading

lock = threading.Lock()


from wn import Wordnet
from wn.morphy import Morphy
import json

from collections import defaultdict


class SingletonOptmizedOptmized(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(SingletonOptmizedOptmized, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



spacy_to_wn = {
    'NOUN': 'n',
    'VERB': 'v',
    'ADJ': 'a',
    'ADV': 'r',
    'CONJ': 'c',
    'CCONJ': 'c',
    'SCONJ': 'c',
    'ADP': 'p'
}

wn_to_spacy = {
    'n': 'NOUN',
    'v': 'VERB',
    'a': 'ADJ',
    'r': 'ADV',
    'c': 'CONJ',
    'p': 'ADP'
}

"""

printable_part_of_speech = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adjective',
        'r': 'Adverb',
        's': 'Adjective Satellite',
        't': 'Phrase',
        'c': 'Conjunction',
        'p': 'Adposition',
        'x': 'Other',
        'u': 'Unknown'
    }
"""



class WordnetApi(metaclass=SingletonOptmizedOptmized):

    def __init__(self, lang = "en"):
        self.__wn = Wordnet('oewn:2021')
        self.__morphy = Morphy(self.__wn)
        self.__wn.lemmatizer = self.__morphy
        # self.__ic = wn.ic.load('~/nltk_data/corpora/wordnet_ic/ic-brown-add1.dat', self.__wn)

    def get_synsets_or_none(self, text):
        output = None
        if text.isalpha():

            synsets = self.__wn.synsets(text)
            output = set()# defaultdict(set)
            for synset in synsets:
                try:
                    lemma = synset.lemmas()[0]
                    # output[synset.pos].add(lemma)
                    output.add(lemma)
                except Exception as ee:
                    print('THREW EXCEPTION LINE 82 WORDNET_API')
                    print(ee)
                try:
                    for word in synset.words():
                        # output[synset.pos].add(word.lemma())
                        output.add(word.lemma())
                except Exception as e:
                    print('THREW EXCEPTION LINE 89 WORDNET_API')

                    print(e)

        return output

    def _get_sense_str(self, sense):
        return sense.word().lemma() # + ' - ' + sense.word().pos

    def get_senses(self, text):
        output = {}
        senses = self.__wn.senses(text)
        sense_str = ''
        sense_rels = defaultdict(list)
        for sense in senses:
            sense_str = self._get_sense_str(sense)  # This will always be the same...

            for rel_type, rel_senses in sense.relations().items():
                for rel_sense in rel_senses:
                    rel_sense_lemma = rel_sense.word().lemma()
                    if rel_sense_lemma not in sense_rels[rel_type]:
                        sense_rels[rel_type].append(rel_sense_lemma)

        output[sense_str] = {
            'relations': sense_rels
        }

        return output

    def _get_synset_str(self, synset):
        return synset.word().lemma() + ' - ' + synset.word().pos

    #@lru_cache(maxsize=4000)

    """def _add_to_cache(self, _cache, key, value):
        pass"""

    #_guw_cache = {}

    def _get_unique_words(self, synset):
        _unique_words = set()
        #for word in synset.words():
        #    _unique_words.add(word.lemma())
        for lemma in synset.lemmas():
            _unique_words.add(lemma)
        return _unique_words

    def get_related_synsets(self, synset):
        output = set()
        for similar_synset in synset.get_related('similar'):
            output.update(self._get_unique_words(similar_synset))
        return output

    printable_part_of_speech = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adj',
        'r': 'Adverb',
        's': 'Adj Sat',
        't': 'Phrase',
        'c': 'Conjunct',
        'p': 'Adpos',
        'x': 'Other',
        'u': 'Unknown'
    }

    def get_definitions(self, synsets):
        output = set()

        for synset in synsets:
            #outstring = f'({synset.pos} - {self.printable_part_of_speech[synset.pos]}): {synset.definition()}'
            output.add((synset.definition(), self.printable_part_of_speech[synset.pos]))

        return list(output)

    def get_synsets(self, text):
        output = []
        synsets = self.__wn.synsets(text)
        definitions = self.get_definitions(synsets)

        synset_words = set()
        synset_relations = defaultdict(set)
        for synset in synsets:
            synset_words.update(self._get_unique_words(synset))
            synset_rels = defaultdict(set)
            for rel_type, rel_synsets in synset.relations().items():
                for rel_synset in rel_synsets:
                    rel_synset_words = self._get_unique_words(rel_synset)
                    synset_rels[rel_type].update(rel_synset_words)

            synset_relations.update(synset_rels)
        serializable_synset_relations = defaultdict(list)
        for rel_type, words_list in synset_relations.items():
            serializable_synset_relations[rel_type] = list(words_list)

        return {
            'definitions': definitions if len(definitions) > 0 else None,
            'words': list(synset_words),
            'relations': serializable_synset_relations
        }

    def get_data_for_text(self, text):
        data = self.get_synsets(text)
        return data


    def get_lemmas_and_words_synset(self, synset):
        output = set()
        try:
            lemma = synset.lemmas()[0]
            output.add(lemma)
        except Exception as ee:
            print(ee)
        try:
            for word in synset.words():
                output.add(word.lemma())
        except Exception as e:
            print(e)
        return output




    def get_synsets_and_similar_or_none(self, text):
        output = None
        # if text.isalpha():
        synsets = self.__wn.synsets(text)
        if synsets is not None:
            output = set()  # defaultdict(set)
            for synset in synsets:
                first_set = self.get_lemmas_and_words_synset(synset)
                output.update(first_set)
                try:
                    similar_synsets = synset.get_related('similar')
                    for similar_synset in similar_synsets:
                        output.update(self.get_lemmas_and_words_synset(similar_synset))
                except Exception as ee:
                    print(ee)

        return output



    def get_relations_or_none(self, text):
        output = None
        synsets = self.__wn.synsets(text)
        if synsets is not None:
        # if text.isalpha():

            output = defaultdict(set)

            for synset in synsets:
                synset_rels = synset.relations()

                for relname, sslist in synset_rels.items():
                    if str(relname.lower()) != 'similar':
                        rel_specific_words = set()
                        for inner_synset in sslist:
                            l_n_w = self.get_lemmas_and_words_synset(inner_synset)
                            rel_specific_words.update(l_n_w)

                        if len(rel_specific_words) > 0:
                            output[relname].update(rel_specific_words)
        return output


    """def get_rhymes_or_none(self, text: str):
        output = None
        if text.isalpha():
            output = pronouncing.rhymes(text)
            if len(output) == 0:
                output = None
        return output"""



def main():
    wordnet_api = WordnetApi()
    # synsets = wordnet_api.get_synsets_or_none('test')
    text_data = wordnet_api.get_data_for_text('running')
    stop_here = ''
    print(json.dumps(text_data, indent=4, sort_keys=True))

    # rhymes = wordnet_api.get_rhymes_or_none('hjkl')
    #senses = wordnet_api.get_senses('test')
    #senses2 = wordnet_api.get_senses('zzz')


    stop_here = ''



if __name__ == '__main__':
    main()


"""
synset_data = {'lemma': lemma,
                               'forms_senses': []}
                    if sense_lemma not in unique_data:
                        sense_forms = set()
                        for form in sense.word().forms():
                            if form not in unique_data:
                                sense_forms.add(form)
                                unique_data.add(form)


                        synset_data['forms_senses'].append({
                            'sense': sense_lemma,
                            'forms': sense_forms
                        })

"""