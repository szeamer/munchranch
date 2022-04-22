import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.name)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def name(self):
        return self.name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password_hash(self, hash):
        self.password_hash = hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class Cat:
    def __init__(self, name, birthdate, color, sex, description, picture, forsale, breeding, sold):
        self.name = name
        self.birthdate = birthdate
        self.color = color
        self.sex = sex
        self.description = description
        self.picture = picture
        self.forsale = forsale
        self.breeding = breeding
        self.birthdate = birthdate
        self.sold = sold
    
    def __repr__(self):
        return self.name + " " + self.description