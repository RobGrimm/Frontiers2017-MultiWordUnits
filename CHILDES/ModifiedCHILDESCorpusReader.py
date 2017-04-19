from nltk.corpus.reader import CHILDESCorpusReader, NS, string_types
from nltk.corpus.reader.xmldocs import ElementTree


sent_node = './/{%s}u' % NS
word_node = './/{%s}w' % NS
word_pos_tag_node = './/{%s}c' % NS
replacement_node = './/{%s}w/{%s}replacement' % (NS, NS)
replaced_word_node = './/{%s}w/{%s}replacement/{%s}w' % (NS, NS, NS)
replaced_word_node2 = './/{%s}w/{%s}wk' % (NS, NS)
stem_node = './/{%s}stem' % NS
relation_node = './/{%s}s' % NS
inflection_node = './/{%s}mor/{%s}mw/{%s}mk' % (NS, NS, NS)
clitic_node = './/{%s}mor/{%s}mor-post/{%s}mw/{%s}stem' % (NS, NS, NS, NS)
clitic_pos_tag_node = './/{%s}mor/{%s}mor-post/{%s}gra' % (NS, NS, NS)



def add_inflection(xmlword, word):
    xmlinfl = xmlword.find(inflection_node)
    if xmlinfl.get('type') == 'sfx':    # regular inflection
        word += '-' + xmlinfl.text
    elif xmlinfl.get('type') == 'sfxf': # irregular inflection
        word += '&' + xmlinfl.text
    return word


def get_pos_tag(xmlword):
    xmlpos = xmlword.findall(word_pos_tag_node) # word's POS tag
    xmlpos2 = xmlword.findall(relation_node)    # relational information (e.g. "SUB" for subject)
    if xmlpos2:
        tag = xmlpos[0].text + ":" + xmlpos2[0].text
    else:
        tag = xmlpos[0].text
    return tag


def get_replaced_word(xmlsent, xmlword):
    if xmlsent.find(replacement_node):
        xmlword = xmlsent.find(replaced_word_node)
    elif xmlsent.find(replaced_word_node2):
        xmlword = xmlsent.find(replaced_word_node2)
    return xmlword


class ModifiedCHILDESCorpusReader(CHILDESCorpusReader):
    """
    Modified (and somewhat cleaner than the NLTK version) '_get_words' method of the CHILDES corpus reader from the NLTK.
    Modified to fetch clitics as separate lexical entries if you retrieve stemmed sentences,
    e.g. by calling 'corpus_reader.tagged_sents(stem=True)'.
    """
    def _get_words(self, fileid, speaker, sent, stem, relation, pos, strip_space, replace):

        # ensure we have a list of speakers
        if isinstance(speaker, string_types) and speaker != 'ALL':
            speaker = [speaker]

        xmldoc = ElementTree.parse(fileid).getroot()

        # processing each sentence in xml doc
        results = []
        for xmlsent in xmldoc.findall(sent_node):
            sents = []

            # select speakers
            if speaker == 'ALL' or xmlsent.get('who') in speaker:

                # process each word
                for xml_word in xmlsent.findall(word_node):
                    clitic_stem = None

                    # get replaced words
                    if replace:
                        xml_word = get_replaced_word(xmlsent, xml_word)

                    # get text
                    if xml_word.text:
                        word = xml_word.text
                    else:
                        word = ''

                    # strip tailing space
                    if strip_space:
                        word = word.strip()

                    # get stemmed words
                    if stem:
                        try:
                            xmlstem = xml_word.find(stem_node)
                            word = xmlstem.text
                        except AttributeError:
                            pass

                        # if there is an inflection
                        try:
                            word = add_inflection(xml_word, word)
                        except:
                            pass

                        # if there is a clitic
                        try:
                            xmlclitic = xml_word.find(clitic_node)
                            clitic_stem = xmlclitic.text
                        except AttributeError:
                            clitic_stem = ''

                    # get pos
                    if pos:
                        try:
                            tag = get_pos_tag(xml_word)
                            word = (word, tag)
                        except (AttributeError, IndexError):
                            word = (word, None)

                        if clitic_stem:
                            # add clitic's pos tag if there is one
                            # in the parent class method, this branch does not fetch the clitic -- this is changed here
                            clitic_pos = xml_word.find(clitic_pos_tag_node)
                            if clitic_pos is not None:
                                clitic_stem = (clitic_stem, clitic_pos.get('relation'))
                            else:
                                clitic_stem = (clitic_stem, None)

                    sents.append(word)
                    if clitic_stem:
                        sents.append(clitic_stem)
                if sent:
                    results.append(sents)
                else:
                    results.extend(sents)

        return results