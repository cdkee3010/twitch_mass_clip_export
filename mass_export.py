import re
import urllib.request
import requests
import sys
from os import listdir
from os.path import isfile, join

basepath = 'downloads/'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'


def retrieve_mp4_data(slug):
    cid = sys.argv[1]
    token = "Bearer "+sys.argv[2]
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": cid,"Authorization":token}).json()
    thumb_url = clip_info['data'][0]['thumbnail_url']
    title = clip_info['data'][0]['title']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


# for each clip in clips.txt
for clip in open('clips.txt', 'r'):
    slug = clip.split('/')[3].replace('\n', '')
    mp4_url, clip_title = retrieve_mp4_data(slug)
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    new_clip_title = clip_title+"_"+slug
    out_filename = regex.sub('', new_clip_title) + '.mp4'
    output_path = (basepath + out_filename)

    #debug code
    #print(out_filename)

    print('\nDownloading clip slug: ' + slug)
    print('"' + clip_title + '" -> ' + out_filename)
    print(mp4_url)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    print('\nDone.')

print('Finished downloading all the videos.')

#Check for clips not downloaded, output difference.txt

onlyfiles = [f for f in listdir('downloads/') if isfile(join('downloads/', f))]

files = []

for filename in onlyfiles:
    if filename == 'cross_reference.py' or filename == 'downloads.txt':
        continue
    else:
        a = filename.split("_")
        b = (a[len(a) - 1]).split(".")
        files.append((b[0]))

clips = open("clips.txt", "r")
clips_list = []

for lines in clips:
    c = lines.split("/")
    d = (c[len(c) - 1])
    e = d.splitlines()
    clips_list.append(e[0])

f = (list(set(clips_list) - set(files)))

if len(f) == 0:
    print("Downloads completed successfully! No clips missed!")
else:
    saved_stdout = sys.stdout
    count = 0
    discrepancy = open("difference.txt", "w+")
    sys.stdout = discrepancy
    for items in f:
        if len(items) > 1:
            print("https://clips.twitch.tv/"+items)
            count = count + 1

    discrepancy.close()
    sys.stdout = saved_stdout

    print("Discrepancy between files created and clips.txt: "+str(count))
    print("difference.txt file created - shows clips NOT downloaded")

