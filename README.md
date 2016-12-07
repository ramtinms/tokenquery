# Tokenregex (regular expressions over tokens)
**Tokenregex** is a query language over sequence of tokens; very similar to regular expressions but on top of tokens. The orginal idea is not new and is taken from *Angel Chang* and *Christopher Manning* presented in [this paper](http://nlp.stanford.edu/pubs/tokensregex-tr-2014.pdf). They have implemeneted it (TOKENSREGEX) in Java inside *Stanford CoreNLP* software package. Note that the language we use here is a little bit different.

## How to install 
```
pip install tokenregex
```

## Language Definition
**Tokens** are smallest processing units and each token is express inside `[` `]`. If you want to use `]` inside your token matches you can simply use `\` to skip.

### Exact match
Exact string match is possible by having the text you want to match inside `"`s.
For example `["painter"]` will match any token that its text is `painter` but not `Painter`.

### Regex match 
If you want to find tokens that matches a regex you can have your regex inside `/`s . 
For example `[/an?/]` matches tokens having text `a` or `an`. 
`[/Al.*/]` matches any token starting with `Al`.
`[/km|kilometers?/]` matches `km`, `kilometer` and `kilometers`
Note that you can use `/` inside the regex without any modification, we only care extra first `/` and last `/`. 

### Label match
You can define as many labels (key/values pairs) you want for each token and check if each label matches or not. 
To do so, you should mention label name with colons inside each token match.
For example, `[pos:"VBZ"]` matches any token that has a label `pos` and the value for that is `VBZ`.
Furthermore, you can use regex for matching values of lables:
`[pos:/V.*/]` matches any token that has a `pos` label and is a verb (If this sentence does not make any sense to you have to learn more about `part of speech tagging` first).

Note: If you want to check if a lable exists or not and you don't care about the value of the label you can simply use this `[pos:/.*/]`.

### Value match
Currenlty we only support a limited set of value operation over token. Hopefully in the future we have more operations over each token. 

`[word>30]` will check if the token is an int and greater than 30.
These comparisions ( >=, <. <=, ==, !=) are also available.

`[len>20]` will check if the len of a token is more than 20

### Quantifiers
You can use quantifiers to have more compact tokenregexes.

#### `?` once or not at all
e.g. `[pos:/.*/]?`

#### `*` zero or more times
e.g. `[pos:/.*/]*`

#### `+` one or more times
e.g. `[pos:/.*/]+`

#### `{x}` x number of times
e.g. `[pos:/.*/]{3}`

#### `{x,y}` between x and y number of times
(Under Construction)
e.g. `[pos:/.*/]{3,5}`

### Compound Expressions
Currently we don't support Compound Expressions. Soon we support `&` and `|` for compounding.

### Capturing and Groups
Like reguar expressions, you can define capturing groups by parentheses. If you don't provide any, it will capture all as a single group.
for example `([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] ["painter"]` return a group containing sequence of tokens with named-entity tag of `PERSON`; and `[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] ["painter"]` will return the whole matched tokens containing names, verbs, ... .

## Other NLP info
We belive a big portion of NLP information can be expressed in terms of labels on top of tokens. Here is a list of the ones currently we use and how we represent it. Please note that you can define your own lables and there is no limitation in theory for this package.
- Part Of Speech tags (e.g. `[pos:/V.*/]`)

- Named-Entity tags (e.g. `[ner:"PERSON"]`)

- Brown clusters

    | label | We | need | a | lawyer | . |
    |----|----|----|----|----|----|
    | POS | `PRP` | `VBP` | `DT` | `NN` | `.` |
    | bcluster| | | |`1000001101000` | 
    
    And we can query member inside clusters by tokenregexes like this:
  `[bcluster:/100000110[0-1]+/])`
   which will match all of these and more. for more info see Miller et al., NAACL 2004
   
    | word | code |
    |--------|-----|
    | lawyer | 1000001101000 |
    | newspaperman | 100000110100100 |
    | stewardess | 100000110100101 |
    | toxicologist | 10000011010011 |
    | slang | 1000001101010 |
    | babysitter | 100000110101100 |
    | conspirator | 1000001101011010 |
    | womanizer | 1000001101011011 |
    | mailman | 10000011010111 |
    | salesman | 100000110110000 |
    | bookkeeper | 1000001101100010 |
    | troubleshooter | 10000011011000110 |
    | bouncer | 10000011011000111 |
    | technician | 1000001101100100 |
    | janitor | 1000001101100101 |
    | saleswoman | 1000001101100110 |


- Word embeddings

  for word embeddings you can use exact match. Hopefully in the future we might implement more fancy metrics for comparision like cosine similarity. 
  e.g. `[w2v:"A0F892"])`

#### Chunks and Phrases
  For chunks we recommend to use IOB format

- Noun phrases 

  We use label `NPH` for noun phrase, `BNP` as a value for starting a noun phrase and `INP` for Continue of a noun phrase. Or you can use directly `BNP` as lable and keep the value for the id of that phrase in your knowledge base if any.

### DAGs

- Rdfs 

- Semantic Roles

- Depdencing parsing

  [Parrent:['']]

### Trees 


## How to use

### A note on tokenization 

You can use your own tokenizer and create tokens or use our nltk wrapper to do the tokenization (see examples).
We highly recommend to use a tokenizer that provides start and end of each token in the original text and the normalized value. This is surprizing helpful for visualization and debugging. For instance NLTK PTB tokenizer does not provide these info; so we wrote an script to estimate these from the output for our goal.
Yes, this tool can be seen as an attempt to combine different types of information provided by NLP technologies considering using same tokenization. Currently we have integration with NLTK tokenizer and POS tagger and we are working to connect it to Spacy and google NLP API.

### Examples 

#### Detecting name of painters
```
from tokenregex.nlp.tokenizer import Tokenizer
from tokenregex.nlp.pos_tagger import POSTagger
from tokenregex.tokenregex import TokenRegex

# Penn Tree Bank Tokenizer
tokenizer = Tokenizer('PTBTokenizer')
# NLTK POS tagger
pos_tagger = POSTagger()

# Test sentence
input_text = 'David is a painter and I work as a writer.'
# Tokenizing the sentence
input_tokens = tokenizer.tokenize(input_text)
# adding pos tags
input_tokens = pos_tagger.tag(input_tokens)

# token regex to extract name of the painters
token_regex_1 = TokenRegex('([pos:"NNP"]) [pos:"VBZ"] [/an?/] ["painter"]')
token_regex_1.match_tokens(input_tokens)

# lets change the sentence
input_text = 'David is a famous painter and I work as a writer.'
input_tokens = tokenizer.tokenize(input_text)
input_tokens = pos_tagger.tag(input_tokens)

# because of `famous` now your token regex 1 isn't working anymore
token_regex_1.match_tokens(input_tokens)


# Adding possible adjectives
token_regex_2 = TokenRegex('([pos:"NNP"]) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_2.match_tokens(input_tokens)


# You can add labels directly
input_tokens[0].add_a_label('ner', 'PERSON')


# A mixture of labels will give you the same result
token_regex_3 = TokenRegex('([ner:"PERSON"]) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_3.match_tokens(input_tokens)


# To cover names with more tokens
token_regex_4 = TokenRegex('([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_4.match_tokens(input_tokens)
    
```
