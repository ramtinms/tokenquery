from conllu.parser import parse, parse_tree
from tokenquery.models.token import Token


class Importer:

    @classmethod
    def load_from_conll_u_file(self, file_path):
        tokens = []
        with open(file_path) as input_file:
            data = input_file.read()
            paresed_data = parse(data)
            total_counter = 0
            total_span_counter = 0
            for sent_counter, sentence in enumerate(paresed_data):
                for token_counter, token in enumerate(sentence):

                    new_token = Token(total_counter,
                                      token['form'],
                                      total_span_counter,
                                      total_span_counter + len(token['form']))

                    total_span_counter += len(token['form']) + 1

                    if token_counter == 0:
                        new_token.add_a_label('B-sent', str(sent_counter))
                    else:
                        new_token.add_a_label('I-sent', str(sent_counter))

                    if token['lemma']:
                        new_token.add_a_label('lemma', token.get('lemma'))

                    if token['upostag']:
                        new_token.add_a_label('upostag', token.get('upostag'))

                    if token['xpostag']:
                        new_token.add_a_label('xpostag', token.get('xpostag'))

                    feats = token['feats']
                    if feats:
                        for feat in feats:
                            new_token.add_a_label('feat-' + feat, feats[feat])

                    if token['head']:
                        new_token.add_a_label('head', str(token.get('head')))

                    if token['deprel']:
                        new_token.add_a_label('deprel', str(token.get('deprel')))

                    if token['deps']:
                        new_token.add_a_label('deps', token.get('deps'))

                    misc = token['misc']
                    if misc:
                        for feat in misc:
                            new_token.add_a_label('misc-' + feat, misc[feat])

                    tokens.append(new_token)
                    total_counter += 1

        return tokens

    @classmethod
    def import_spacy_doc(doc):
        tokens = []
        for word in doc:
            new_token = Token(word.i, word.text, word.idx, word.idx + len(word.text_with_ws))
            if word.lemma:
                new_token.add_a_label('lemma', word.lemma)
            if word.tag:
                new_token.add_a_label('tag', word.tag)
            if word.tag_:
                new_token.add_a_label('tag_', word.tag_)
            if word.pos:
                new_token.add_a_label('pos', word.pos)
            if word.pos_:
                new_token.add_a_label('pos_', word.pos_)
            if word.ent_iob:
                new_token.add_a_label('ent_iob', word.ent_iob)
            if word.ent_type_:
                new_token.add_a_label('ent_type_', word.ent_type_)
            if word.shape:
                new_token.add_a_label('shape', word.shape)
            if word.prefix:
                new_token.add_a_label('prefix', word.prefix)
            if word.suffix:
                new_token.add_a_label('suffix', word.suffix)
            if word.cluster:
                new_token.add_a_label('brown_cluster', '{0:8b}'.format(word.cluster))
            if len(word.vector) > 0:
                new_token.add_a_label('word2vec', '[' + ','.join(['{0:.1f}'.format(item) for item in word.vector]) + ']')

            # TODO add sentences
        return tokens

    @classmethod
    def import_from_g_nlp_api(output_objects):
        # process tokens
        tokens = []
        span_start_to_token_index = {}
        for counter, token in enumerate(output_objects.get('tokens', [])):
            start_offset = token.get('text', {}).get('beginOffset')
            text = token.get('text', {}).get('content', '')
            new_token = Token(counter, text, start_offset, start_offset + len(text))
            if token.get('lemma'):
                new_token.add_a_label('lemma', token.get('lemma'))
            for feature in token.get('partOfSpeech', {}):
                new_token.add_a_label('pos-'+feature, token.get('partOfSpeech').get(feature))

            # process  dependency parsing info
            new_token.add_a_label('dep-head', str(token.get('dependencyEdge').get('headTokenIndex')))
            new_token.add_a_label('dep-label', token.get('dependencyEdge').get('label'))

            span_start_to_token_index[start_offset] = counter
            tokens.append(new_token)

        # process sentences
        prev_offset = 0
        sentences = output_objects.get('sentences', [])
        for counter, sentence in enumerate(sentences):
            start_offset = sentence.get('text', {}).get('beginOffset')
            if start_offset:
                start = span_start_to_token_index[prev_offset]
                end = span_start_to_token_index[start_offset]
                for i, token in enumerate(tokens[start:end]):
                    if i == 0:
                        token.add_a_label('B-Sent', counter)
                    else:
                        token.add_a_label('I-Sent', counter)
            prev_offset = start_offset
        for i, token in enumerate(tokens[prev_offset:]):
            if i == 0:
                token.add_a_label('B-Sent', len(sentences))
            else:
                token.add_a_label('I-Sent', len(sentences))

        # process entities (chunks to tokens)
        entities = output_objects.get('entities', [])
        for entity in entities:
            name = entity.get('name', '')
            salience = entity.get('salience', '')
            entity_type = entity.get('type', 'UNKNOWN')
            metadata = entity.get('metadata', {})
            mentions = entity.get('mentions', [])
            for mention in mentions:
                mention_type = mention.get('type', 'UNKNOWN')
                mention_text_begin_offset = mention.get('text', {}).get('beginOffset')
                mention_text_content = mention.get('text', {}).get('content')
                # Warning - very fragile
                start = span_start_to_token_index[mention_text_begin_offset]
                number_of_tokens = len(mention_text_content.split(r'\s'))
                for i, token in enumerate(tokens[start: start + number_of_tokens + 1]):
                    if i == 0:
                        token.add_a_label('B-' + entity_type, name)
                        token.add_a_label('B-entity', str(salience))
                        for meta in metadata:
                            token.add_a_label('B-entity-meta-' + meta, metadata.get(meta))
                    else:
                        token.add_a_label('I-' + entity_type, name)
                        token.add_a_label('I-entity', str(salience))
                        for meta in metadata:
                            token.add_a_label('I-entity-meta-' + meta, metadata.get(meta))

        return tokens
