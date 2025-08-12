class Company:
    def __init__(self, name, website, ig_link, fb_link, phone_number, slug):
        self.name = name
        self.website = website
        self.ig_link = ig_link
        self.fb_link = fb_link
        self.phone_number = phone_number

        self.slug = slug


class Person:
    def __init__(self, name, job_title, phone_number, email, ig_link, fb_link):
        self.name = name
        self.job_title = job_title
        self.phone_number = phone_number
        self.email = email
        self.ig_link = ig_link
        self.fb_link = fb_link
