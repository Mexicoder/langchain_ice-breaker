import os
import requests
import os
import requests
import json

CACHE_FILE = "linkedin_cache.json"


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrap information from LinkedIn profiles,
    Manually scrap the infromation from LinkedIn profiles.
    """

    # Load cache file if it exists
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    # Check if response is already cached
    if linkedin_profile_url in cache:
        return cache[linkedin_profile_url]

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f"Bearer {os.environ['PROXYCURL_API_KEY']}"}

    response = requests.get(
        api_endpoint, headers=header_dic, params={"url": linkedin_profile_url}
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    # data.pop("certifications")
    
    # if data.get("certifications"):
    #     for group_dict in data.get("certifications"):
    #         group_dict.pop("profile_pic_url")
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    # Cache the response
    cache[linkedin_profile_url] = response.json()

    # Save cache to file
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

    # return response.json()
    return json.dumps(data)
