import requests
import json

def get_filepaths():
    url = "https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    forecast = []
    for item in data:
        if 'entry' in item and item['entry'].endswith("-t3.nc"):
            forecast.append("https://mnemosyne.somisana.ac.za" + item['path'])

    return forecast

if __name__ == '__main__':
    paths = get_filepaths()
    print(json.dumps(paths, indent=2))