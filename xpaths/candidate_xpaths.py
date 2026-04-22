"""Strong XPath locators for candidate add flow."""

from __future__ import annotations

# --- Primary actions (data-testid + visible label) ---
# Set each `data-testid` to match the product. Current Recruiterflow build ships empty
# `data-testid=""` on these buttons; the label keeps the locator unique until real ids land.
CANDIDATE_ADD_BUTTON_TESTID = ""
CANDIDATE_CREATE_BUTTON_TESTID = ""

# --- Add-candidate form fields (index-free locators) ---
FIRST_NAME_INPUT = "//input[@placeholder='e.g. John' and contains(@class,'form-control-input')]"
LAST_NAME_INPUT = "//input[@placeholder='e.g. smith' and contains(@class,'form-control-input')]"
EMAIL_INPUT = "//input[@placeholder='e.g. johnsmith@gmail.com' and contains(@class,'form-control-input')]"

LOCATION_SEARCH_INPUT = "//input[@placeholder='Search location...' and contains(@class,'form-control-input')]"
LOCATION_STREET1_INPUT = "//input[@placeholder='Street address I' and contains(@class,'form-control-input')]"
LOCATION_STREET2_INPUT = "//input[@placeholder='Street address II' and contains(@class,'form-control-input')]"
LOCATION_CITY_INPUT = "//input[@placeholder='City...' and contains(@class,'form-control-input')]"
LOCATION_STATE_INPUT = "//input[@placeholder='State...' and contains(@class,'form-control-input')]"
LOCATION_COUNTRY_INPUT = "//input[@placeholder='Country...' and contains(@class,'form-control-input')]"
LOCATION_ZIP_INPUT = "//input[@placeholder='Zip code...' and contains(@class,'form-control-input')]"

EXPERIENCE_COMPANY_INPUT = "//input[@placeholder='Enter company name' and contains(@class,'form-control-input')]"
EXPERIENCE_TITLE_INPUT = "//input[@placeholder='Enter title' and contains(@class,'form-control-input')]"
EXPERIENCE_FROM_DATE_INPUT = (
    "//div[.//input[@placeholder='To Date (Leave blank if current position)']]"
    "//input[@placeholder='From Date' and contains(@class,'form-control-input')]"
)
EXPERIENCE_TO_DATE_INPUT = (
    "//input[@placeholder='To Date (Leave blank if current position)' and contains(@class,'form-control-input')]"
)

EDUCATION_SCHOOL_INPUT = "//input[@placeholder='Enter school name' and contains(@class,'form-control-input')]"
EDUCATION_DEGREE_INPUT = "//input[@placeholder='Enter degree' and contains(@class,'form-control-input')]"
EDUCATION_SPECIALIZATION_INPUT = "//input[@placeholder='Enter specialization' and contains(@class,'form-control-input')]"
EDUCATION_FROM_DATE_INPUT = (
    "//div[.//input[@placeholder='To Date (Leave blank if current school)']]"
    "//input[@placeholder='From Date' and contains(@class,'form-control-input')]"
)
EDUCATION_TO_DATE_INPUT = (
    "//input[@placeholder='To Date (Leave blank if current school)' and contains(@class,'form-control-input')]"
)

LINKEDIN_INPUT = "//input[@placeholder='Linkedin link' and contains(@class,'form-control-input')]"

# --- Form validation (add page) ---
FORM_FIELD_ERROR_CLASS_ERROR = "//form//*[contains(@class,'error')]"
FORM_FIELD_ERROR_CLASS_INVALID = "//form//*[contains(@class,'invalid')]"
FORM_FIELD_ERROR_CLASS_DANGER = "//form//*[contains(@class,'danger')]"

FORM_FIELD_ERROR_XPATHS: tuple[str, ...] = (
    FORM_FIELD_ERROR_CLASS_ERROR,
    FORM_FIELD_ERROR_CLASS_INVALID,
    FORM_FIELD_ERROR_CLASS_DANGER,
)

# --- Post-submit error copy ---
# Keep this strict: only ARIA alert regions, excluding header settings wrapper.
ERROR_MESSAGE_ALERT = "//*[@role='alert' and not(contains(@class,'alert-settings'))]"


def quote_xpath_literal(value: str) -> str:
    """Quote a string for use inside XPath literals (handles embedded quotes)."""
    if "'" not in value:
        return f"'{value}'"

    parts = value.split("'")
    chunks: list[str] = []
    for index, part in enumerate(parts):
        chunks.append(f"'{part}'")
        if index != len(parts) - 1:
            chunks.append("\"'\"")
    return "concat(" + ", ".join(chunks) + ")"


def xpath_button_by_testid(testid: str) -> str:
    return f"//button[@data-testid={quote_xpath_literal(testid)}]"


def xpath_candidate_action_button(testid: str, button_text: str) -> str:
    """Locate toolbar / form primary buttons by data-testid and exact visible text."""
    return (
        "//button["
        f"@data-testid={quote_xpath_literal(testid)} and text()={quote_xpath_literal(button_text)}"
        "]"
    )


ADD_CANDIDATE_BUTTON_XPATH = xpath_candidate_action_button(CANDIDATE_ADD_BUTTON_TESTID, "+ Candidate")
CREATE_CANDIDATE_BUTTON_XPATH = xpath_candidate_action_button(CANDIDATE_CREATE_BUTTON_TESTID, "Create candidate")
