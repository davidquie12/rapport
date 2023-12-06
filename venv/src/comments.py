import re
import libcst as cst
import os

class comments_Collector():
    def __init__(self, matrix : dict[str, dict[str, list[str]]], user_dir: str) -> None:
        self.matrix = matrix
        self.file_content :dict
        self.parse_content :dict
        self.comments_list :dict
        self.user_dir = user_dir
        self.userT : dict
        self.userT = self.link_author_to_content()
        self.authors = self.userT.keys()
        
        
        
    def link_author_to_content(self, files : list):
        #get author names
        path_origin = os.path.abspath("./"+ self.user_dir) # get current self.user_directory
        currentdir = os.path.dirname(os.path.abspath(path_origin))  #get self.user_directory name from path
        dirc_path =  os.listdir(currentdir) # get directory names
        for dir in range(len(dirc_path)):
            self.user_tasks = {
                {dirc_path[dir] : files[dir]}
            }
        return self.user_tasks
    
    def get_content(self, files : list):
        # get file 
        
        for file,author in files , self.authors:
            with open(f,'r') as f:
            # get content out of files  
                content = f.read()
                
                self.file_content[author]=content
                
    # parse data from files            
    def parse_data(self):
        for file,author in self.file_content, self.authors:
            parsed = cst.parse_module(file[author])
            self.parse_content[author]= parsed
            
    def search_file(self):
        #create regular expression for commented lines
        for content ,author in self.parse_content,self.authors:
            comments = re.findall("^#",content[author])
            self.comments_list[author]=comments
            
    def compare_2_files(self,file_path1 :str, file_path2 :str):
        #check file names
        if file_path1.split('/')[-1] != file_path2.split('/')[-1]:
            return False  # File names are different

        # check file content
        with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()
            
            if content1 == content2:
                return True 
            else:
                return False , content1 , content2
            
    def extract_comment_text(text):
        pattern = r'#(.*)$'
        matches = re.findall(pattern, text, re.MULTILINE)
        comment_texts = [comment.strip() for comment in matches if comment.strip()]

        return comment_texts    
    
    def compare_multiple_files(self,file_paths):
        num_files = len(file_paths)
        identical_files = []

        for i in range(num_files):
            for j in range(i + 1, num_files):  # Compare each file with the rest
                is_identical, content1, content2 = self.compare_2_files(file_paths[i], file_paths[j])
                if not is_identical:
                    self.matrix[file_paths[i]][file_paths[j]] = "identieke comments " + self.extract_comment_text(content1)
                    self.matrix[file_paths[j]][file_paths[i]] = "identieke comments " + self.extract_comment_text(content2)
                    
                    

        return identical_files
    

        
            

        