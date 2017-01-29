<p align="left">
  <img src="https://raw.githubusercontent.com/ramtinms/tokenquery/master/resources/Token_query_logo.png" width="350"/>
</p>

**TokenQuery** is a query language over any labeled text (sequence of tokens); very similar to regular expressions but on top of tokens. TokenQuery can be viewed as an interface to query for specific patterns in a sequence of tokens using information provided by diverse NLP engines.


## What is a `Token`?
In order to process text (natural language text), the common approach for natural language processing (NLP) is to break the text down into smaller processing units (tokens). Options include phonemes, morphemes, lexical information, phrases, sentences, or paragraphs. For example, this sentence :`President Obama delivered his Farewell Address in Chicago on January 10, 2017.` can be divided into tokens shown in blue highlights. 

<p align="left">
  <img src="https://raw.githubusercontent.com/ramtinms/tokenquery/master/resources/TokenQuery_example_1.png" />
</p>
Inside TokenQuery each token contains a text (textual content of token), start and end index of the span inside the original text and a set of labels (i.e. key/value pairs) provided by NLP engines. In our example, the red labels (POS tags) are coming from Stanford POS tagger, the orange labels are from Google NLP API, and purple ones are coming from an internal topic extractor. One of the challeneges for natural language processing, is the fact that each unit is providing isolated information about each token in different formats and currently is really hard to have a query considering labels coming from different processing units. 

TokenQuery enables us to 
- Combine labels from different NLP engines 
- Query and reasoning over tokenized text
- Defining extentions for desired query functions

