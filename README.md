# FlashBackup
Simple python script to efficiently copy files to USB flash drives and maintain.  A Sqlite3 database is maintained on the USB drive that contains all of the modification times and sizes so they can be compared on subsequent runs.


Usage: python flashbackup.py [fromdir1 fromdir2 ...] todir

Example: Need to backup /var/subversion and /home/jgettys/Arduino directory.  Flash drive is mounted at /media/flash

$>python flashbackup.py /var/subversion /home/jgettys/Arduino /media/flash

The flash drive will have a backup directory containing the full paths of both the /var/subversion and /home/jgettys/Arduino backups.
All files will be bzip2 and have a bz2 extension.

This program creates a sqlite3 database on the flash media that contains a list of the files and the
modification time and size.  These are used in subsequent runs to determine what files have been touched and require copying.

