# khinsider_midi_scraper
Simple scraper for locally cloning the midi files on khinsider.com/midi

### Dependencies
* Python 3.7+
* Libraries:
  * requests==2.28.2
  * beautifulsoup4==4.11.2

### Setup:
* Clone Repo
* pip3 install -r requirements.txt

### Usage:
python3 main.py

### Behaviour
* Runs with 10x concurrency on the root node i.e. the console level.
* Will create an "output" directory in the same folder as the script
* Will create sub-folders for each game and place the downloaded midi files in those sub-directories