The inital idea came from *Angel Chang* and *Christopher Manning* presented in [this paper](http://nlp.stanford.edu/pubs/tokensregex-tr-2014.pdf). They have implemeneted it (TOKENSREGEX) in Java inside *Stanford CoreNLP* software package. Our version uses a different language for the query which is extensible, more structured, and supporting more features. 


## TokenQuery language
The language is defined as follow. Each query consists of a group of tokens shown each inside `[` `]`s. If you want to use `]` inside your token matches you can simply use `\` to skip.


```
[expr_for_token1][expr_for_token2][expr_for_token3]
```
which means we are searching for a sequence of three tokens that the first token satisfies the condition provided by `expr_for_token1`, the second token satisfies the condition provided by `expr_for_token2` and so on. 

## Quantifiers
Likewise regular expressions, you can use quantifiers to have more compact queries. For example, the following query will match zero or more tokens satisfying the condition provided by `expr_for_token1` followed by another token satisfies condition provided by `expr_for_token2`.
```
[expr_for_token1]*[expr_for_token2]
```
| type | occurrence | example |
| ----  | ---- | ---- | 
| `?` | once or not at all | `[expr_for_token]?` |
| `*` | zero or more times | `[expr_for_token]*` |
| `+` | one or more times | `[expr_for_token]+` |
| `{x}` | x number of times | `[expr_for_token]{3}` |
| `{x,y}` | between x and y number of times | `[expr_for_token]{3,5}` |

## Capturing Groups
Like reguar expressions, you can define capturing groups by parentheses. 
for example `([expr_for_token1]+) [expr_for_token2] [expr_for_token3]` returns a group containing sequence of tokens with satisfies the condition provided by expr_for_token1. Hence, `([expr_for_token1]+) [expr_for_token2] ([expr_for_token3])` returns two groups (`chunk1` and `chunk2`) with a list of tokens matched inside each parentheses. You can also use named capturing by using `(name <desired_pattern>)`. For example `(name [expr_for_token1])` captures results under the name of `name`.
If you don't provide any, it will capture all as a single group; in other words,  `[expr_for_token1]+ [expr_for_token2] [expr_for_token3]` is equal to `([expr_for_token1]+ [expr_for_token2] [expr_for_token3])`.

## Token Expression
Expressions (like `expr_for_token1` in the above examples) can be viewed as a list of acceptors for each token.

### Basic expressions
`[label:operation(operation_input)]` is the base unit for defining a token expression, which means running `operation` on the value of `label` for this token returns if we should accept this token or not. `operation` is a function that accepts a token and optional extra setting string (`operation_input`) and returns `True` or `False`. 
For example, `[pos:str_eq(VBZ)]` matches any token that has a label `pos` and the string value for that is equal to `VBZ`. `str_eq` is an standard string operation check if the string is equal the extra setting string. 
or `[pos:str_reg(V.*)]` matches any token that has a `pos` label and the value for that label matches regex `V.*`. (i.e. any verbs)
Note: If you want to check if a label exists or not and you don't care about the value of the label you can simply use this `[pos:str_reg(.*)]`.
If no label provided the default will consider the text of the token. For example, `[str_reg(.*)]` will match any token or `[str_reg('painter')]` matches any token that has 'painter' as text.

### core operations (acceptors)
Here is the list of predefined operations. You can extend this framework with your own defined operations.  

#### String 
   This package provides string operations described below.
   
| operation | description | examples | 
| ----  | ---- | ---- |
| `str_eq` | string equals to extra setting string | `[str_eq(Obama)]` , `[pos:str_eq(VBZ)]` |
| `str_reg` | string matches regex provided by extra setting string | `[str_req(an?)]`, `[pos:str_eq(V.*)]`  |
| `str_len` | lenght of the string compared to the value of extra setting string. (`==`, `>`, `<`, `!=` ,`>=`, `<=`)  | `[str_len(=12)]`, `[ner:str_len(>6)]`, `[str_len(!=2)]` |

**Shortened versions**   
  For the convinence of use, exact string match is possible by having the text you want to match inside `"`s.
For example `["painter"]` will match any token that its text is `painter` but not `Painter`.
If you want to find tokens that matches a regex you can have your regex inside `/`s . For example `[/an?/]` matches tokens having text `a` or `an`. 
`[/Al.*/]` matches any token starting with `Al`.
`[/km|kilometers?/]` matches `km`, `kilometer` and `kilometers`

#### Int
 This package provides operations that will cast the value of labels into an integer and apply arithmetic operations on that. 
   
| operation | description | examples | 
| ----  | ---- | ---- |
| `int_value` | casts the value of label into an integer and compare it to the integer provided by extra setting string  (`==`, `>`, `<`, `!=` ,`>=`, `<=`)  | `[int_value(==5)]` , `[month:int_value(>1)]`, `[year:int_value(>1990)]` |
| `int_e` | casts the value of label into an integer and check if it is equal to int provided by extra setting string.  | `[int_value(5)]` , `[month:int_value(1)]` |
| `int_g` | `int_g(X)` is equivalent to use `int_value(>X)`  | `[month:int_g(1)]` |
| `int_l` | `int_l(X)` is equivalent to use `int_value(<X)`  | `[month:int_l(6)]` |
| `int_ne` | `int_ne(X)` is equivalent to use `int_value(!=X)`  |  `[int_ne(13)]` |    
| `int_le` | `int_le(X)` is equivalent to use `int_value(<=X)` | `[int_le(12)]` |    
| `int_ge` | `int_ge(X)` is equivalent to use `int_value(>=X)` | `[int_ge(0)]` |

#### Web
This package provides operations for capturing meaningful web patterns.
| operation | description | examples | 
| ----  | ---- | ---- |
| `web_is_url` | the string is a web url  | `[text:web_is_url()]` , `[freebase_id:web_is_url()]`|
| `web_is_email` | the string is an email  | `[text:web_is_email()]` , `[contact:web_is_email()]`|
| `web_is_emoji` | the string is an emoji or emojicon  | `[text:web_is_emoji()]` |
| `web_is_hex_code` | the string is a hex code | `[color:web_is_hex_code()]` |
| `web_is_hashtag` | the string is a hashtag  | `[tag:web_is_hashtag()]` |
  
#### Date
This package provides operations for working with date and time info in iso format.

| operation | description | examples | 
| ----  | ---- | ---- |
| `date_is` | the date in iso format is same as extra setting string  | `[date:date_is(2008-09-15T15:53:00)]`|
| `date_is_after` | the date in iso format is after the date in extra setting string | `[date:date_is_after(2008-09-15)]` |
| `date_is_before` | the date in iso format is before the date in extra setting string | `[date:date_is_before(2008-09-15)]` |
| `date_y_is` | the year of the date in iso format is equal to the month in extra setting | `[date:date_y_is(2008)]` |
| `date_m_is` | the month of the date in iso format is equal to the month in extra setting | `[date:date_m_is(9)]`,  `[date:date_m_is(09)]`|
| `date_d_is` | the day of the date in iso format is equal to the month in extra setting | `[date:date_y_is(15)]` |

## compound expressions
For each token is possible to compound several basic expressions to support more complex patterns. Compounding is done using `!` (not), `&` (and) and `|` (or) symbols. For example, `[!pos:str_reg(V.*)]` means any token that it is not a verb. 
`[pos:str_reg(V.*)&!str_eq(is)]` matches any verb except `is`. 
 The `!` has the highest proiority and the `&` and `|` has same priority and right associative. You can change the priority by using parentheses. 
```
!X and Y        <=>   ( (!(X)) and Y )
!(X and Y)      <=>   ( !(X and Y) )
!(X and Y) or Z <=>   ( ( !(X and Y) ) or Z )
(X and Y) or Z  <=>   ( ( X and Y) or Z )
X and Y or Z    <=>   ( X and (Y or Z) )
```

# How to install 
```
pip install tokenquery
```
It has been test to work on python 2.7+ 

## How to use
You can use your own tokenizer and create tokens or use our nltk wrapper to do the tokenization (see examples).
We highly recommend to use a tokenizer that provides start and end of each token in the original text and the normalized value. This is surprizing helpful for visualization and debugging. For instance NLTK PTB tokenizer does not provide these info; so we wrote an script to estimate these from the output for our goal.
Yes, this tool can be seen as an attempt to combine different types of information provided by NLP technologies considering using same tokenization. Currently we have integration with NLTK tokenizer and POS tagger and we are working to connect it to Spacy and google NLP API.

## NLP Examples
We belive a big portion of NLP information can be expressed in terms of labels on top of tokens. Here is a list of the ones currently we use and how we represent it. 
- Part Of Speech tags (e.g. `[pos:/V.*/]`)

- Lemma  (e.g. `[lemma:'be']`)

- Named-Entity tags (e.g. `[ner:"PERSON"]`)

- Brown clusters

    | label | We | need | a | lawyer | . |
    |----|----|----|----|----|----|
    | POS | `PRP` | `VBP` | `DT` | `NN` | `.` |
    | bcluster| | | |`1000001101000` | 
    
    And we can query members inside a cluster by tokenquery like this:
  `[bcluster:/100000110[0-1]+/])`
   which will match all of these and more. (for more info see Miller et al., NAACL 2004)
   
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
  For word embeddings you can use exact match. You can also define fancy metrics for comparision like cosine similarity as an operation. implemente more  like . 
  e.g. `[w2v:cos_sim(A0F892<0.5)])`

#### Chunks and Phrases
  For chunks we recommend to use IOB formatting.
  
- Noun phrases 
  We use label `N-PH` for noun phrase, `B-NP` as a value for starting a noun phrase and `I-NP` for Continue of a noun phrase. Or you can use directly `B-NP` as lable and keep the value for the id of that phrase in your knowledge base if any.

### Examples 

#### Detecting name of painters
```
from tokenquery.nlp.tokenizer import Tokenizer
from tokenquery.nlp.pos_tagger import POSTagger
from tokenquery.tokenquery import TokenQuery

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
token_regex_1 = TokenQuery('([pos:"NNP"]) [pos:"VBZ"] [/an?/] ["painter"]')
token_regex_1.match_tokens(input_tokens)

# lets change the sentence
input_text = 'David is a famous painter and I work as a writer.'
input_tokens = tokenizer.tokenize(input_text)
input_tokens = pos_tagger.tag(input_tokens)

# because of `famous` now your token regex 1 isn't working anymore
token_regex_1.match_tokens(input_tokens)

# Adding possible adjectives
token_regex_2 = TokenQuery('([pos:"NNP"]) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_2.match_tokens(input_tokens)

# You can add labels directly
input_tokens[0].add_a_label('ner', 'PERSON')

# A mixture of labels will give you the same result
token_regex_3 = TokenQuery('([ner:"PERSON"]) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_3.match_tokens(input_tokens)

# To cover names with more tokens
token_regex_4 = TokenQuery('([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] [pos:"JJ"]* ["painter"]')
token_regex_4.match_tokens(input_tokens)
    
```