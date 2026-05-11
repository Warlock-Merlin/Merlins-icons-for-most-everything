import os
import re
import sys
import urllib.parse
import difflib

# Where installed icons live after the installer runs.
INSTALLED_ICON_FOLDER = r"C:\.ico"
# Fallback when running from the repo for testing.
REPO_ICON_FOLDER = os.path.join(os.path.dirname(__file__), "Icons")

SUPPORTED_EXT = ".ico"

ICON_ALIAS_MAP = {
    "facebook": ["fb", "facebookcom"],
    "youtube": ["yt", "youtubecom"],
    "google": ["googlecom"],
    "google news": ["news.google", "newsgooglecom"],
    "Gmail icon": ["mail.google", "mailgooglecom", "gmailcom"],
    "youtube": ["yt", "youtubecom"],
    "asus": ["asuscom", "asusrouter"],
    "twitter": ["x", "twittercom"],
    "telegram": ["t.me", "telegramme"],
    "github": ["githubcom"],
    "reddit": ["redditcom"],
}


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    text = re.sub(r"[^a-z0-9]", "", text)
    return text


def resolve_icon_alias(query):
    normalized_query = normalize_text(query)
    for canonical, aliases in ICON_ALIAS_MAP.items():
        if normalized_query == normalize_text(canonical):
            return normalize_text(canonical)
        for alias in aliases:
            if normalized_query == normalize_text(alias):
                return normalize_text(canonical)
    return normalized_query


def find_icon_folder():
    if os.path.isdir(INSTALLED_ICON_FOLDER):
        return INSTALLED_ICON_FOLDER
    if os.path.isdir(REPO_ICON_FOLDER):
        return REPO_ICON_FOLDER
    return None


def load_icon_candidates(folder):
    icons = []
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.lower().endswith(SUPPORTED_EXT):
                rel_path = os.path.relpath(os.path.join(root, file_name), folder)
                icons.append((rel_path, os.path.join(root, file_name)))
    return icons


def best_icon_match(query, icon_entries):
    normalized_query = resolve_icon_alias(query)
    best = None
    best_score = 0

    for rel, path in icon_entries:
        icon_name = os.path.splitext(rel)[0]
        normalized_icon = normalize_text(icon_name)

        if normalized_query == normalized_icon:
            return rel, path

        score = 0
        if normalized_query in normalized_icon or normalized_icon in normalized_query:
            score = 80
        else:
            score = int(difflib.SequenceMatcher(None, normalized_query, normalized_icon).ratio() * 100)

        if score > best_score:
            best_score = score
            best = (rel, path)

    if best_score >= 60:
        return best
    return None


def safe_shortcut_name(text):
    text = text.strip()
    text = re.sub(r"^https?://", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^www\.", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[^a-zA-Z0-9 ._-]", "", text)
    text = text.strip()
    if not text:
        text = "shortcut"
    return text


def desktop_path():
    if os.name == "nt":
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            return os.path.join(user_profile, "Desktop")
    return os.path.join(os.path.expanduser("~"), "Desktop")


def create_url_shortcut(target_url, icon_path, output_path):
    content = [
        "[InternetShortcut]",
        f"URL={target_url}",
        f"IconFile={icon_path}",
        "IconIndex=0",
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))


def normalize_domain(text):
    text = text.lower().strip()
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    text = text.split("/")[0]
    parts = text.split(".")
    if len(parts) > 2 and parts[0] in {"www", "m", "app", "mobile", "store"}:
        parts = parts[1:]
    if len(parts) >= 2:
        return parts[-2]
    return parts[0]


def parse_website_input(text):
    text = text.strip()
    if not text:
        return None, None

    if re.search(r"\.[a-z0-9]{2,}$", text) or text.startswith("http"):
        url = text
        if not re.match(r"^https?://", url, flags=re.IGNORECASE):
            url = "https://" + url
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname or parsed.path
        site_query = normalize_domain(hostname)
        return url, site_query

    return "https://" + text + ".com", normalize_domain(text)


def main():
    print("Create a desktop shortcut with a matching icon.")
    icon_folder = find_icon_folder()
    if icon_folder is None:
        print("Error: No icon folder found. Please run the installer first or keep the repo Icons folder available.")
        return

    print(f"Using icon folder: {icon_folder}")
    icon_candidates = load_icon_candidates(icon_folder)
    if not icon_candidates:
        print("Error: No .ico files were found in the icon folder.")
        return

    shortcut_name_input = input("Enter the name you want for the shortcut: ").strip()
    if not shortcut_name_input:
        print("Shortcut name is required. Exiting.")
        return

    website_input = input("Enter the website URL or site name: ").strip()
    target_url, query = parse_website_input(website_input)
    if target_url is None:
        print("No website entered. Exiting.")
        return

    match = best_icon_match(query, icon_candidates)
    if match is None:
        print(f"No matching icon found for '{query}'.")
        print("Please add the corresponding .ico to your icon library and generate a new manifest.")
        return

    rel_name, icon_path = match
    desktop = desktop_path()
    if not os.path.isdir(desktop):
        print(f"Desktop folder not found: {desktop}")
        return

    shortcut_name = safe_shortcut_name(shortcut_name_input)
    shortcut_file = os.path.join(desktop, f"{shortcut_name}.url")
    create_url_shortcut(target_url, icon_path, shortcut_file)

    print(f"Shortcut created: {shortcut_file}")
    print(f"Using icon: {rel_name}")


if __name__ == "__main__":
    main()
