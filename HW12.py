from collections import UserDict
from datetime import datetime, timedelta
import pickle
class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def __next__(self):
        number=int(input("Enter how many contacts you want to see\n"))
        text_phones = ''
        if number>len(self.data.items()):
            return print(f"There are only {len(self.data.items())} contacts in your contact list. Please try again")
        for index, (name, record) in enumerate(self.data.items()):
            if index+1==number:
                text_phones += name + ' ' + ', '.join([phone.value for phone in record.phones]) + '\n'
                return text_phones
            text_phones += name + ' ' + ', '.join([phone.value for phone in record.phones]) + '\n'
    def save(self):
        with open('contact_book.txt', 'wb') as fh:
            pickle.dump(self.data, fh)

    def load(self):
        try:
            with open('contact_book.txt', 'rb') as fh:
                contacts = pickle.load(fh)
                return contacts
        except FileNotFoundError:
            return None
class CustomIterator:
    def __iter__(self):
        return contacts_dictionary

class Record():
    def __init__(self, name, phone = None, birthday=None):
        self.name = Name(name)
        self.birthday = None
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []
        
    def add_phone(self, phone):
        new_phone=Phone.valid_phone(phone)
        self.phones.append(Phone(new_phone))
    
    def delete_phone(self, phone):
        some_list=[phone.value for phone in self.phones]
        if phone in some_list:
            self.phones.pop(some_list.index(phone))

    def change_phone(self, old_phone, new_phone):
        some_list=[phone.value for phone in self.phones]
        self.phones[some_list.index(old_phone)] = Phone(new_phone)
    def add_birthday(self, birthday):
        if not Birthday.valid_birthday(birthday):
            print('Not valid birthday, enter "addbirthday" "first name" "second name" "year.month.day"')
            return
        borndate = Birthday(birthday)
        borndate.value = birthday
        self.birthday = borndate
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            if self.birthday.value.replace(year=today.year) >= today:
                result = self.birthday.value.replace(
                    year=today.year) - today
            else:
                result = self.birthday.value.replace(
                    year=today.year) - today.replace(year=today.year - 1)
            print(result.days)
        else:
            print('No birthday found')

class Field():
    def __init__(self, value):
        self._value = value
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    def __init__(self, name):
        self.value = name

class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        self._value = phone

    @classmethod
    def valid_phone(cls, value):
        return sanitize_phone_number(value)

    def __repr__(self):
        return self._value

class Birthday(Field):
    @Field.value.setter
    def value(self, birthday):
        self._value = datetime.strptime(birthday, '%Y.%m.%d').date()

    @classmethod
    def valid_birthday(cls, value):
        return 0 < int(value.split('.')[0]) <= datetime.now().date().year and 0 < int(value.split('.')[1]) <= 12 and 0 < int(value.split('.')[2]) <= 31

    def __repr__(self):
        return self._value

contacts_dictionary = AdressBook()

def format_phone_number(func):
    def inner(x):
        result = func(x)
        if len(result)<10:
            return sanitize_phone_number(input("Looks like you type wrong number.Please try again.Type only number\n"))
        elif len(result)<12:
            new_result="+38"+result
            return new_result
        elif len(result)<13:
            new_result="+"+result
            return new_result
        elif len(result)>=13:
            return sanitize_phone_number(input("Looks like you type wrong number.Please try again.Type only number\n"))
        else:
            return result      
    return inner

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

def format_name(list):
    if isinstance(list,str):
        list=list.strip().split()
    new_name=[]
    for i in list:
        if i.isalpha():
            name=i.lower().capitalize()
            new_name.append(name)
        else:
            return format_name(input("Looks like you type wrong name.Please try again.Type only first and second name\n"))
    return " ".join(new_name) 
            

def parser_command(string):
    modified_list1=string.strip().split()
    return modified_list1

