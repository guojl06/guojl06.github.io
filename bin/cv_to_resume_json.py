#!/usr/bin/env python3
"""Convert _data/cv.yml (RenderCV format) → assets/json/resume.json (JSON Resume format).

This keeps the web-page CV in sync with the PDF source so you only edit one file.
Usage:
    python bin/cv_to_resume_json.py [_data/cv.yml] [assets/json/resume.json]
"""
import json
import sys

import yaml


def convert_date(d):
    """RenderCV dates may be int (1900) or str (2014-04-01); normalize to string."""
    if d is None or d == "":
        return ""
    if isinstance(d, int):
        return f"{d}-01-01"
    return str(d)


# --- per-section converters: RenderCV item dict → JSON Resume item dict ---

def convert_education(items):
    return [
        {
            "institution": it.get("institution", ""),
            "location": it.get("location", ""),
            "url": it.get("url", ""),
            "area": it.get("area", ""),
            "studyType": it.get("degree", it.get("studyType", "")),
            "startDate": convert_date(it.get("start_date")),
            "endDate": convert_date(it.get("end_date")),
            "score": it.get("score", ""),
            "courses": it.get("courses", ""),
            "highlights": it.get("highlights", []),
        }
        for it in items
    ]


def convert_work(items):
    return [
        {
            "name": it.get("company", it.get("name", "")),
            "position": it.get("position", ""),
            "url": it.get("url", ""),
            "location": it.get("location", ""),
            "startDate": convert_date(it.get("start_date")),
            "endDate": convert_date(it.get("end_date")),
            "summary": it.get("summary", ""),
            "highlights": it.get("highlights", []),
        }
        for it in items
    ]


def convert_volunteer(items):
    return [
        {
            "organization": it.get("company", it.get("organization", "")),
            "position": it.get("position", ""),
            "url": it.get("url", ""),
            "location": it.get("location", ""),
            "startDate": convert_date(it.get("start_date")),
            "endDate": convert_date(it.get("end_date")),
            "summary": it.get("summary", ""),
            "highlights": it.get("highlights", []),
        }
        for it in items
    ]


def convert_awards(items):
    return [
        {
            "title": it.get("title", ""),
            "date": convert_date(it.get("date")),
            "awarder": it.get("awarder", ""),
            "summary": it.get("summary", ""),
            "url": it.get("url", ""),
        }
        for it in items
    ]


def convert_publications(items):
    return [
        {
            "name": it.get("title", ""),
            "publisher": it.get("publisher", ""),
            "releaseDate": convert_date(it.get("releaseDate", it.get("release_date"))),
            "url": it.get("url", ""),
            "summary": it.get("summary", ""),
        }
        for it in items
    ]


def convert_skills(items):
    return [
        {
            "name": it.get("name", ""),
            "level": it.get("level", ""),
            "icon": it.get("icon", ""),
            "keywords": it.get("keywords", ""),
        }
        for it in items
    ]


def convert_languages(items):
    return [
        {
            "name": it.get("name", ""),
            "fluency": it.get("summary", ""),
        }
        for it in items
    ]


def convert_interests(items):
    return [
        {
            "name": it.get("name", ""),
            "icon": it.get("icon", ""),
            "keywords": it.get("keywords", ""),
        }
        for it in items
    ]


def convert_certificates(items):
    return [
        {
            "name": it.get("name", ""),
            "date": convert_date(it.get("date")),
            "issuer": it.get("issuer", ""),
            "icon": it.get("icon", ""),
            "url": it.get("url", ""),
        }
        for it in items
    ]


def convert_projects(items):
    return [
        {
            "name": it.get("name", ""),
            "startDate": convert_date(it.get("start_date")),
            "endDate": convert_date(it.get("end_date")),
            "description": it.get("summary", ""),
            "highlights": it.get("highlights", []),
            "url": it.get("url", ""),
        }
        for it in items
    ]


def convert_references(items):
    return [
        {
            "name": it.get("name", ""),
            "icon": it.get("icon", ""),
            "reference": it.get("reference", ""),
        }
        for it in items
    ]


# Map RenderCV section names (lowercased) → (JSON Resume key, converter)
SECTION_MAP = {
    "education": ("education", convert_education),
    "experience": ("work", convert_work),
    "work": ("work", convert_work),
    "volunteer": ("volunteer", convert_volunteer),
    "awards": ("awards", convert_awards),
    "publications": ("publications", convert_publications),
    "skills": ("skills", convert_skills),
    "languages": ("languages", convert_languages),
    "interests": ("interests", convert_interests),
    "certificates": ("certificates", convert_certificates),
    "projects": ("projects", convert_projects),
    "references": ("references", convert_references),
}


def convert(cv_data):
    cv = cv_data.get("cv", cv_data)

    basics = {
        "name": cv.get("name", ""),
        "label": cv.get("headline", cv.get("label", "")),
        "image": cv.get("photo", cv.get("image", "")),
        "email": cv.get("email", ""),
        "phone": cv.get("phone", ""),
        "url": cv.get("website", cv.get("url", "")),
        "summary": cv.get("summary", ""),
    }

    # Location
    addr = cv.get("address", {})
    loc = cv.get("location", "")
    if isinstance(loc, str) and loc:
        basics["location"] = {"address": loc}
    elif addr:
        basics["location"] = {
            "address": addr.get("street", ""),
            "postalCode": addr.get("postalCode", ""),
            "city": addr.get("city", ""),
            "countryCode": addr.get("countryCode", ""),
            "region": addr.get("region", ""),
        }
    else:
        basics["location"] = {}

    # Social networks → profiles
    url_for = {
        "GitHub": "https://github.com/{}",
        "LinkedIn": "https://linkedin.com/in/{}",
        "X": "https://x.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://instagram.com/{}",
        "YouTube": "https://youtube.com/@{}",
    }
    profiles = []
    for sn in cv.get("social_networks", []):
        net = sn.get("network", "")
        user = sn.get("username", "")
        url = sn.get("url", "") or url_for.get(net, "").format(user) if user else ""
        profiles.append({"network": net, "username": user, "url": url})
    basics["profiles"] = profiles

    resume = {"basics": basics}
    for section_name, items in cv.get("sections", {}).items():
        key = section_name.lower().strip()
        if key in SECTION_MAP:
            json_key, fn = SECTION_MAP[key]
            resume[json_key] = fn(items)

    return resume


def main():
    cv_path = sys.argv[1] if len(sys.argv) > 1 else "_data/cv.yml"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "assets/json/resume.json"

    with open(cv_path, "r", encoding="utf-8") as f:
        cv_data = yaml.safe_load(f)

    resume = convert(cv_data)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=2, ensure_ascii=False)

    print(f"✓ {cv_path} → {out_path}")


if __name__ == "__main__":
    main()
