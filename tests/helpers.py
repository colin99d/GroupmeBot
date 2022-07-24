from bot import schemas


def get_post(option):
    return {
        "attachments": [],
        "avatar_url": "https://i.groupme.com/1024x1024.jpeg.c64d4fc5aeca45cb9fd2c1ca054fc22d",
        "created_at": 1632929238,
        "group_id": schemas.settings.TEST_GROUP_ID,
        "id": "163292923878111513",
        "name": "Colin Delahunty",
        "sender_id": "29762584",
        "sender_type": "user",
        "source_guid": "baac853e03cdf5d1d1ff77f105711ef3",
        "system": False,
        "text": f"@sportsbot {option}",
        "user_id": "29762584",
    }
