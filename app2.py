import streamlit as st
from rapidfuzz import process, fuzz

# Map of known abbreviations to their full names
known_abbreviations = {
    "usa": "United States of America",
    "uk": "United Kingdom",
    "uae": "United Arab Emirates",
    "prc": "People's Republic of China",
    "russia": "Russian Federation",  # Common name, full name is "Russian Federation"
    "sa": "Saudi Arabia",
    "rsa": "Republic of South Africa",
    "drc": "Democratic Republic of the Congo",
    "roc": "Republic of China",  # Refers to Taiwan
    "south korea": "Republic of Korea",
    "north korea": "Democratic People's Republic of Korea",
    "vn": "Vietnam",
    "ven": "Venezuela",
    "bol": "Bolivia",
    "ir": "Iran",
    "jp": "Japan",
    "de": "Germany",
    "fr": "France",
    "es": "Spain",
    "it": "Italy",
    "br": "Brazil",
    "ca": "Canada",
    "mx": "Mexico",
    "in": "India",
    "aus": "Australia",
    "nz": "New Zealand",
    "arg": "Argentina",
    "sg": "Singapore",
    "my": "Malaysia",
    "id": "Indonesia",
    "ph": "Philippines",
    "th": "Thailand",
    "lk": "Sri Lanka",
    "pk": "Pakistan",
    "bd": "Bangladesh",
    "np": "Nepal",
    "mm": "Myanmar",
    "kh": "Cambodia",
    "la": "Laos",
    "vn": "Vietnam",
    "kr": "South Korea",
    "kp": "North Korea",
    "eg": "Egypt",
    "ng": "Nigeria",
    "ke": "Kenya",
    "tz": "Tanzania",
    "ug": "Uganda",
    "dz": "Algeria",
    "ma": "Morocco",
    "gh": "Ghana",
    "ci": "Côte d'Ivoire",
    "nl": "Netherlands",
    "be": "Belgium",
    "pt": "Portugal",
    "no": "Norway",
    "se": "Sweden",
    "fi": "Finland",
    "dk": "Denmark",
    "gr": "Greece",
    "pl": "Poland",
    "hu": "Hungary",
    "cz": "Czech Republic",
    "sk": "Slovakia",
    "at": "Austria",
    "ch": "Switzerland",
    "ie": "Ireland",
    "lu": "Luxembourg",
    "cy": "Cyprus",
    "mt": "Malta",
    "is": "Iceland",
    "li": "Liechtenstein",
    "mc": "Monaco",
    "sm": "San Marino",
    "va": "Vatican City",
    "by": "Belarus",
    "md": "Moldova",
    "ua": "Ukraine",
    "am": "Armenia",
    "ge": "Georgia",
    "az": "Azerbaijan",
    "kz": "Kazakhstan",
    "uz": "Uzbekistan",
    "tm": "Turkmenistan",
    "kg": "Kyrgyzstan",
    "tj": "Tajikistan",
    # Add more as needed
}


def adjust_score_for_short_queries(query, items, score_threshold):
    # Adjust score for short queries
    if len(query) <= 3:
        score_threshold = max(30, score_threshold - 20)  # More lenient for short queries
    return score_threshold

def post_match_filtering(query, match, score):
    # Filter out irrelevant matches for short queries
    if len(query) <= 3 and not match.lower().startswith(query):
        return None, 0  # Discard irrelevant matches
    return match, score

def main():
    st.title("Enhanced Matching App")

    user_list = st.text_area("Enter your list items separated by commas or new lines:")
    user_query = st.text_input("Enter your query to find the closest match:")

    items = [item.strip().lower() for item in user_list.replace(',', '\n').split('\n') if item.strip()]

    if user_query and items:
        user_query_lower = user_query.lower()

        # Initial fuzzy matching
        closest_match, score, _ = process.extractOne(user_query_lower, items, scorer=fuzz.WRatio)

        # Adjust score threshold for short queries
        score_threshold = adjust_score_for_short_queries(user_query_lower, items, 60)

        if closest_match and score > score_threshold:
            # Post-match filtering for relevance
            filtered_match, filtered_score = post_match_filtering(user_query_lower, closest_match, score)
            if filtered_match:
                st.success(f"]{filtered_match}")
            else:
                st.error("No relevant match found. Please try a different query.")
        else:
            st.error("No close match found.")

if __name__ == "__main__":
    main()