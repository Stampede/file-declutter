# file-declutter
Script to Auto-Delete Files in a directory after a certain amount of time
## What it does
The script is intended to reduce digital file clutter by auto-deleting files past a certain age.

It recursively scans a directory on your computer and records any files that it finds along with a timestamp for when they first appeared in the directory. If a file in that directory has been modified recently, it updates the "first appeared" timestamp to the file's modification time. If a file is more than 60 days old, then the script will delete it. The script will immediately delete any empty directories.

## Why I made it
I liked the convenience of using the Linux /tmp directory to auto-delete files, but I wanted something with more persistence.

## Example use cases
* Experiment on copies of your files with new software so you don't screw up the original files
* Saving memes to share with friends that will be stale in a few weeks
* Edit photos, videos or audio files in different ways while you decide which version you will keep
* For any short-term projects where you don't need to store your work long-term

## How to use
1. Create a directory at `$HOME/Downloads/'2 months to live/'`
2. Create a directory `logs/` inside that directory
3. Set up a cron job or task scheduler to run the script every 6 hours or so.
4. You can manually delete any files in the temp directory at any time, except for the `cleanup_shelf` file in the `logs/` folder. Don't mess with that one, or it will reset the clock on all the other files.

## How to customize for your setup
* You can change the location of your "temp directory" in line 9.
* You can increase or decrease the retention time in line 10.

### Other notes
* Not tested on Windows or Mac
* The "hitdict" variable name is a play on words. We are creating a hit list of files to delete...but they are stored in a Python dictionary, so it's a hit dict instead. Clever?
* I don't understand the different software licenses. As far as I'm concerned, this script is public domain.
