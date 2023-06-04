import subprocess
import sys

downloads = "/home/tim/plex_media"

if "magnet" not in sys.argv[1]:
  print("This is not a valid magnet link")

else:
  print("This is a valid magnet link")
  magnet_link = sys.argv[1]
  start_index = magnet_link.find("&dn=") + len("&dn=")  # Find the starting index of the desired portion
  end_index = magnet_link.find("&", start_index)  # Find the ending index of the desired portion

  dir_name = magnet_link[start_index:end_index]  # Extract the desired portion

  print("Downloading Torrent")
  # Specify the file paths for output and error logs
  output_log = "/var/log/python-web-server/torrent.log"
  error_log = "/var/log/python-web-server/torrent.log"

  # Open the log files in append mode
  with open(output_log, "a") as out_file, open(error_log, "a") as err_file:
  # Execute the command and redirect output and error streams to the log files
      result = subprocess.run(["transmission-cli", magnet_link, "-f", "/home/tim/python-web-server/kill.sh", "-w", f"{downloads}/{dir_name}"],
                            stdout=out_file, stderr=err_file,
                            text=True)
