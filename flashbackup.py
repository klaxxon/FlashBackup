''' 
Flashbackup

Simple, database backed backup utility with compression

Usage: python flashbackup.py [fromdir1 fromdir2 ...] todir

Example: Need to backup subversion and Arduino directory.  Flash drive is mounted at /media/flash

$>python flashbackup.py /var/subversion /home/jgettys/Arduino /media/flash

The flash drive will have a backup directory containing the full paths of both the /var/subversion and /home/jgettys/Arduino backups.
All files will be bzip2 and have a bz2 extension.

This program creates a sqlite3 database on the flash media that contains a list of the files and the
modification time and size.  These are used in subsequent runs to determine what files have been touched and require copying.


'''
import sys
import os
import sqlite3
import datetime
import bz2

def humanize_bytes(bytes, precision=2):
	abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
	)
	if bytes == 1:
		return '1 byte'
	for factor, suffix in abbrevs:
		if bytes >= factor:
			break
	return '%.*f %s' % (precision, 1.0 * bytes / factor, suffix)

def copyfile(fname, toname):
	st = os.stat(fname)
	sz = st.st_size
	fsrc = open(fname, "rb")
	fdst = bz2.BZ2File(toname + ".bz2", "wb", compresslevel=9)
	#print "File: " + fname
	hsz = humanize_bytes(st.st_size)
	sys.stdout.write("%10d / %-10s\r" % (0, hsz))
	copied = 0
	while True:
		buf = fsrc.read(65536)
		if not buf:
			break
		fdst.write(buf)
		copied += len(buf)
		perc = 100 * copied / st.st_size
		sys.stdout.write("%10s / %-10s : " % (humanize_bytes(copied), hsz))
		i = 0
		while (i < perc):
			sys.stdout.write("*")
			i = i + 2
		while (i < 100):
			sys.stdout.write("-")
			i = i + 2
		sys.stdout.write(" %d%%\r" % (perc))
	fsrc.close()
	fdst.close()
	sys.stdout.write("\n")

def copyFile(fromname, todir, c):
	path = os.path.dirname(fromname)
	file = os.path.basename(fromname)
	topath = todir + "/backup/" + path
	if not os.path.exists(topath):
		#print "Creating path: " + topath
		os.makedirs(topath)
	#print "Copyfile from " + fromname + " to " + topath + "/" + file
	copyfile(fromname, topath + "/" +  file)
	st = os.stat(fromname)
	c.execute("UPDATE files SET modified='%d', filesize='%d' WHERE filename='%s'" % (st.st_mtime, st.st_size, fromname))


def dobackup(dirfrom, dirto, db):
	global filecount, copycount
	for dirName, subdirList, fileList in os.walk(dirfrom):
		#print("dirName=%s, dirfrom=%s" % (dirName, dirfrom))
		#print("Dir %s" % dirName)
		for fname in fileList:
			filecount = filecount + 1
			fname = dirName + "/" + fname
			#print("\t%s" % fname)
			# Does this exist in database?
			c = db.cursor()
			c.execute("SELECT modified, filesize FROM files WHERE filename='" + fname + "'")
			row = c.fetchone()
			if row == None:
				c.execute("INSERT INTO files VALUES('" + fname + "','','','%s')" % datetime.datetime.now())
				copycount = copycount + 1
				print "New file " + fname
				copyFile(fname, dirto, c)
			else:
				c.execute("UPDATE files SET lastchecked='%s' WHERE filename='%s'" % (datetime.datetime.now(), fname))
				st = os.stat(fname)
				#print "Testing change:"
				#print st
				#print row
				if ( ("%d" % st.st_mtime) != row[0]):
					print "Modified time has changed for " + fname
					copyFile(fname, dirto, c)
					copycount = copycount + 1
				elif ( ("%d" % st.st_size) != row[1]):
					print "File size has changed for " + fname
					copyFile(fname, dirto, c)
					copycount = copycount + 1

		db.commit()

def usage():
	print 'Usage: hasbackup.py [fromdir1 fromdir2...] todir'
	sys.exit(' ')


def main():
	global filecount, copycount
	filecount = 0
	copycount = 0
	if len(sys.argv) < 3:
		usage()
	print "Fast backup\n"
	dirto = sys.argv[len(sys.argv) - 1]
	db = sqlite3.connect(dirto + "/flashbackup.db")
	db.execute("CREATE TABLE IF NOT EXISTS files (filename text NOT NULL PRIMARY KEY, modified text, filesize text, lastchecked text)")
	db.commit()
	db.execute("UPDATE files SET lastchecked=null");
	db.commit()
	for i in range(1, len(sys.argv) - 1):
		dirfrom = sys.argv[i]
		dobackup(dirfrom, dirto, db)
	removecount = 0
	c = db.cursor()
	c2 = db.cursor()
	c.execute("SELECT filename FROM files WHERE lastchecked IS NULL")
	for row in c:
		rf = dirto + "/backup/" + row[0] + ".bz2"
		print "Removing file %s.bz2" % row[0]
		os.remove(rf)
		removecount = removecount + 1
	c.execute("DELETE FROM files WHERE lastchecked IS NULL")
	db.commit()
	db.close()
	print("%d files checked, %d files copied, %d files deleted" % (filecount, copycount, removecount))
	sys.exit(' ')



#-------------------------------
if __name__ == "__main__":
    main()
