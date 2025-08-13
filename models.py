class Person:
    def __init__(self, name, job_title, phone_number, email):
        self.name = name
        self.job_title = job_title
        self.phone_number = phone_number
        self.email = email


class Company:
    def __init__(self, name, website, ig_link, fb_link, phone_number, persons, slug):
        self.name = name
        self.website = website
        self.ig_link = ig_link
        self.fb_link = fb_link
        self.phone_number = phone_number
        self.persons = persons

        self.slug = slug
