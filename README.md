<p align="left">
  <img src="https://raw.githubusercontent.com/ramtinms/tokenregex/master/resources/Token_query_logo.png" width="350"/>
</p>

**TokenQuery** is a query language over any labeled text (sequence of tokens); very similar to regular expressions but on top of tokens. TokenQuery can be viewed as an interface to query for specific patterns in a sequence of tokens using information provided by diverse NLP engines.


# What is a `Token`?
In order to process text (natural language text), the common approach for natural language processing (NLP) is to break the text down into smaller processing units (tokens). Options include phonemes, morphemes, lexical information, phrases, sentences, or paragraphs. 


<p align="left">
  <img src="https://raw.githubusercontent.com/ramtinms/tokenregex/master/resources/TokenQuery_example_1.png" />
</p>


e.g.  sentence
`President Obama delivered his Farewell Address in Chicago on January 10, 2017.`

# colors from different engines 



tokens 

Currently many NLP engines extracts information from a text and provide those information in the format of diverse set of labels over tokens. TokenQuery
- Enables us to combine labels from different NLP engines 
- Query and reasoning over tokenized text
- Defining extentions for labeled-based processing


 token sequences




One of the challeneges for natural language processing, is the fact that each unit is providing isolated information about each token in different formats and currently is really hard to have a query considering labels coming from different processing units. 




#############################
Data modeling
In NLP applications, text is typically tokenized into
units of characters (tokens).
tokens are mutli-faceted information 
Each token contains few properties. 
Each token contains few basic fields and fields key, value pairs 
specials fields 
    text (textual content of token)
    start_offset
    end_offset
    meta

You can define as many labels (key/values pairs) you want for each token and check if each label matches or not. 

#################################


In tokenregex, each token contains a text, start offset and end offset of the span inside the original text, and a list of key value pairs which we call the key as label and the value as the value for that label. 

# Where the idea came from.
The inital idea came from *Angel Chang* and *Christopher Manning* presented in [this paper](http://nlp.stanford.edu/pubs/tokensregex-tr-2014.pdf). They have implemeneted it (TOKENSREGEX) in Java inside *Stanford CoreNLP* software package. Our version uses a different language for the query which is extensible, more structured, and supporting more features. 


# Tokenregex language
The language is defined as follow. Each query consists of a group of tokens shown each inside `[` `]`s. If you want to use `]` inside your token matches you can simply use `\` to skip.


```
[expr_for_token1][expr_for_token2][expr_for_token3]
```
which means we are searching for a sequence of three tokens that the first token satisfies the condition provided by expr_for_token1, the second token satisfies the condition provided by expr_for_token2 and so on. 

## Quantifiers
Likewise regular expressions, you can use quantifiers to have more compact tokenregexes. For example the following query will match zero or more tokens satisfying the condition provided by expr_for_token1 followed by another token satisfies condition provided by expr_for_token2.
```
[expr_for_token1]*[expr_for_token2]
```

|----|----|----| 
| type | occurrence | example |
| `?` | once or not at all | `[expr_for_token]?` |
| `*` | zero or more times | `[expr_for_token]*` |
| `+` | one or more times | `[expr_for_token]+` |
| `{x}` | x number of times | `[expr_for_token]{3}` |
| `{x,y}` | between x and y number of times | `[expr_for_token]{3,5}` |


## Capturing and Groups
Like reguar expressions, you can define capturing groups by parentheses. 
for example `([expr_for_token1]+) [expr_for_token2] [expr_for_token3]` returns a group containing sequence of tokens with satisfies the condition provided by expr_for_token1. Hence, `([expr_for_token1]+) [expr_for_token2] ([expr_for_token3])` returns two groups with a list of tokens matched inside each parentheses. 

If you don't provide any, it will capture all as a single group. For example, `[expr_for_token1]+ [expr_for_token2] [expr_for_token3]` is equal to `([expr_for_token1]+ [expr_for_token2] [expr_for_token3])`.



## Token Expression
Expressions (like `expr_for_token1` in the above examples) can be viewed as a list of acceptors for each token. 

# Basic expressions
`[label:operation(operation_input)]` is the base form for defining a token expression, in which, `label` selects the value for the label from the token and `operation` is the required operation on top of this value which return True or False. Operations can also get extra input strings which is provided by `operation_input`. 
For example, `[pos:str_eq(VBZ)]` matches any token that has a label `pos` and the string value for that is equal to `VBZ`.
or `[pos:str_reg(V.*)]` matches any token that has a `pos` label and the value for that label matches regex `V.*`. (i.e. any verbs)
Note: If you want to check if a label exists or not and you don't care about the value of the label you can simply use this `[pos:str_reg(.*)]`.
If no label provided the default will consider the text of the token. For example, `[str_reg(.*)]` will match any token or `[str_reg('painter')]` matches any token that has 'painter' as text.

### core operations (acceptors)
Here is the list of predefined operations. Note that in this framework an extiontion format is considered for your own desired operations.  

## String 

  str_eq 

  str_reg

  str_len



  Examples 

  Shortened versions, 
  
  Exact string match is possible by having the text you want to match inside `"`s.
For example `["painter"]` will match any token that its text is `painter` but not `Painter`.

### Regex match 
If you want to find tokens that matches a regex you can have your regex inside `/`s . 
For example `[/an?/]` matches tokens having text `a` or `an`. 
`[/Al.*/]` matches any token starting with `Al`.
`[/km|kilometers?/]` matches `km`, `kilometer` and `kilometers`
Note that you can use `/` inside the regex without any modification, we only care extra first `/` and last `/`. 

`[len>20]` will check if the len of a token is more than 20


## Int
  
  Examples 
  
  int_value

  int_e

  int_g

  int_l

  int_ne

  int_le

  int_ge





### Value match
Currenlty we only support a limited set of value operation over token. Hopefully in the future we have more operations over each token. 

`[num>30]` will check if the token is an int and greater than 30.
These comparisions ( >=, <. <=, ==, !=) are also available.



## Web
  web_is_url
  web_is_email
  web_is_hex_code
  web_is_hashtag
  web_is_emoji



## Date

  String iso format

  date_is 
  date_is_after
  date_is_before
  date_y_is
  date_m_is
  date_d_is


# compound expressions
For each token is possible to compound several basic expressions to support more complex patterns. Compounding is done using `!` (not), `&` (and) and `|` (or) symbols. For example, [!pos:str_reg(V.*)] means any token that it is not a verb. 
`[pos:str_reg(V.*)&!str_eq(is)]` matches any verb except `is`. 

## what is the priority of compounding
 The `!` has the highest proiority and the `&` and `|` has same priority and right associative. You can change the priority by using parentheses. 
```
!X and Y        <=>   ( (!(X)) and Y )
!(X and Y)      <=>   ( !(X and Y) )
!(X and Y) or Z <=>   ( ( !(X and Y) ) or Z )
(X and Y) or Z  <=>   ( ( X and Y) or Z )
X and Y or Z    <=>   ( X and (Y or Z) )
```

## How to install 
```
pip install tokenregex
```

## Other NLP Examples
We belive a big portion of NLP information can be expressed in terms of labels on top of tokens. Here is a list of the ones currently we use and how we represent it. Please note that you can define your own lables and there is no limitation in theory for this package.
- Part Of Speech tags (e.g. `[pos:/V.*/]`)

- Lemma  (e.g. `[lemma:'be']`)

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