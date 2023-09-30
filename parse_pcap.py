import pyshark
import argparse
import requests


def getVendor(MACAddress):
    apiUrl = (
        f"https://www.macvendorlookup.com/api/v2/{MACAddress}"  # macvendorlookup.com
    )
    response = requests.get(apiUrl)
    if response.status_code == 200:
        data = response.json()
        if data and data[0].get("company"):
            return data[0]["company"]
    return "Not Found"


def getMACAddresses(input_file, output):
    addresses = set()

    cap = pyshark.FileCapture(input_file)
    for packet in cap:
        try:
            if "wlan" in packet:
                src = packet.wlan.sa
                dst = packet.wlan.da

                if src:
                    addresses.add(src)
                if dst:
                    addresses.add(dst)
        except AttributeError:
            pass

    with open(output, "w") as file:
        for mac in addresses:
            try:
                vendor = getVendor(mac.replace(":", ""))  # format for api
                file.write(f"{mac} - {vendor}\n")
            except Exception as e:
                pass

    return addresses


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="pcap file here")
    args = parser.parse_args()

    output = args.input.split(".")[0] + ".txt"

    addresses = getMACAddresses(args.input, output)

    print("Done! {} addresses found".format(len(addresses)))
