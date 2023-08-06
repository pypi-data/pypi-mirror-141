# pyright:reportUnknownMemberType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownLambdaType=false

import re
from typing import Any, List

import en_core_web_sm

from py_pdf_term._common.consts import ALPHABET_REGEX, SYMBOL_REGEX

from .data import Token
from .base import BaseLanguageTokenizer


class EnglishTokenizer(BaseLanguageTokenizer):
    def __init__(self) -> None:
        enable_pipes = ["tok2vec", "tagger", "attribute_ruler", "lemmatizer"]
        self._model = en_core_web_sm.load()
        self._model.select_pipes(enable=enable_pipes)

        self._en_regex = re.compile(ALPHABET_REGEX)
        self._symbol_regex = re.compile(rf"({SYMBOL_REGEX})")

    def inscope(self, text: str) -> bool:
        return self._en_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Token]:
        text = self._symbol_regex.sub(r" \1 ", text)
        return list(map(self._create_token, self._model(text)))

    def _create_token(self, token: Any) -> Token:
        if self._symbol_regex.fullmatch(token.text):
            return Token("en", token.text, "SYM", "*", "*", token.text)

        return Token(
            "en", token.text, token.pos_, token.tag_, "*", token.lemma_.lower()
        )
