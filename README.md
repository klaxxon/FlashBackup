# FlashBackup

This is my attempt to learn python and hopefully solve a problem.  I wanted something that would test the modification time and size of files (and possible a hash) on my backup flash drive against what was to be backed up.  Problem is, I do not want to read/scan the entire flash drive because it is slow, so I want to store all of the relevent data somewhere that can be accessed fast.  Soooooo....

Simple python script to efficiently copy files to USB flash drives and maintain.  A Sqlite3 database is maintained on the USB drive that contains all of the modification times and sizes so they can be compared on subsequent runs.

Usage: python flashbackup.py [fromdir1 fromdir2 ...] todir<br/>
NOTE: Do not use ../ before your from paths.

Example: Need to backup /test and /home/myuser directory.  Flash drive is mounted at /media/flash

Files to backup
<pre>
/test/dir1/
            test1.log
            test2.log
/test/dir2
            test3.log
/home/myuser
            user.log
</pre>
Run the command to backup these two diectories to /media/flash
<pre>
$ python flashbackup.py /test /home/myuser /media/flash
</pre>
The flash drive will have the following files:
<pre>
/media/flash/
            flashbackup.db
/media/flash/backup/test/dir1/
            test1.log.bz2
            test2.log.bz2
/media/flash/backup/test/dir2/
            test3.log.bz2
/media/flash/backup/home/myuser
            user.log.bz2
</pre>

The flash drive will have a backup directory containing the full paths of both the /test and /home/myuser backups.
All files will be bzip2 and have a bz2 extension.

This program creates a sqlite3 database on the flash media that contains a list of the files and the
modification time and size.  These are used in subsequent runs to determine what files have been touched and require copying.

