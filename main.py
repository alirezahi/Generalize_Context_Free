import string
from itertools import chain, combinations

# Alphabet of our language
alphabet = list(string.ascii_lowercase)
# Variables used in our language
variables = list(string.ascii_uppercase)


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))

class ContextFree():
    def __init__(self,r,s):
        self.v = variables
        self.sigma = alphabet
        self.r = r
        self.s = s

    def generalize(self):
        self.__remove_lambda()
        self.__remove_useless_variables()

    def __remove_lambda(self):
        v_n = []
        for leading_rule,result_rule in self.r.items():
            for right_result in result_rule:
                if right_result == 'λ':
                    v_n.append(leading_rule)
        sth_new_added = True
        while sth_new_added:
            sth_new_added = False
            for leading_rule,result_rule in self.r.items():
                if leading_rule not in v_n:
                    need_to_be_vn = False
                    for right_result in result_rule:
                        need_to_be_vn = False
                        for element in right_result:
                            if not(element in variables):
                                need_to_be_vn = True
                    if need_to_be_vn:
                        sth_new_added = True
                        v_n.append(leading_rule)
        new_grammer = {}
        for leading_rule, result_rule in self.r.items():
            for right_result in result_rule:
                for combination in powerset(v_n):
                    if len(combination) > 0:
                        for element_of_combination in combination:
                            new_result = right_result.replace(element_of_combination,'')
                            new_result = new_result.replace('λ', '')
                        if len(new_result) > 0:
                            if leading_rule not in new_grammer:
                                new_grammer[leading_rule] = []
                            new_grammer[leading_rule].append(new_result)
        for leading,result in new_grammer.items():
            new_grammer[leading] = list(set(result))
        self.r = new_grammer

    def __remove_useless_variables(self):
        using_variables_type_one = []
        using_variables_type_two = [self.s]
        using_variables_type_three = []
        continue_bool = True
        while continue_bool:
            continue_bool = False
            for leading,res in self.r.items():
                for element in res:
                    endless = False
                    for letter in element:
                        if (letter in alphabet) or (letter in using_variables_type_one):
                            endless = True
                    if endless and leading not in using_variables_type_one:
                        using_variables_type_one.append(leading)
                        continue_bool = True
        while len(using_variables_type_two) > 0:
            goal = using_variables_type_two.pop()
            using_variables_type_three.append(goal)
            for element in self.r[goal]:
                for letter in element:
                    if letter in variables and letter not in using_variables_type_two and letter not in using_variables_type_three:
                        using_variables_type_two.append(letter)
        new_rule = {}
        for leading,res in self.r.items():
            for element in res:
                add = True
                for letter in element:
                    if letter in variables and (letter not in using_variables_type_one or letter not in using_variables_type_three):
                        add = False
                if add:
                    if leading not in new_rule:
                        new_rule[leading] = []
                    new_rule[leading].append(element)

        
                        



c = ContextFree({'S': ['λ', 'Ab'], 'A': ['λ','a','B'],'B':{'B'}},'S')
c.generalize()
