import re
import pickle
import sys

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last.capitalize() # Capitalize the last name
        self.first = first.capitalize() # Capitalize the first name
        self.mi = mi.upper() if mi else 'X' # Uppercase the middle initial, if it exists. If not, use 'X'
        self.id = Person.verify_id(id) # Use a verified id string
        self.phone = Person.verify_phone(phone) # Use a verified phone number string

    def display(self):
        """
        Prints a formatted string version of the object
        """
        print(f'Employee id: {self.id}\n          {self.first} {self.mi} {self.last}\n          {self.phone}')

    def verify_id(id):
        """
        Given an id string, the function checks its validity. If valid, it return the id.
        If not, the function queries the user for another id and validates it recursively.

        Parameters
        ----------
        id : string
            An unvalidated id string
        
        Returns
        -------
        string
            A guaranteed valid id string. Valid id strings must contain exactly two letters followed by four digits
        """
        if re.search('^[A-Z][A-Z]\d\d\d\d$', id):
            return id
        else:
            print(f'ID invalid: {id}')
            print(f'ID is two letters followed by 4 digits')
            id = input(f'Please enter a valid ID: ')
            return Person.verify_id(id)

    def verify_phone(phone):
        """
        Given a phone number string, the function checks its validity. If valid, it return the phone number string.
        If not, the function queries the user for another phone number string and validates it recursively.

        Parameters
        ----------
        phone : string
            An unvalidated phone number string
        
        Returns
        -------
        string
            A guaranteed valid phone number string. Valid phone number strings must be in the format
            'DDD-DDD-DDDD', where 'D' is any digit 0-9.
        """
        if re.search('^\d\d\d-\d\d\d-\d\d\d\d$', phone):
            return phone
        else:
            print(f'Phone {phone} is invalid')
            print(f'Enter phone number in form 123-456-7890')
            phone = input(f'Enter phone number: ')
            return Person.verify_phone(phone)

def load_data_from_csv(path):
    """
    Load person data from a csv file

    Open a csv file with the given path, iterate over valid lines, 
    instantiate Person objects and return a dictionary of those objects
    where K=person.id, V=person

    Parameters
    ----------
    path : string
        Relative path to the data file to be loaded

    Returns
    -------
    dict
        A dictionary of Person objects where K=person.id, V=person
    """
    people = {}
    with open(path) as file:
        # Read, then skip column line
        line = file.readline()
        
        # Read first data line
        line = file.readline()

        # Iterate over every line
        while line:
            split = line.rstrip().split(',') # Remove trailing '\n' and split by commas
            person = Person(split[0], split[1], split[2], split[3], split[4])
            people[person.id] = person # Add person to people dictionary
            line = file.readline()
    return people

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("No data path specified.")
    
    people = load_data_from_csv(sys.argv[1])

    pickle.dump(people, open('dict.p', 'wb'))
    pickled_people = pickle.load(open('dict.p', 'rb'))

    print("Employee List:\n")
    for person in pickled_people.values():
        person.display()
        print()