def name_search(some_list):
    name_list=list(contacts_dictionary.data.keys())
    if isinstance(some_list,str):
        some_list=some_list.strip().split()
    result=[]
    if len(some_list)==1:
        if some_list[0].lower()=="cancel":
            return
        for i in name_list:
            if some_list[0].lower().capitalize() in i:
                result.append(i)
            else:
                pass
    elif len(some_list)==2:
        new_name=" ".join([some_list[0].lower().capitalize(),some_list[1].lower().capitalize()])
        another_name =" ".join([some_list[1].lower().capitalize(),some_list[0].lower().capitalize()])
        if new_name in name_list:
            record = contacts_dictionary.data[new_name]
            return ', '.join([phone.value for phone in record.phones])
        elif another_name in name_list:
            record = contacts_dictionary.data[another_name]
            return ', '.join([phone.value for phone in record.phones])
        for i in name_list:
            if some_list[0].lower().capitalize() in i:
                result.append(f"{i}")
            elif some_list[1].lower().capitalize() in i:
                result.append(f"{i}") 
            else:
                pass
    if len(result)>=1:
        return name_search(input(f'{result} These are the best match what I found for you. Type one of this names to see number you need\n'))
    else:
        return name_search(input('No results were found with such name.Try another name or type "cancel"\n'))
def hello():
    return handler(input("Hello.How can I help you?:\n"))
def phone_number(list):
    if isinstance(list,str):
        phone_number(["phone"]+parser_command(list))
    elif len(list)<2 or len(list)>4:
        return phone_number(input('Function "change" accept only 2 parameters.Please type first name and second name.\n'))
    elif len(list) in [2,3]:
        list2=list[1:]
        phone_number=name_search(list2)
        if phone_number==None:
            print("Let's try something else")
        else:
            print(f'Contact has such number(s):{phone_number}')
def change(list):
    if isinstance(list,str):
        change(["change"]+parser_command(list))
    elif len(list)==4:
        list2=list[1:3]
        clean_name=format_name(list2)
        clean_name2=format_name(" ".join([list2[1],list2[0]]))
        if clean_name in contacts_dictionary.data.keys():
            old_phone=contacts_dictionary.data[clean_name]
            if len(old_phone.phones)>=2:
                old_telephone=input(f"There are few phones for {clean_name}.{[phone.value for phone in old_phone.phones]}.Type one you want to change.")
                old_phone.change_phone(sanitize_phone_number(old_telephone), sanitize_phone_number(list[-1]))
                print(f'Contact dictionary successfully updated. {old_telephone} replaced with {sanitize_phone_number(list[-1])}')
            else:
                old_phone.change_phone(old_phone.phones[0].value, sanitize_phone_number(list[-1]))
                print(f'Contact dictionary successfully updated. Old phone replaced with {sanitize_phone_number(list[-1])}')
        elif clean_name2 in contacts_dictionary.data.keys():
            old_phone=contacts_dictionary.data[clean_name2]
            if len(old_phone.phones)>=2:
                old_telephone=input(f"There are few phones for {clean_name2}.{[phone.value for phone in old_phone.phones]}.Type one you want to change.")
                old_phone.change_phone(sanitize_phone_number(old_telephone), sanitize_phone_number(list[-1]))
                print(f'Contact dictionary successfully updated. {old_telephone} replaced with {sanitize_phone_number(list[-1])}')
            else:
                old_phone.change_phone(old_phone.phones[0].value, sanitize_phone_number(list[-1]))
                print(f'Contact dictionary successfully updated. Old phone replaced with {sanitize_phone_number(list[-1])}')
        else:
            return print('There are no match for your input. Type "show all" to see all contacts\n')
    else:
        return change(input('Function "change" accept only such sequence: first name,second name and phone number.Please try again\n'))

def show_all():
    some = CustomIterator()
    try:
        for _ in some:
            if _ == None:
                raise StopIteration
            else:
                print(_)
                raise StopIteration
    except StopIteration:
        pass
def add_delete(string,list):
    if isinstance(list,str):
        add_delete(string,parser_command(list))
    elif len(list)==4:
        list2=[]
        list2.extend(list[1:-1])
        clean_name=format_name(list2)
        clean_name2=format_name(" ".join([list2[1],list2[0]]))
        if clean_name in contacts_dictionary:
            record = contacts_dictionary.data[clean_name]
            if string=="add":
                record.add_phone(list[-1])
            else:
                record.delete_phone(sanitize_phone_number(list[-1]))
        elif clean_name2 in contacts_dictionary:
            record = contacts_dictionary.data[clean_name2]
            if string=="add":
                record.add_phone(list[-1])
            else:
                record.delete_phone(sanitize_phone_number(list[-1]))
        else:
            if string=="add":
                record = Record(clean_name)
                contacts_dictionary.add_record(record)
                update = contacts_dictionary.data[clean_name]
                update.add_phone(list[-1])
            else:
                add_delete(input('Something wrong.Please type "delete" first name,second name and phone number:\n'))
        if string=="add":
            print(f'Contact dictionary successfully updated with such contact {clean_name}')
        if string=="delete":
            print(f'Contact dictionary successfully updated.From contact {clean_name} removed such number {sanitize_phone_number(list[-1])}')
    else:
        return add_delete(string,input(f'Something wrong.Please type first name,second name and phone number:\n'))

