import requests
import zipfile
import io
import pandas as pd

# Your LTA API key
API_KEY = 'OUxVLPw5QjGPE37Z0lZ44g=='

HEADERS = {
    'AccountKey': API_KEY,
    'accept': 'application/json'
}

# LTA endpoints
ENDPOINTS = {
    'bus':   'https://datamall2.mytransport.sg/ltaodataservice/PV/Bus',
    'train': 'https://datamall2.mytransport.sg/ltaodataservice/PV/Train'
}

def get_fresh_link(endpoint):
    """Step 1 — Call LTA API to get a fresh S3 download link"""
    print(f"Calling LTA API: {endpoint}")
    response = requests.get(endpoint, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        link = data['value'][0]['Link']
        print(f"Fresh link obtained!")
        return link
    else:
        print(f"API call failed: {response.status_code}")
        return None

def download_and_save(link, save_path):
    """Step 2 — Download ZIP from S3, extract CSV, save locally"""
    print(f"Downloading ZIP...")
    response = requests.get(link)   # no API key needed for S3

    if response.status_code == 403:
        print("Link expired! Re-run the script to get a fresh link.")
        return None
    elif response.status_code != 200:
        print(f"Download failed: {response.status_code}")
        return None

    # Extract CSV from ZIP in memory
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        print(f"Files inside ZIP: {z.namelist()}")
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f)

    # Save to csv folder so you never need to call API again
    df.to_csv(save_path, index=False)
    print(f"Saved to {save_path}")
    return df

if __name__ == "__main__":
    # --- BUS ---
    bus_link = get_fresh_link(ENDPOINTS['bus'])
    if bus_link:
        df_bus = download_and_save(
            link      = bus_link,
            save_path = 'csv/PassengerVolumeByBusStops.csv'
        )
        if df_bus is not None:
            print("\n=== BUS PREVIEW ===")
            print(df_bus.head())
            print(df_bus.shape)
            print(df_bus.columns.tolist())

    # --- TRAIN ---
    train_link = get_fresh_link(ENDPOINTS['train'])
    if train_link:
        df_train = download_and_save(
            link      = train_link,
            save_path = 'csv/PassengerVolumeByTrainStations.csv'
        )
        if df_train is not None:
            print("\n=== TRAIN PREVIEW ===")
            print(df_train.head())
            print(df_train.shape)
            print(df_train.columns.tolist())