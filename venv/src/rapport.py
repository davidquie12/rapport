from pprint import pprint
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
import os
import libcst as cst
from .LexiconCollector import LexiconCollector , collect_unknown_words
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
class rapport():
    def __init__(self) -> None:
        self.authors = ["david", "andreas", "emmanuel"] # change
        self.alias_authors = {"student_1":"david", "student_2":"andreas", "student_3":"emmanuel"}
        self.opm = ["/", "/", "/"]
        self.matrix = self.create_matrix()
        self.user_directory : str
        
    def create_matrix(self):
        matrix = {author : { comp_author : self.opm.copy() for comp_author in self.authors if comp_author != author } for author in self.authors }
        return matrix
    
    def create_alias_matrix(self):
        alias_matrix = {author : { comp_author : self.opm.copy() for comp_author in self.alias_authors.keys() if comp_author != author } for author in self.alias_authors.keys() }
        #pprint(alias_matrix)
        return alias_matrix
    
    def generate_report(self, matrix):
        output_file = input("Wat is de naam van je output file met extension ? ")  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "outputtemplate.html")  

        with open(output_path, 'r') as file:
            template_content = file.read()
            temp = Template(template_content)
            rendered_template = temp.render(rap=matrix)

            with open(output_file, 'w') as file:
                file.write(rendered_template)
        
    def analyse(self):
        file_trees = {}
        for author in self.authors:
            file_trees[author] = []
            author_directory = input(f"Enter directory for {author}: ")

            if not os.path.exists(author_directory):
                print(f"Directory {author_directory} not found.")
                continue

            for file_name in os.listdir(author_directory):
                file_path = os.path.join(author_directory, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        content = file.read()
                        tree = cst.parse_module(content)
                        file_trees[author].append(tree)

        identical_pairs = {}
        for author, trees in file_trees.items():
            print(f"Files for {author}:")
            for i, tree in enumerate(trees):
                print(f"Tree {i + 1}: {tree.code}")
            print()

        for author, trees in file_trees.items():
            print(f"Comparing files for {author}...")
            trees_without_comments = remove_comments(trees)
            identical_pairs[author] = compare_syntax_trees(trees_without_comments)

        for author, pairs in identical_pairs.items():
            print(f"Identical trees for {author} except for comments:")
            if pairs:
                for pair in pairs:
                    print(f"Trees {pair[0]} and {pair[1]} are identical except for comments.")
            else:
                print("No identical trees found except for comments.")

    def spellcheck(self):
        collector = LexiconCollector()
        dir_path = os.path.join(os.path.abspath("./"), self.user_directory)
        file_list = os.listdir(dir_path)
        tree_list = []

        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                content = f.read()
                tree = cst.parse_module(content)
                tree_list.append(tree)
                tree.visit(collector)

        lexicon = collector.get_all_words()
        return lexicon, tree_list

    def compare_files(self, tree_list):
        for i in range(len(tree_list)):
            for j in range(len(tree_list)):
                if i != j:
                    val = tree_list[i].deep_equals(tree_list[j])
                    if val:
                        author = self.authors[i]
                        comp_author = self.authors[j]
                        self.matrix[author][comp_author] = f"Identical content in files {i} and {j}"
 
    def render(self,file):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, file)
        
        with open(output_path, 'r') as file:
            temp = file.read()
            print(temp)
        
class RemoveCommentsTransformer(cst.CSTTransformer):
    def leave_Comment(self, original_node: cst.Comment) -> cst.RemovalSentinel:
         # Remove all comment nodes
        return cst.RemoveFromParent()


def compare_syntax_trees(tree_list):
    # Compare all syntax trees 
    identical_trees = []
    for i in range(len(tree_list)):
        for j in range(i + 1, len(tree_list)):
            identical = tree_list[i].deep_equals(tree_list[j])
            if identical:
                identical_trees.append((i, j))
    
    return identical_trees


def remove_comments(tree_list):
    transformer = RemoveCommentsTransformer()
    trees_without_comments = [tree.visit(transformer) for tree in tree_list]
    return trees_without_comments


o = rapport()
#o.generate_report(o.create_alias_matrix())
o.render("out.html")
o.analyse()

        



