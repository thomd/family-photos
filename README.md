# Familiy Photos

Mastering the endless flood of familiy photos with **bash**, **python**, **data-science** and **machine-learning**.

## Setup

    brew install python fd exiftool slugify imagemagick

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Preparation

### Copy new photos & movies from iPhone into a local folder

#### Method 1 (prefered)

Open [icloud.com](https://www.icloud.com), select images and click download icon. This downloads a live-image as HEIC- & MOV-file and a regular image as HEIC file.

Save ZIP file in `~/Downloads` and unzip

    cd ~/Downloads
    unzip "iCloud Photos.zip"
    cd "iCloud Photos"

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

### Overview of file types

    while read file; do echo ${file##*.}; done < <(fd -t f) | sort | uniq -c

  with progress bar:

    while read file; do echo ${file##*.}; done < <(fd -t f) | tqdm --total `find . -type f | wc -l` | sort | uniq -c

### Convert Images to JPG

  Convert `HEIC` to `jpg`:

    fd -e heic -x convert {} {.}.jpg
    fd -e heic -X rm

  Make file extensions lowercase:

    for f in *.JPG; do mv "$f" "${f//JPG/jpg}"; done
    for f in *.MOV; do mv "$f" "${f//MOV/mov}"; done

  Rename `jpeg` to `jpg`:

    fd -e jpeg -x mv {} {.}.jpg

### Move images into Pictures folder

    fd -e jpg -x mv {} ~/Pictures/TODO

### Move movies into Movies folder

    fd -e mov -x mv {} ~/Movies/TODO

## Image Processing

    cd ~/Pictures

### Make a tar backup before doing any file changes

    tar -cvf TODO.tar TODO

with progress bar:

    tar -cvf TODO.tar TODO |& tqdm --total `fd . TODO | wc -l`

### File Cleanup

Find files with anomal filenames:

    cd ~/develop/family-photos
    ./filename-anomaly.py --path ~/Pictures/TODO

Rename file with anomal filename:

    mv weird-filename.jpg nice-filename.jpg

Remove whitespace and special-characters in filenames and make lower-case:

    cd ~/Pictures/TODO
    while read f; do slugify -adx "$f"; done < <(fd -t f) | tqdm --total `fd -t f | wc -l`

Set file permissions:

    cd ~/Pictures/TODO
    chmod 644 *

Remove Apple quarantine (when downloading files on a Mac, Apple adds the `x-attribute: com.apple.quarantine`)

    fd -t f -x xattr -d com.apple.quarantine

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

