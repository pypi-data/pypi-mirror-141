import json, os, sys
from wordlehelper.words import LIST as WORLD_LIST

__location_word_list__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


digits = ["first", "second", "third", "fourth", "fifth"]
INPUT_CHARACTERS = "Type {} letter, blank if unknown >> "

def get_all_words(character_array):
    """
    return a list of word that follow the below condition
    for i n range 0:5
        character_array[i] in word[i].

    :param character_array:
    :return:
    """
    resp = []
    for word in WORLD_LIST:
        in_list = True
        for i in range(0, len(word)):
            if character_array[i] not in word[i]:
                in_list = False
        if in_list:
            resp.append(word)
    return resp

def filter_excluded_characters(words, excluded):
    if excluded == None:
        return words
    resp = []
    for word in words:
        if len(list(set(excluded) - set(list(word)))) == len(excluded):
            resp.append(word)
    return resp

def filter_included_characters(words, included):
    if included == None:
        return words
    resp = []
    for word in words:
        if len(list(set(included) - set(list(word)))) == 0:
            resp.append(word)
    return resp

def get_filtered_word_list(position_characters, included_list, not_included_list):
    resp = get_all_words(position_characters)
    print("List with Position Characters", resp)

    if included_list != None:
        resp = filter_excluded_characters(resp, not_included_list)
        print("List After Filter 1, excluded character", resp)

    if not_included_list != not_included_list:
        resp = filter_included_characters(resp, included_list)
        print("List After Filter 2, included character", resp)
    print ("Final List", resp)
    return resp

def execute():
    if sys.argv[1] == "search":
        c_1 = input(INPUT_CHARACTERS.format(digits[0]))
        c_2 = input(INPUT_CHARACTERS.format(digits[1]))
        c_3 = input(INPUT_CHARACTERS.format(digits[2]))
        c_4 = input(INPUT_CHARACTERS.format(digits[3]))
        c_5 = input(INPUT_CHARACTERS.format(digits[4]))

        resp = get_all_words([c_1, c_2, c_3, c_4, c_5])
        print("\nList with Position Characters", resp, "\n")

        included = str(input("Type all character that has to be included in word (separated with comma) >> ")).replace(" ", "")
        if included != "":
            included_arr = included.split(",")
            resp = filter_included_characters(resp, included_arr)
            print("\nList After Filter 2, included character", resp, "\n")

        not_included = str(input("Type all character that has to be excluded from word (separated with comma) >> ")).replace(" ", "")
        if not_included != "":
            not_included_arr = not_included.split(",")
            resp = filter_excluded_characters(resp, not_included_arr)
            print("\nList After Filter 1, excluded character", resp, "\n")
        print("Final List", resp)

if __name__ == '__main__':
    execute()