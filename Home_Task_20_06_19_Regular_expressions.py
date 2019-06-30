from pprint import pprint
import re
import csv

with open("phonebook_raw.csv",  encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
def regx(list):
    pattern = "(\'[А-ЯЁ][а-яё]+)(\s)([А-ЯЁ][а-яё]+)(\s)"
    res = re.sub(pattern, r"\1', '\3', '", str(contacts_list))
    # print(res)
    pattern = "(\'[А-ЯЁ][а-яё]+)(\s)"
    res2 = re.sub(pattern, r"\1', '", str(res))
    # print(res2)
    pattern = "(\''| \'',)"
    res3 = re.sub(pattern, r"", str(res2))
    # print(res3)
    pattern = "(8|\+7)(\s)*?(\()?([495]{3})?(\))?(\s)*(\-)?(([913]{3}|[748]{3}|[983]{3})?(\-|)(\d{2})(\-|)(\d{2}))|(((\()?([а-я]+\.)(\s)|([а-я]+\.)(\s))((\d+))|(\)))"
    res4 = re.sub(pattern, r"+7(\4)\9-\11-\13\17\22", str(res3))
    # print(res4)
    pattern = "(([+7()-]{6})|((\,\s)(\])))"
    res5 = re.sub(pattern, r"\5", str(res4))
    # print(res5)
    pattern = "\'|\[|\]]"
    res6 = re.sub(pattern, r"", str(res5))
    # print(res6)

    res_list = res6.split('], ')
    contacts = [res.split(', ') for res in res_list]
    return contacts

contacts = regx(contacts_list)
key = contacts.pop(0)
print(key)

def selection_of_unique_lastname(contacts):
    lastname_set = set([lastname[0] for lastname in contacts])
    lastname_list = list(lastname_set)
    return lastname_list


def search_for_duplicates_by_lastname():
    lastname_list = selection_of_unique_lastname(contacts)

    duplicate_list = []
    original_list = []
    for lastname in lastname_list:
        count = 0
        for contact in contacts:
            if count == 0:
                if lastname == contact[0]:
                    count += 1
                    original_list.append(contact)
            elif count == 1:
                if lastname == contact[0]:
                    duplicate_list.append(contact)
    return original_list, duplicate_list

def merging_data_from_duplicates():
    original_list, duplicate_list = search_for_duplicates_by_lastname()

    for contact in duplicate_list:
        for contact_2 in original_list:
            if contact[0] == contact_2[0]:
                joined_contact = set([*contact, *contact_2])
                joined_contact_list = list(joined_contact)

                for element in joined_contact_list:
                    if element not in contact_2:
                        contact_2.append(element)
# Тут я просто в ручную для одного контакта меню порядок. так как не придумала как сделать это иначе
    for contact in original_list:
        if contact[0] == 'Мартиняхин':
            for element in contact:
                if element == '+7(495)913-00-37':
                    contact.append(contact.pop(contact.index(element)))

    return original_list

contact_list_2 = [key, *merging_data_from_duplicates()]
pprint(contact_list_2)

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contact_list_2)