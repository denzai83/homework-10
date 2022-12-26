from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Name(Field):
    pass


class Phone(Field):
    def __eq__(self, __o) -> bool:
        if self.value == __o.value:
            return True
        return False


class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        return f'Sorry, phone must be a Phone instance'

    def delete_phone(self, phone: Phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones[self.phones.index(old_phone)] = new_phone


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


contacts = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return 'Wrong command! Please, try again!'
        except ValueError:
            return 'Wrong command! Please, try again!'
        except IndexError:
            return 'Wrong command! Please, try again!'
    return wrapper


@input_error
def add_contact(message):
    name, phone = message.lower().split()
    name = Name(name.title())
    phone = Phone(phone)
    if name.value in contacts:
        if phone in contacts[name.value].phones:
            return f'{phone.value} already exists in contact {name.value}'
        else:
            contacts[name.value].add_phone(phone)
            return f'{phone.value} successfully added to contact {name.value}'
    else:
        contact = Record(name)
        contacts.add_record(contact)
        contacts[name.value].add_phone(phone)
        return f'Contact {name.value} has been added'


@input_error
def change_number(message):
    name, old_phone, new_phone = message.lower().split()
    name = Name(name.title())
    old_phone = Phone(old_phone)
    new_phone = Phone(new_phone)
    if name.value in contacts:
        contacts[name.value].edit_phone(old_phone, new_phone)
        return f'{old_phone.value} has been changed on {new_phone.value} for contact {name.value}'
    else:
        return f'Contact {name.value} does not exist'


@input_error
def delete_number(message):
    name, phone = message.lower().split()
    name = Name(name.title())
    phone = Phone(phone)
    if name.value in contacts:
        contacts[name.value].delete_phone(phone)
        return f'{phone.value} has been deleted from contact {name.value}'
    else:
        return f'Contact {name.value} does not exist'


def goodbye():
    return print('Good bye!')


@input_error
def greeting(message):
    return 'How can I help you?'


@input_error
def show_all(message):
    item = ''
    for contact in contacts.values():
        item += f'{contact.name}: {contact.phones}\n'
    return item.rstrip('\n')


@input_error
def show_phone(message):
    name = message.lower()
    name = Name(name.title())
    if name.value in contacts:
        contact = contacts[name.value]
        return f'{contact.name}: {contact.phones}'
    else:
        return f'Contact {name.value} does not exist'


commands = {
    'add': add_contact,
    'change': change_number,
    'delete': delete_number,
    'hello': greeting,
    'phone': show_phone,
    'show all': show_all
}


@input_error
def main():
    while True:
        command = input('>>>: ')

        if command.lower() in ('.', 'close', 'exit', 'good bye'):
            goodbye()
            break

        for key in commands:
            if command.lower().strip().startswith(key):
                print(commands[key](command[len(key):].strip()))


if __name__ == '__main__':
    main()
