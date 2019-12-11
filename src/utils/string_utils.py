import re
import unicodedata
import string
import hashlib

class StringUtils:
    @staticmethod
    def reduce_ligne_de_points(word):
        return re.sub(r"\.\.\.(\.)+", "....", word)

    @staticmethod
    def text_to_char_list(txt):
        return [char for char in txt]

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    @staticmethod
    def reduce_ligne_de_ptsusp(word):
        return re.sub(r"(&ptsup)+", "....", word)


    @classmethod
    def normalize_as_valid_filename_string(cls, s):
        s_mod = StringUtils.strip_accents(s)
        return re.sub(" ", "_", s_mod)




class HashUtils:

    @classmethod
    def normalize_string_and_append_hash(cls, s):
        s_mod = StringUtils.normalize_as_valid_filename_string(s)
        s_mod += "_§_"
        s_hash = s_mod + str(cls.get_sha1(s))  # str(my_own_string_hash(s, modulo_int, ord_function, alphabet_len))
        return s_hash

    @classmethod
    def get_sha1(cls, s):
        return hashlib.sha1(str.encode(s)).hexdigest()



