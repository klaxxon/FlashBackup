# FlashBackup
Simple python script to efficiently copy files to USB flash drives and maintain.  A Sqlite3 database is maintained on the USB drive that contains all of the modification times and sizes so they can be compared on subsequent runs.

Usage: python flashbackup.py [fromdir1 fromdir2 ...] todir
NOTE: Do not use ../ before your from paths.

Example: Need to backup /test and /home/myuser directory.  Flash drive is mounted at /media/flash

/test/dir1/
            test1.log
            test2.log
/test/dir2
            test3.log
/home/myuser
            user.log

$ python flashbackup.py /test /home/myuser /media/flash

The flash drive will have the following files:

/media/flash/
            flashbackup.db
/media/flash/backup/test/dir1/
            test1.log.bz2
            test2.log.bz2
/media/flash/backup/test/dir2/
            test3.log.bz2
/media/flash/backup/home/myuser
            user.log.bz2


The flash drive will have a backup directory containing the full paths of both the /test and /home/myuser backups.
All files will be bzip2 and have a bz2 extension.

This program creates a sqlite3 database on the flash media that contains a list of the files and the
modification time and size.  These are used in subsequent runs to determine what files have been touched and require copying.

