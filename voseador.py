from unidecode import unidecode
import copy

class Voseador:

    __irregular_verbs = {
        "haber":{"indicativo":"has"},
    }

    __VALID_MOODS_FROM_VOSOTROS = ("indicativo", "imperativo")
    
    def vos_from_vosotros(self, mood, infinitivo, second_person):
        if mood not in self.__VALID_MOODS_FROM_VOSOTROS:
            raise ValueError(f"Invalid mood {mood}. Possible moods are: {self.__VALID_MOODS_FROM_VOSOTROS}")
        
        if infinitivo in self.__irregular_verbs.keys():
            return self.__irregular_verbs[infinitivo][mood]

        elif mood == "indicativo":
            return self.__get_vos_from_vosotros_indicativo(infinitivo, second_person)
        
        elif mood == "imperativo":
            return "-"


    def add_vos_to_verbecc_conjugation(self, conjugation):
        final_conjugation = copy.deepcopy(conjugation)

        infinitivo = conjugation["moods"]["infinitivo"]["infinitivo"][0]

        indicativo_presente = conjugation["moods"]["indicativo"]["presente"]
        indicativo_presente = self.__add_vos_to_verbecc_indicativo_presente(infinitivo, indicativo_presente)
        final_conjugation["moods"]["indicativo"]["presente"] = indicativo_presente

        return final_conjugation
    
    def __add_vos_to_verbecc_indicativo_presente(self, infinitivo, indicativo_presente):
        if infinitivo in self.__irregular_verbs.keys():
            indicativo_vos = self.__irregular_verbs[infinitivo]["indicativo"]
        else:
            indicativo_vosotros = self.__isolate_verb(indicativo_presente[4])
            indicativo_vos = self.__get_vos_from_vosotros_indicativo(infinitivo, indicativo_vosotros)
            
        indicativo_presente.insert(2, "vos " + indicativo_vos)
        return indicativo_presente
       
    def __get_vos_from_vosotros_indicativo(self, infinitivo, second_person):
        descinence = unidecode(infinitivo[-2:])

        second_person_verb = self.__isolate_verb(second_person)
        if descinence == "ir":
            return second_person_verb
        elif descinence == "er" or descinence == "ar":
            return self.__remove_i_from_vosotros(second_person_verb)
        else:
            raise ValueError("Invalid infinitivo for verb. Infinitivos should end in ar/er/ir.")
    
    #"vosotros calláis" -> "calláis"
    def __isolate_verb(self, person_and_verb):
        return person_and_verb.split()[-1]
    
    #"calláis" -> "callás"
    def __remove_i_from_vosotros(self, verb):
        return verb[:-2] + verb[-1:]
        
    





    
    
