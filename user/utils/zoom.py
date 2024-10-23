import requests # type: ignore
from rest_framework.response import Response
from rest_framework import status

def create_zoom_meeting(request):
    # Zoom API URL for creating meetings
    zoom_api_url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {'tptYhdApSnm3QUFX7NHvjQ'}",
        "Content-Type": "application/json"
    }
    
    # Updated meeting data
    meeting_data = {
        "topic": "test",
        "type": 2,
        "start_time": "2024-12-01T10:00:00Z",  # Future date
        "duration": 3,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": True,
            "watermark": True,
            "audio": "voip",
            "auto_recording": "cloud"
        }
    }
    
    response = requests.post(zoom_api_url, json=meeting_data, headers=headers)
    
    # Log the exact response from Zoom for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
    
    if response.status_code == 201:
        return Response(response.json(), status=status.HTTP_201_CREATED)
    else:
        print("Error Details:", response.json())  # Log the error details
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
