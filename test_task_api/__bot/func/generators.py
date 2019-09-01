import random

"""
No comments... Just simple ...
"""


class Randomizer():
    def __init__(self):
        self.domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def get_one_random_domain(self, domains):
        return domains[random.randint(0, len(self.domains) - 1)]

    def get_one_random_name(self, letters):
        name = ""
        for i in range(7):
            name = name + letters[random.randint(0, len(self.letters) - 1)]
        return name

    def generate_record(self):
        first_name = str(self.get_one_random_name(self.letters))
        last_name = str(self.get_one_random_name(self.letters))
        one_domain = str(self.get_one_random_domain(self.domains))
        password = str(self.get_one_random_name(self.letters))

        return {"email": ("%s_%s@%s" % (first_name, last_name, one_domain)),
                "first_name": first_name,
                "last_name": last_name,
                "password": password}

    def generate_title(self):
        title = ""
        for i in range(15):
            title += self.letters[random.randint(0, len(self.letters) - 1)]
        return title.upper()

    def generate_text(self):
        text = ""
        for i in range(100):
            text += self.letters[random.randint(0, len(self.letters) - 1)]
        return text.capitalize()
