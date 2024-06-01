# Familiy Photos

Mastering the endless flood of familiy photos with **bash**, **python**, **data-science** and **machine-learning**.

## Setup

    brew install python fd exiftool slugify imagemagick cmake pyenv
    pyenv install 3.10.9
    pyenv shell 3.10.9
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Alternatively use a Dockerfile

TODO

## Download Images From iPhone

### Copy Photos & Movies from iPhone into a Local Folder

#### Method 1 (Preferred)

Open [icloud.com](https://www.icloud.com), select multiple images and click download icon. 

This downloads images as HEIC files and in addition Live-Images as MOV files

Save ZIP file in `~/Downloads` and unzip

    cd ~/Downloads
    rm -r ~/develop/family-photos/todo
    unzip -d ~/develop/family-photos/todo "iCloud Photos.zip"
    cd ~/develop/family-photos

#### Method 2

Use AirDrop from Fotos App on iPhone to keep Live-Images (converted into MOV files).

If Live-Images are not in the download folder, then select them on the iPhone under "Alben > Live Photos" and transer via AirDrop. 

Then copy Live Photos via

    cd ~/Library/Caches/Cleanup At Startup
    while read file; do echo ${file##*.}; done < <(find . -type f) | sort | uniq -c
    find . -type f -iname "*.jpg" -exec mv {} ~/Pictures/todo-new/ \;
    find . -type f \( -iname "*.mov" -or -iname "*.mp4" -or -iname "*.m4v" -or -iname "*.avi" \) -exec mv {} ~/Movies/todo-new/ \;

#### Method 3

Connect iPhone via USB with iMac and import into Fotos-App (using an "import" Mediathek), then export original Photos

## Preparations

    ./photo-tools --types todo

1. Convert all images to `jpg` files and move into `photos` folder.
2. Move all `mov` files into `movies` folder

    ./photo-tools --group todo

3. Find files with filename anomalies:

    ./filename-anomaly.py --path photos

4. Remove whitespace and special-characters in filenames and make lower-case:

    while read f; do slugify -adx "$f"; done < <(fd . -t f photos)

5. Set propper file permissions:

    ch photos
    chmod 644 *

6. Remove Apple quarantine (when downloading files on a Mac, Apple adds the `x-attribute: com.apple.quarantine`)

    fd . -t f todo -x xattr -d com.apple.quarantine

### Verify EXIF Date

List images with MISSING exif-date:

    cd ~/Pictures/TODO
    while read f; do exiftool $f | grep -q "Create Date" || echo $f; done < <(fd -t f)

Add exit date manually:

TODO

### Remove Duplicate Images

Remove all images which are already on the backup drive

  Get year of current files:

    cd ~/Pictures/TODO
    while read f; do exiftool $f | grep "Create Date" | head -n 1 | awk '{print $4}' | awk -F':' '{print $1}'; done < <(fd -t f) | tqdm --total `fd -t f | wc -l` | sort | uniq -c

  Summarize duplicates for a year, e.g. `2020`:

    cd ~/Pictures/TODO
    fdupes -r -m . /Volumes/Backup2/fotos/Familie/2020

  Delete duplicates from `todo` folder (preserves the first which is `Familie` folder)

    fdupes -r todo/ Familie/2020/
    fdupes -rdN todo/ Familie/2020/                                                                    # preserve the first file and delete rest without prompting
    while read f; do echo $f | grep ^todo | xargs rm -v; done < <(fdupes -Ar todo/ Familie/2020/)      # delete files from todo folder

### Manually delete bad images which are not worth to archive via images viewer, e.g. ApolloOne

    cd todo/
    open -a ApolloOne .

# Image Management

## Distribute photos into date folders

  sort images within `todo/*` into date folders `todo/2020/*`, `todo/2019/*`, ...

    cd todo/
    count=0; while IFS= read -r -d '' F; do
      D=`exiftool "$F" | grep "^Create Date" | head -n 1 | awk '{print $4}' | tr ':' '-'`;
      DD=`echo "$D" | cut -c 1-4`;
      count=$(($count+1));
      echo "[$count] $DD $D $F";
      mkdir -p "$DD/$D";
      FF=`basename "$F" | tr -s ' ' '-'`;
      mv "$F" "$DD/$D/$FF";
    done < <(find . -maxdepth 1 -type f -iname '*.jpg' -print0)

  or use bash script

    cd Pictures/
    ./distribute-images.sh todo

## import family photos in Photos app

1. Open `Photos`: Hold down `Option` Key and click `Photos`, then select Library.

2. Open Import Script

    open ImportPhotoFolders.applescript

3. Build and Run.

4. Select `Familie` folder

## backup family photos

    rsync -avP --stats /Users/thomas/Pictures/Familie /Volumes/Backup/fotos
    rsync -avP --stats /Users/thomas/Pictures/Familie /Volumes/Backup/fotos

# Movies Management

First check for possible movies files

    while read file; do echo ${file##*.}; done < <(find . -type f) | sort | uniq -c

## Sort movies into todo/date folders

  sort movies within `todo/*` into date folders `todo/2020/*`

    cd todo/
    count=0; while IFS= read -r -d '' F; do
      D=`exiftool "$F" | grep "^Date/Time Original" | head -n 1 | awk '{print $4}' | tr ':' '-'`;
      DD=`echo "$D" | cut -c 1-4`;
      count=$(($count+1));
      mkdir -p "$DD/$D";
      FF=`basename "$F" | tr -s ' ' '-'`;
      echo "[$count] $F $DD/$D/$FF";
      mv "$F" "$DD/$D/$FF";
    done < <(find . -maxdepth 1 -type f -iname '*.mov' -or -iname '*.mp4' -or -iname '*.m4v' -or -iname '*.avi' -print0)

## Backup family movies

    rsync -avP --stats /Users/thomas/Movies/Familie /Volumes/Backup/filme
    rsync -avP --stats /Users/thomas/Movies/Thomas /Volumes/Backup/filme

