from spellchecker import SpellChecker
import libcst as cst
import keyword

class LexiconCollector(cst.CSTVisitor):
    def __init__(self):
        self.spell = SpellChecker()
        
        self.voc = []

    def visit_SimpleString(self, node: cst.SimpleString):
        words = node.value.replace('\n', ' ').split()
        for word in words:
            if not keyword.iskeyword(word):
                self.voc.append(word.lower())

    def visit_name(self, node: cst.Name) -> None:
        self.voc.append(node.value.lower())
        
    def get_all_words(self):
        return self.voc
    