def set_birthday(list):
    if len(list) != 4:
        return print('Function "addbirthday" accept only such sequence:"addbirthday", first name,second name and date.Please try again')
    list2=list[1:3]
    clean_name=format_name(list2)
    clean_name2=format_name(" ".join([list2[1],list2[0]]))
    if clean_name in contacts_dictionary.data:
        try:
            setting = contacts_dictionary.data[clean_name]
            setting.add_birthday(list[3])
            if setting.birthday:
                print(f'Birthday for contact {clean_name} added')
        except IndexError:
            return print('Function "addbirthday" accept only such sequence:"addbirthday", first name,second name and date.Please try again')
    elif clean_name2 in contacts_dictionary.data:
        try:
            setting = contacts_dictionary.data[clean_name2]
            setting.add_birthday(list[3])
            print(f'Birthday for contact {clean_name2} added as {list[3]}')
        except IndexError:
            return print('Function "addbirthday" accept only such sequence:"addbirthday", first name,second name and date.Please try again')
    else:
        return print("There are no such conctact exist to apply birth date")
def show_birthday(list):
    if len(list) != 3:
        return show_birthday(input('Function "daystobirthday" accept only such sequence:"daystobirthday", first name,second name.Please try again'))
    list2=list[1:3]
    clean_name=format_name(list2)
    clean_name2=format_name(" ".join([list2[1],list2[0]]))
    if clean_name in contacts_dictionary.data:
        birthding = contacts_dictionary.data[clean_name]
        birthding.days_to_birthday()
    elif clean_name2 in contacts_dictionary.data:
        birthding = contacts_dictionary.data[clean_name2]
        birthding.days_to_birthday()
    else:
        return print("There are no such conctact exist")
def handler(string):
    exit_list=['good bye','close','exit']
    while string.lower() not in exit_list:
        parsed=parser_command(string)
        if len(parsed)==1 and parsed[0].lower()=="hello":
            return hello()
        elif len(parsed)>1:
            if parsed[0].lower()=="add":
                add_delete("add",parsed)
                return handler(input("Would you like to do something else?\n"))
            elif parsed[0].lower()=="phone":
                phone_number(parsed)
                return handler(input("Would you like to do something else?\n"))
            elif parsed[0].lower()=="delete":
                add_delete("delete",parsed)
                return handler(input("Would you like to do something else?\n"))
            elif parsed[0].lower()=="change":
                change(parsed)
                return handler(input("Would you like to do something else?\n"))
            elif string.lower() =="show all":
                show_all()
                return handler(input("Would you like to do something else?\n"))
            elif parsed[0] =="addbirthday":
                set_birthday(parsed)
                return handler(input("Would you like to do something else?\n"))
            elif parsed[0] =="daystobirthday":
                show_birthday(parsed)
                return handler(input("Would you like to do something else?\n"))
            else:
                return handler(input("Looks like you type something wrong.Please try again,don't forget space between words\n"))
        else:
                return handler(input("Looks like you type something wrong.Please try again,don't forget space between words\n"))

def main():
    print('Hello. I am bot which works with your phone book.')
    print('[1] Enter "hello" and receive answer "How can I help you?"')
    print('[2] Enter "add ...". With this command I will save in memory new contact(Only Ukraininan Numbers).')
    print('[3] Enter "change ...". With this command I will change number in existing contact.Excepting first or second name')
    print('[4] Enter "phone ....". With this command I will show number of contact that you enter.')
    print('[5] Enter "show all". With this command I will show all numbers existing in your contact list.')
    print('[6] Enter "delete ...". With this command I delete requested number from existed contact if any.')
    print('[7] Enter "addbirthday ...". With this command I will add/change birtday for requested contact.')
    print('[8] Enter "daystobirthday ...". With this command I will show all birtdays of contact list or requested contact.')
    print('[9] Enter "good bye","close" or "exit" to quit.')
    load_contacts = contacts_dictionary.load()
    if load_contacts:
        for key, value in load_contacts.items():
            contacts_dictionary.data[key] = value
    user_input_value = input('How can I help you today?:\n')
    handler(user_input_value)
    contacts_dictionary.save()
    print("Good bye!")
if __name__ == '__main__':
    main()