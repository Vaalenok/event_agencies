from models import Company


def get_companies(json: dict):
    result = []

    vendors = json.get("vendors", [])

    if vendors:
        for vendor in vendors:
            result.append(
                Company(
                    vendor.get("name", None),
                    None,
                    None,
                    vendor.get("phoneNumber", None),
                    vendor.get("slug", None)
                )
            )

    return result


def get_company_info():
    pass
