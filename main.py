from pprint import pprint
import csv
import re
import os

def read_csv(file_name):
    contacts_dict = []
    with open(file_name, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        keys = contacts_list[0]
        values = contacts_list[1:]
        for num, vals in enumerate(values):
            contacts_dict.append({})
            for key, val in zip(keys, vals):
                contacts_dict[num].update({key:val})
    return contacts_dict

def fix_phones(in_file,out_file):
    with open(in_file, encoding="utf-8") as f:
        text = f.read()
    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
    with open(out_file, 'w+', encoding="utf-8") as f:
        text = f.write(fixed_phones)

def fix_names(file_name):
        contact_dicts = read_csv(file_name)
        for v in contact_dicts:
            splt = v['lastname'].split(' ')
            if len(splt) > 1:
                v['lastname'] = splt[0]
                v['firstname'] = splt[1]
                if len(splt) > 2:
                   v['surname'] = splt[2]
            splt = v['firstname'].split(' ')
            if len(splt) >1:
                v['firstname'] = splt[0]
                v['surname'] = splt[1]

        return contact_dicts

def uniq_name(file_name):
    new_contact_dicts = []
    contact_dicts = fix_names(file_name)
    for contact in contact_dicts:
        firstname = contact['firstname']
        lastname = contact['lastname']
        for column in contact_dicts:
            new_firstname = column['firstname']
            new_lastname = column['lastname']
            if firstname == new_firstname and lastname == new_lastname:
                if contact['surname'] =='':
                    contact['surname'] =column['surname']
                if contact['organization'] =='':
                    contact['organization'] =column['organization']
                if contact['position'] =='':
                    contact['position'] =column['position']
                if contact['phone'] =='':
                    contact['phone'] =column['phone']
                if contact['email'] =='':
                    contact['email'] =column['email']
    for contact in contact_dicts:
        if contact not in new_contact_dicts:
            new_contact_dicts.append(contact)
    pprint(new_contact_dicts)
    return new_contact_dicts

def writer(dicts):
    keys = list(dicts[0].keys())
    with open("phonebook.csv", "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(keys)
        for d in dicts:
            datawriter.writerow(d.values())

def main():
    fix_phones("phonebook_raw.csv", "fixed_phones.csv")
    final_dicts = uniq_name("fixed_phones.csv")
    writer(final_dicts)
    os.remove("fixed_phones.csv")
if __name__ == '__main__':
    main()