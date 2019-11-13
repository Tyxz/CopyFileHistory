# CopyFileHistory
Simple Python script to copy the latest version of your files from the FileHistory folder on your back up drive to a destination of your choosing.

I like to customize my OS. Additionally, I had a small SDD. Therefore, I placed my Windows 10 installation on the SSD and kept my user data on my HDD (sys link). Because I fell in love with the MacOS TimeMachine, I used the similiar software FileHistory from Microsoft. FileHistory (the automatic Windows Backup system) didn't like my settings. It coppied everything, but I was unable to restore it, after my HDD decided to stop working. 

This simple script helped me to rescue most of my data. FileHistory keeps the data as plain copies at ```F:\\FileHistory\\Username\\Computername\\Data```. Every version has a UTC timestamp of the modification. If the path is too long to store, it will create a obscure index, because Windows. These files are unrecoverable for me. The rest can simply be copied to a new destination, and every file except the latest version can be deleted. The latest version needs the timestamp removed and that's it. 

The script ```main.py src dst [--recursive] [--verbose] [--skip]``` will does that for you.

If you already copied everything, ```iso_remover.py path [--recursive]``` will remove the timestamps and keep the latest version.

Maybe it will help someone.
