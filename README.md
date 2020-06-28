
# PREPARATION

1. Copy all new photos & movies from all devices into a **download** folder. 

  Use AirDrop from Fotos App on iPhone to keep Live-Images (converted into MOV files)
  If Live-Images are not in the download folder, then select them on the iPhone under "Alben > Live Photos" and
  transer via AirDrop. Then copy Live Photos via

    cd ~/Library/Caches/Cleanup At Startup
    find . -type f -iname "*.mov" -exec cp {} ~/Pictures/todo/ \;
    find . -type f -iname "*.jpg" -exec cp {} ~/Pictures/todo/ \;

2. Get overview of file types

    while read file; do echo ${file##*.}; done < <(find . -type f) | sort | uniq -c

3. Move images and movies into **todo** folders

  Images:

    find . -type f -iname "*.jpg" -exec mv {} ~/Pictures/todo/ \;

  Movies:

    find . -type f -iname "*.mov" -exec mv {} ~/Movies/todo/ \;

3. Make a tar backup before doing any file changes

    tar -cvf todo.tar todo/

4. Remove **duplicate** images and movies

  Get distribution of years:

    cd todo/
    while read f; do exiftool $f | grep "Create Date" | head -n 1 | awk '{print $4}' | awk -F':' '{print $1}'; done < <(find . -type f) | tqdm --total `find . -type f | wc -l` | sort | uniq -c

  Search duplicates for all years

    cd ~/Pictures
    fdupes -rm todo/ Familie/2020/

  Delete duplicates from `todo` folder (preserves the first which is `Familie` folder)

    fdupes -r todo/ Familie/2020/
    fdupes -rdN todo/ Familie/2020/                                                                    # preserve the first file and delete rest without prompting
    while read f; do echo $f | grep ^todo | xargs rm -v; done < <(fdupes -Ar todo/ Familie/2020/)      # delete files from todo folder

5. Do some file **cleanup**

  Set file permissions

    cd todo/
    chmod 644 *

  Remove trailing ` 2` index from filename

    cd todo/
    find . -type f -name "* *"
    while read f; do mv "${f}" "${f/ 2/}"; done < <(find . -type f -iname "* 2.JPG")

  Make all file lowercase

    cd todo/
    slugify -n *
    slugify -iad *.jpg

6. Check if all photos have an EXIF date

  List images with missing exif-date:

    cd todo/
    while read f; do exiftool $f | grep -q "Create Date" || echo $f; done < <(find . -type f)

7. Manually delete **bad images** which are not worth to archive via images viewer, e.g. **ApolloOne**.

    cd todo/
    open -a ApolloOne .

# IMAGES

## sort photos into date folders

  sort images within `todo/*` into date folders `todo/2020/*`

    cd todo/
    count=0; while IFS= read -r -d '' F; do
      D=`exiftool "$F" | grep "Create Date" | head -n 1 | awk '{print $4}' | tr ':' '-'`;
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

## import family photos in `Photos` app

1. Open `Photos`: Hold down `Option` Key and click `Photos`, then select Library.

2. Open Import Script

    open ImportPhotoFolders.applescript

3. Build and Run.

4. Select `Familie` folder

## backup family photos

    rsync -avP --stats /Users/thomas/Pictures/Familie /Volumes/Backup2/fotos
    rsync -avP --stats /Users/thomas/Pictures/Familie /Volumes/Backup/fotos



# MOVIES

First check for possible movies files

    while read file; do echo ${file##*.}; done < <(find . -type f) | sort | uniq -c

## move movies from `~/Pictures` to `~/Movies`

    while read file; do
      D=$(dirname $file);
      F=$(basename $file);
      mkdir -p "/Users/thomas/Movies/Familie/2019/$D";
      mv "$file" $_;
    done < <(find . -type f -iname "*.mp4")

## backup family movies

    rsync -avP --stats /Users/thomas/Movies/Familie /Volumes/Backup2/filme



# vim:nospell:tw=0:nowrap
