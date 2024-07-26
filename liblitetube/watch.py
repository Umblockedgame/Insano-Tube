import json
import datetime
import yt_dlp
import timeago
from yt_dlp.utils import DownloadError


def GetTracks(video):
    """
    Function to get tracks from a YouTube video
    """
    # Initialize empty dictionaries and lists
    data = {}
    streams = {}
    itags = []

    try:
        # Set up YouTube downloader with quiet mode enabled and geo bypass
        ydl_opts = {
            'quiet': True,
            'geo_bypass': True,
            'format': 'best',
            'noplaylist': True,
            'no_warnings': True
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Extract information about the video using the downloader
        info = json.loads(json.dumps(ydl.sanitize_info(ydl.extract_info(
            'https://youtube.com/watch?v=' + video, download=False))))
        allstreams = info["formats"]

        # Extract relevant information from the video information
        data["channel_id"] = info.get("channel_id", "N/A")
        data["title"] = info.get("fulltitle", "N/A")
        data["view_count"] = info.get("view_count", 0)
        data["uploader"] = info.get("uploader", "N/A")
        data["age_limit"] = info.get("age_limit", 0)
        a = info.get("upload_date", "N/A")

        if a != "N/A":
            date_year = int(str(a)[0:4])
            date_month = int(str(a)[4:6])
            date_day = int(str(a)[6:8])
            data["upload_date"] = timeago.format(
                datetime.date(date_year, date_month, date_day))
        else:
            data["upload_date"] = "N/A"

        data["description"] = info.get("description", "N/A")
        data["channel_follower_count"] = info.get("channel_follower_count", 0)
        data["like_count"] = info.get("like_count", 0)
        data["thumbnail"] = info.get("thumbnail", "N/A")

        # Extract available video streams
        for i in allstreams:
            itags.append(i["format_id"])

        # Extract 360p stream if available
        if "18" in itags:
            streams["360p"] = []
            for o in allstreams:
                if o["format_id"] == "18":
                    streams["360p"].append({"size": "360", "url": o['url']})

        # Extract 720p stream if available
        if "22" in itags:
            streams["720p"] = []
            for o in allstreams:
                if o["format_id"] == "22":
                    streams["720p"].append({"size": "720", "url": o['url']})

        # Add streams to data dictionary and return
        data["streams"] = streams
        return data

    except DownloadError as e:
        return {"error": "Could not download video information. Possible geographical restrictions."}
    except Exception as e:
        return {"error": str(e)}


# Ejemplo de uso
video_info = GetTracks('dQw4w9WgXcQ')
print(video_info)
