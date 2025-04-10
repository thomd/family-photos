# Familiy Photos

Mastering the endless flood of familiy photos with **bash**, **python**, **data-science** and **machine-learning**.

## Setup

Setup of python based tools:

    brew install python cmake pyenv
    pyenv install 3.10.9
    pyenv shell 3.10.9
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Setup of bash based tools:

    brew install fd exiftool imagemagick cmake
    make

## Download Images and Movies From iPhone

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

## Preparation

Print file types:

    ./photo-tools --types todo

Normalize images:

    ./photo-tools --normalize todo

Move images into `photos` folder and movies into `movies` folder:

    ./photo-tools --group todo

Find files with filename anomalies:

    ./filename-anomaly --path todo_photos

## Remove Duplicate Images

Remove all images which are already on the backup drive (using md5 hash):

    ./photo-tools --duplicates photos /path/to/archive/folder

Remove images which are very similar (using dHash):

    ./remove-duplicates --images todo_photos

Manually remove images which are slightly similar using a webapp (using dHash):

    ./find-image-duplicates --images todo_photos --threshold 10

## Distribute into 'year/year-month-day' folders

Check for images with missing EXIF date:

    ./photo-tools --exif todo_photos

Distribute images into 'year/year-month-day' folders:

    ./photo-tools --distribute todo_photos

## Copy Images onto External Backup Drive

    rsync -avP --stats Fotos /Volumes/Backup/fotos

## Import Photos into Photos App

1. Open `Photos`: Hold down `Option` Key and click `Photos`, then select Library.

2. Open Import Script

    open ImportPhotoFolders.applescript

3. Build and Run.

4. Select `Familie` folder

## Photo Applications

Alternative apps for photo management:

1. [PhotoPrism](https://www.photoprism.app/) is an AI-Powered Photos App for the Decentralized Web. It makes use of the latest technologies to tag and find
   pictures automatically without getting in your way. You can run it at home, on a private server, or in the cloud. See also this [docker-compose.yml](https://awesome-docker-compose.com/apps/photo-server/photoprism).
