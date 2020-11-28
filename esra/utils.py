import re
import spacy
import en_core_web_md
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex

def custom_tokenizer(nlp):
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9\.])[:<>=()+—](?=[{a}0-9\.])".format(a=ALPHA),
            r"(?<=[A-Za-z]{2})/(?=[A-Za-z]{2})",
            r"(?:[{a}]\.)+ [{a}0-9]".format(a=ALPHA),
        ]
    )

    infix_re = compile_infix_regex(infixes)
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes + ('-',))
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes + ('-',))

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=nlp.tokenizer.token_match,
                                rules=nlp.Defaults.tokenizer_exceptions)

nlp = en_core_web_md.load()
nlp.tokenizer = custom_tokenizer(nlp)

def nlp_split(text):
    text = re.sub(r'[(\-\-\-|\-\-|\-|\->)]', '-', text)
    text = re.sub(r'[\[\]"‘’“”!$~`#]', ' ', text)
    text = re.sub(r'[!?]', '.', text)
    text = re.sub(r'\\cite{.*}', ' ', text)
    text = re.sub(r'\\[(leftrightarrow|mid|vec)]', ' ', text)
    text = re.sub(r'[(extit|mph|extsl)]\{(.*)\}', '\\1', text)
    text = re.sub(r'\\[(url|textit|mph)]\{(.*?)\}', '\\1', text)
    text = re.sub(r'[\{\}\\]', ' ', text)
    text = ' '.join(text.split())
    return nlp(text)