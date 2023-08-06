import re
from collections import Counter



class DocumentTermMatrix:
    
    def __init__(self, df, text_column, response_column):
        self.df = df
        self.text_column = text_column
        self.response_column = response_column
        self.__dictionary = None
        
    def __repr__(self):
        df = self.df
        nr = df.shape[0]
        nc = df.shape[1]
        tcol = self.text_column
        rcol = self.response_column
        ret1 = "|------------------- DTM -------------------|\n"
        ret2 = f"| -- input data of {nr} rows and {nc} columns\n"
        ret3 = f"| -- text column name: {tcol}\n"
        ret4 = f"| -- response column name: {rcol}\n"
        ret5 = "|------------------------------------------|"
        return f"{ret1}{ret2}{ret3}{ret4}{ret5}"
    
    
    def __return_stopwords(self):
        stop_words = [
            "a", "about", "above", "above", "across", "after", 
            "afterwards", "again", "against", "all", "almost", 
            "alone", "along", "already", "also","although",
            "always","am","among", "amongst", "amoungst", 
            "amount",  "an", "and", "another", "any","anyhow",
            "anyone","anything","anyway", "anywhere", "are", 
            "around", "as",  "at", "back","be","became", 
            "because","become","becomes", "becoming", "been", 
            "before", "beforehand", "behind", "being", "below", 
            "beside", "besides", "between", "beyond", "bill", 
            "both", "bottom","but", "by", "call", "can", "cannot", 
            "cant", "co", "con", "could", "couldnt", "cry", "de", 
            "describe", "detail", "do", "done", "down", "due",
            "during", "each", "eg", "eight", "either", "eleven",
            "else", "elsewhere", "empty", "enough", "etc", "even", 
            "ever", "every", "everyone", "everything", "everywhere", 
            "except", "few", "fifteen", "fify", "fill", "find", 
            "fire", "first", "five", "for", "former", "formerly",
            "forty", "found", "four", "from", "front", "full", 
            "further", "get", "give", "go", "had", "has", "hasnt", 
            "have", "he", "hence", "her", "here", "hereafter", "hereby",
            "herein", "hereupon", "hers", "herself", "him", "himself",
            "his", "how", "however", "hundred", "ie", "if", "in", "inc",
            "indeed", "interest", "into", "is", "it", "its", "itself",
            "keep", "last", "latter", "latterly", "least", "less", "ltd",
            "made", "many", "may", "me", "meanwhile", "might", "mill", 
            "mine", "more", "moreover", "most", "mostly", "move", "much",
            "must", "my", "myself", "name", "namely", "neither", "never", 
            "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
            "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", 
            "on", "once", "one", "only", "onto", "or", "other", "others",
            "otherwise", "our", "ours", "ourselves", "out", "over", "own",
            "part", "per", "perhaps", "please", "put", "rather", "re", 
            "same", "see", "seem", "seemed", "seeming", "seems", "serious",
            "several", "she", "should", "show", "side", "since", "sincere", 
            "six", "sixty", "so", "some", "somehow", "someone", "something",
            "sometime", "sometimes", "somewhere", "still", "such", "system",
            "take", "ten", "than", "that", "the", "their", "them", 
            "themselves", "then", "thence", "there", "thereafter", "thereby",
            "therefore", "therein", "thereupon", "these", "they", "thick", 
            "thin", "third", "this", "those", "though", "three", "through", 
            "throughout", "thru", "thus", "to", "together", "too", "top", 
            "toward", "towards", "twelve", "twenty", "two", "un", "under", 
            "until", "up", "upon", "us", "very", "via", "was", "we", "well",
            "were", "what", "whatever", "when", "whence", "whenever", "where", 
            "whereafter", "whereas", "whereby", "wherein", "whereupon", 
            "wherever", "whether", "which", "while", "whither", "who",
            "whoever", "whole", "whom", "whose", "why", "will", "with", 
            "within", "without", "would", "yet", "you", "your", "yours", 
            "yourself", "yourselves", "the"
        ]
        return stop_words
    
    def __flatten(self, lol, rem_dups = True, keep_order = True):
        if rem_dups:
            flat_list = [item for sublist in lol for item in sublist]
            if keep_order:
                ret = list(dict.fromkeys(flat_list))
            else:
                ret = list(set(flat_list))
        else:
            ret = [item for sublist in lol for item in sublist]
        return ret
        
    def __make_wordsplit(self, df = None, clean_html = True):
        if df is None: 
            df = self.df
        text_col = self.text_column
        if clean_html:
            remove_strings = "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"
        else:
            remove_strings = "[.,!?:;-@#]"
        rs_compiled = re.compile(remove_strings)
        ret = []
        for r in range(len(df)):
            tmp_sent = df.loc[r, text_col]
            tmp_sent_clean = re.sub(rs_compiled, '', tmp_sent)
            tmp_split = [s.lower() for s in tmp_sent_clean.split(" ")]
            ret.append(tmp_split)
        return ret
    
    def __make_dictionary(self, rem_stp_wrds, stp_wrds_lst):
        split_word_list = self.__make_wordsplit()
        ret = self.__flatten(split_word_list)
        if rem_stp_wrds:
            if stp_wrds_lst is None:
                use_stop_words = self.__return_stopwords()
                ret = [r for r in ret if r not in use_stop_words]
            else:
                ret = [r for r in ret if r not in stp_wrds_lst]
        return ret
    
    
    def dtm(self, remove_stopwords = True, stopword_list = None):
        use_dictionary = self.__make_dictionary(
            rem_stp_wrds = remove_stopwords, 
            stp_wrds_lst = stopword_list
        )
        self.__dictionary = use_dictionary
        split_word_list = self.__make_wordsplit()
        ret_lst = []
        for l in range(len(split_word_list)):
            tmp_ret_siw = split_word_list[l]
            tmp_count = Counter(tmp_ret_siw)
            res = [tmp_count[word] for word in use_dictionary]
            ret_lst.append(res)
        ret_array = np.array(ret_lst).reshape(len(ret_lst), len(use_dictionary))
        ret_df = pd.DataFrame(ret_array)
        ret_df.columns = use_dictionary
        ret_df["RESPONSE"] = self.df[self.response_column]
        return ret_df
    
    
    def new_dtm(self, new_df):
        use_dictionary = self.__dictionary
        split_word_list = self.__make_wordsplit(df = new_df)
        ret_lst = []
        for l in range(len(split_word_list)):
            tmp_ret_siw = split_word_list[l]
            tmp_count = Counter(tmp_ret_siw)
            res = [tmp_count[word] for word in use_dictionary]
            ret_lst.append(res)
        ret_array = np.array(ret_lst).reshape(len(ret_lst), len(use_dictionary))
        ret_df = pd.DataFrame(ret_array)
        ret_df.columns = use_dictionary
        return ret_df
