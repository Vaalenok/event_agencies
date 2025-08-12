from bs4 import BeautifulSoup
import json

from models import Company


def find_companies(_json: dict):
    result = []

    vendors = _json.get("vendors", [])

    if vendors:
        for vendor in vendors:
            result.append(
                Company(
                    vendor.get("name", None),
                    None,
                    [],
                    vendor.get("phoneNumber", None),
                    vendor.get("slug", None)
                )
            )

    return result


def get_company_info(html, company: Company):
    soup = BeautifulSoup(html, "html.parser")

    script_tag = soup.find(
        "script", attrs={"type": "application/ld+json", "data-sentry-component": "StructuredData"}
    )

    if script_tag:
        json_text = script_tag.string
        data = json.loads(json_text)
        website_url = data.get("url", None)
        company.website = website_url

    div = soup.find("div", attrs={"data-sentry-component": "SocialLinks"})

    if div:
        links = div.find_all("a")

        if links:
            for link in links:
                company.links.append(link.get("href", None))

    return company
