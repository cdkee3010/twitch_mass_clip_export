import re
import urllib.request
import sys
from os import listdir
from os.path import isfile, join

basepath = 'downloads/'
SEPARATOR = '|'


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

    
skipped_clips = [];
for clip in open('clips.txt', 'r'):
    clip = clip.replace('\n', '')
    clip_data = clip.split(SEPARATOR)
    title, slug, mp4_url = clip_data;
    title = title.replace(' ', '_')
    regex = re.compile('[^a-zA-Z0-9_]')
    title = regex.sub('', title)
    out_filename = title + '_' + slug + '.mp4'
    output_path = (basepath + out_filename)

    #debug code
    #print(out_filename)

    print('\nDownloading clip slug: ' + slug)
    print('"' + title + '" -> ' + out_filename)
    print(mp4_url)
    try:
      urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
      print('\nDone.')
    except:
      skipped_clips.append((out_filename, mp4_url))
      print('\nError: ' + str(sys.exc_info()[0]))

print('\nFinished downloading all the videos.')

#Check for clips not downloaded, output difference.txt

if len(skipped_clips) == 0:
    print("Downloads completed successfully! No clips missed!")
else:
    saved_stdout = sys.stdout
    # count = 0
    discrepancy = open("difference.txt", "w+")
    sys.stdout = discrepancy
    for clip_data in skipped_clips:
      filename, mp4_url = clip_data
      print(filename + SEPARATOR + mp4_url + '\n')
      # count = count + 1

    discrepancy.close()
    sys.stdout = saved_stdout

    print("Number of skipped clips: " + str(len(skipped_clips)))
    print("difference.txt file created - shows clips NOT downloaded")

