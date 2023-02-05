from unidecode import unidecode
import copy

class Voseador:
    __ACCENTUATED_VOCALS = {
        "a":"á",
        "e":"é",
        "i":"í", 
        "o":"ó", 
        "u":"ú",
        "A":"Á",
        "E":"É",
        "I":"Í",
        "O":"Ó",
        "U":"Ú"
    }

    __irregular_verbs = {
        "haber":{"indicativo":{"presente":"has",}, 
                 "imperativo":{"afirmativo":"habe"}, 
                 "subjuntivo":{},
                 "condicional":{}
                 },
    }

    __VALID_TENSES_FROM_VOSOTROS = {
        "indicativo":("presente",), 
        "imperativo":("afirmativo", "negativo"),
        "subjuntivo":("presente", "pretérito-perfecto"), 
        "condicional":tuple()

        }

    __MOODS_WITH_SECOND_PERSON = ("indicativo", "imperativo", "subjuntivo", "condicional")
    
    def vos_from_vosotros(self, mood, tense, infinitivo, vosotros_verb):
        if tense not in self.__VALID_TENSES_FROM_VOSOTROS[mood]:
            raise ValueError(f"Invalid tense '{mood} : {tense}' for derivation. Possible tenses are: {self.__VALID_TENSES_FROM_VOSOTROS}")
        
        if self.__is_verb_irregular(infinitivo, mood, tense):
            return self.__get_vos_from_irregularities_table(infinitivo, mood, tense)

        elif mood == "indicativo":
            return self.__get_vos_indicativo_from_vosotros_indicativo(infinitivo, vosotros_verb)
        
        elif mood == "imperativo":
            return self.__get_vos_imperativo_from_vosotros_imperativo(tense, vosotros_verb)
        
        elif mood == "subjuntivo":
            return self.__get_vos_subjuntivo_from_vosotros_subjuntivo(tense, vosotros_verb)

    def add_vos_to_verbecc_conjugation(self, conjugation):
        final_conjugation = copy.deepcopy(conjugation)

        infinitivo = conjugation["moods"]["infinitivo"]["infinitivo"][0]

        for mood in self.__MOODS_WITH_SECOND_PERSON:
            for tense in conjugation["moods"][mood]:
                tense_verbs = conjugation["moods"][mood][tense]
                tense_verbs_with_vos = self.__add_vos_to_verbecc_tense(mood, tense, tense_verbs, infinitivo)
                final_conjugation["moods"][mood][tense] = tense_verbs_with_vos

        return final_conjugation
    
    def __add_vos_to_verbecc_tense(self, mood_name, tense_name, tense_verbs, infinitivo):
        if tense_name in self.__VALID_TENSES_FROM_VOSOTROS[mood_name]:
            vosotros_verb = self.__get_vosotros_verb_from_verbecc_tense_list(mood_name, tense_verbs)
            vos_verb = self.vos_from_vosotros(mood_name, tense_name, infinitivo, vosotros_verb)

        else:
            vos_verb = self.__isolate_verb(tense_verbs[1])

        final_tense_verbs = copy.deepcopy(tense_verbs)
        return self.__insert_verb_in_verbecc_tense_list(mood_name, tense_name, final_tense_verbs, vos_verb)
    
    def __get_vosotros_verb_from_verbecc_tense_list(self, mood_name, tense_verbs):
        if mood_name == "imperativo":
            vosotros_verb = tense_verbs[3]
        else:
            vosotros_verb = tense_verbs[4]
        
        vosotros_verb = self.__isolate_verb(vosotros_verb)

        return vosotros_verb
    
    def __insert_verb_in_verbecc_tense_list(self, mood_name, tense_name, tense_verbs, vos_verb):
        prefix = self.__get_prefix(mood_name, tense_name)
        if mood_name == "imperativo":
            tense_verbs.insert(1, prefix + vos_verb)
        else:
            tense_verbs.insert(2, prefix + vos_verb)
        return tense_verbs

    def __get_vos_indicativo_from_vosotros_indicativo(self, infinitivo, vosotros_verb):
        descinence = unidecode(infinitivo[-2:])

        if descinence == "ir":
            return vosotros_verb
        elif descinence == "er" or descinence == "ar":
            return self.__remove_i_from_vosotros(vosotros_verb)
        else:
            raise ValueError("Invalid infinitivo for verb. Infinitivos should end in ar/er/ir.")
    
    def __get_vos_imperativo_from_vosotros_imperativo(self, tense, vosotros_verb):
        if tense == "afirmativo":
            vosotros_verb = self.__remove_d_from_vosotros_imperativo(vosotros_verb)
            vosotros_verb = self.__add_tilde_to_last_letter(vosotros_verb)
            return vosotros_verb
        else:
            return self.__remove_i_from_vosotros(vosotros_verb)
    
    def __get_vos_subjuntivo_from_vosotros_subjuntivo(self, tense, vosotros_verb):
        if tense == "presente":
            return self.__remove_i_from_vosotros(vosotros_verb)
        elif tense == "pretérito-perfecto":
            words = vosotros_verb.split()
            aux_verb = words[0]
            aux_verb = self.__remove_i_from_vosotros(aux_verb)
            return aux_verb + " " + words[1]

    def __get_vos_from_irregularities_table(self, infinitivo, mood, tense):
        return self.__irregular_verbs[infinitivo][mood][tense]

    def __is_verb_irregular(self, infinitivo, mood, tense):
        if infinitivo in self.__irregular_verbs.keys():
            if tense in self.__irregular_verbs[infinitivo][mood]:
                return True

    def __get_prefix(self, mood, tense):
        if tense == "afirmativo":
            return ""
        elif tense == "negativo":
            return "no "
        else:
            return "vos "

    #"vosotros calláis" -> "calláis"
    def __isolate_verb(self, person_and_verb):
        words = person_and_verb.split()
        if len(words) == 1:
            return person_and_verb
        else:
            return " ".join(words[1:])
    
    #"calláis" -> "callás"
    def __remove_i_from_vosotros(self, verb):
        return verb[:-2] + verb[-1:]
    
    #"callad" -> "calla"
    def __remove_d_from_vosotros_imperativo(self, verb):
        return verb[:-1]
    
    #"calla" -> "callá"
    def __add_tilde_to_last_letter(self, verb):
        return verb[:-1] + self.__ACCENTUATED_VOCALS[verb[-1]]
        
        
    





    
    
