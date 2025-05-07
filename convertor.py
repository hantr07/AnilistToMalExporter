import sys
import requests
import xml.etree.ElementTree as ET

ANILIST_BASE = "https://graphql.anilist.co/"

# Status mappings for anime and manga
status_mappings_anime = {
    "CURRENT": "Watching",
    "PLANNING": "Plan to Watch",
    "DROPPED": "Dropped",
    "COMPLETED": "Completed",
    "PAUSED": "On-Hold"
}

status_mappings_manga = {
    "CURRENT": "Reading",
    "PLANNING": "Plan to Read",
    "DROPPED": "Dropped",
    "COMPLETED": "Completed",
    "PAUSED": "On-Hold"
}

# GraphQL query for anime and manga
media_list_fetch = """
query($username: String, $type: MediaType) {
  MediaListCollection(userName: $username, type: $type, sort: STATUS) {
    lists {
      entries {
        progress
        status
        score
        startedAt {
          year
          month
          day
        }
        completedAt {
          year
          month
          day
        }
        media {
          id
          idMal
          title {
            english
            romaji
          }
        }
      }
    }
  }
}
"""

def fetch_media_list(anilist_username: str, media_type: str) -> dict:
    """Fetch anime or manga list from AniList."""
    response = requests.post(
        url=ANILIST_BASE,
        json={
            "query": media_list_fetch,
            "variables": {
                "username": anilist_username,
                "type": media_type
            }
        }
    )
    response.raise_for_status()
    return response.json().get("data", {}).get("MediaListCollection", {}).get("lists", [])

def create_xml(anilist_username: str, media_list: list, media_type: str) -> None:
    """Create MAL-compatible XML for anime or manga."""
    root = ET.Element("myanimelist")

    # Boilerplate XML
    my_info = ET.SubElement(root, "myinfo")
    user_export_type = ET.SubElement(my_info, "user_export_type")
    user_export_type.text = "1" if media_type == "ANIME" else "2"  # 1 for anime, 2 for manga

    # Select appropriate status mappings
    status_mappings = status_mappings_anime if media_type == "ANIME" else status_mappings_manga

    for media_list_item in media_list:
        entries = media_list_item.get("entries", [])
        for entry in entries:
            mal_id = entry.get("media", {}).get("idMal")
            title = entry.get("media", {}).get("title", {}).get("english") or entry.get("media", {}).get("title", {}).get("romaji")
            status = status_mappings.get(entry.get("status"))
            score = entry.get("score")
            progress = entry.get("progress")
            start_date = "{y:04d}-{m:02d}-{d:02d}".format(
                y=entry.get("startedAt", {}).get("year") or 0,
                m=entry.get("startedAt", {}).get("month") or 1,
                d=entry.get("startedAt", {}).get("day") or 1
            ) if entry.get("startedAt", {}).get("year") else "0000-00-00"
            end_date = "{y:04d}-{m:02d}-{d:02d}".format(
                y=entry.get("completedAt", {}).get("year") or 0,
                m=entry.get("completedAt", {}).get("month") or 1,
                d=entry.get("completedAt", {}).get("day") or 1
            ) if entry.get("completedAt", {}).get("year") else "0000-00-00"

            if not mal_id or title in (None, "None"):
                continue  # Skip entries without MAL ID or valid title

            # Create anime or manga container
            container = ET.SubElement(root, "anime" if media_type == "ANIME" else "manga")

            # Add fields based on media type
            ET.SubElement(container, "series_animedb_id" if media_type == "ANIME" else "manga_mangadb_id").text = str(mal_id)
            ET.SubElement(container, "my_watched_episodes" if media_type == "ANIME" else "my_read_chapters").text = str(progress)
            ET.SubElement(container, "my_score").text = str(score) if score else "0"
            if status not in ("Plan to Watch", "Plan to Read"):
                ET.SubElement(container, "my_start_date").text = start_date
            if status == "Completed":
                ET.SubElement(container, "my_finish_date").text = end_date
            ET.SubElement(container, "my_status").text = status
            ET.SubElement(container, "update_on_import").text = "1"

            print(f"ADDED [{media_type}]: {status} > {title}")

    # Write to XML file
    output_file = f"{anilist_username}_MAL_{'anime' if media_type == 'ANIME' else 'manga'}.xml"
    with open(output_file, "wb") as xml_file:
        tree = ET.ElementTree(root)
        tree.write(xml_file)
    print(f"Saved {media_type} list to {output_file}")

def convert(anilist_username: str) -> None:
    """Convert AniList anime and manga lists to MAL XML."""
    # Fetch and process anime
    anime_list = fetch_media_list(anilist_username, "ANIME")
    if anime_list:
        create_xml(anilist_username, anime_list, "ANIME")
    else:
        print("No anime list found or failed to fetch anime data.")

    # Fetch and process manga
    manga_list = fetch_media_list(anilist_username, "MANGA")
    if manga_list:
        create_xml(anilist_username, manga_list, "MANGA")
    else:
        print("No manga list found or failed to fetch manga data.")

def main():
    if len(sys.argv) < 2:
        print("Please provide a valid AniList username")
        anilist_username = input().strip()
    else:
        anilist_username = sys.argv[1].strip()

    convert(anilist_username)

if __name__ == "__main__":
    main()
