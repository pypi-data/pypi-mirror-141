from .stats import calculate_keywords
import pandas

class NGrams:
    def __init__(self, filename, size, **kwargs):
        # Parse args and kwargs
        self.filename = filename
        self.size = size
        self.group_by = kwargs['group_by']
        self.sep = kwargs['sep']
        self.text_filter = kwargs['text_filter']
        self.cross_sentence_boundary = kwargs['cross_sentence_boundary']
        self.punct_pos = kwargs['punct_pos']
        self.chunk_num = kwargs['chunk_num']
        self.chunk_size = kwargs['chunk_size']
        self.ngram_references = {}
        self.ngrams = self.calculate_ngrams()
        
    # This is the cool method for getting keywords
    def __truediv__(self, other):
        return calculate_keywords(self.ngrams, other.ngrams)

    def calculate_ngrams(self):
        ngram_dict = {}
        self.elixir = pandas.read_csv(self.filename, sep='\t', escapechar='\\', index_col=None, header=0, chunksize=self.chunk_size, keep_default_na=False)
        # word_tracking will contain each words. Once it hits correct size or end of sentence, then reset the words.
        word_tracking = []
        current_citation = ''
        # Iterate through each chunk of the elix file.
        for block_num, chunk in enumerate(self.elixir):
            chunk = self.filter_chunk(chunk)
            print(f'\rN-Gram Progress: {round((block_num+1)/self.chunk_num*100, 2)}%', end='')
            # Iterate through each word in the chunk.
            for w in chunk.to_dict('records'):
                # Check to see if the word is punctuation.
                if w['pos'] in self.punct_pos:
                    continue
                # Get the citation (location) of the word.
                citation = self.get_citation(chunk, w)
                # If the citation is not the same as the current_citation, then we've hit a new sentence.
                # Words should not be in an ngram from different sentences.
                
                if citation != current_citation:
                    # Reset word_tracking if cross_sentence_boundary is set to False.
                    if not self.cross_sentence_boundary:
                        word_tracking = []
                    current_citation = citation

                    
                # Append the next word to word_tracking
                word_tracking.append(w[self.group_by])
                
                if len(word_tracking) == self.size:
                    full_ngram = self.sep.join(word_tracking)
                    if full_ngram not in ngram_dict:
                        ngram_dict[full_ngram] = 0
                    ngram_dict[full_ngram] += 1
                    # Pop the first word in word_tracking in preparation for the next word.
                    word_tracking.pop(0)
        
        print(f'\rSorting N-Grams by Frequency...          ', end='')
        sorted_ngram_dict = sorted(ngram_dict.items(), key=lambda t: (-t[1], t[0]))
        print('\n')
        return sorted_ngram_dict

    def get_citation(self, chunk, word):
        headers = list(chunk.columns.values)
        index_of_word_index = headers.index('word_index')
        citation_headers = headers[0:index_of_word_index]
        citation = '/'.join([str(word[i])for i in citation_headers])
        return citation

    # Filters the chunk based on optional filters.
    def filter_chunk(self, chunk):
        if self.text_filter == None:
            return chunk
        elif isinstance(self.text_filter, dict):
            filter_index = 0
            for key, value in self.text_filter.items():
                if filter_index == 0:
                    if value.startswith('!'):
                        new_chunk = chunk[chunk[key] != value[1:]]
                    else:
                        new_chunk = chunk[chunk[key] == value]
                else:
                    if value.startswith('!'):
                        new_chunk = new_chunk[new_chunk[key] != value[1:]]
                    else:
                        new_chunk = new_chunk[new_chunk[key] == value]
                filter_index += 1
            return new_chunk
        elif isinstance(self.text_filter, list):
            pass
            # TODO: This is where a user could input ['Book of Mormon/1 Nephi/1/1'] to specify exact citation filtering.

    def export_as_txt(self, filename):
        with open(filename, 'w', encoding='utf-8') as file_out:
            print(f'ngram\tfrequency', file=file_out)
            for ngram in self.ngrams:
                print(ngram[0], ngram[1], sep='\t', file=file_out)