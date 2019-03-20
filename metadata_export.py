import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', dest='base_url', type=str, required=True)
parser.add_argument('--library', dest='library', type=str, required=True)

args = parser.parse_args()
print("finding library [%s] at %s" % (args.library, args.base_url))

sections = requests.get("%s/library/sections" % args.base_url, headers={'Accept': 'application/json'}).json()

key = None
for section in sections['MediaContainer']['Directory']:
    if section['title'] == args.library:
        print("found library [%s]" % args.library)
        key = section['key']
        break

if not key:
    print("library [%s] not found" % args.library)
    sys.exit(-1)

print("pulling content for library [%s]" % args.library)
content = requests.get("%s/library/sections/%s/all" % (args.base_url, key), headers={'Accept': 'application/json'}).json()

def safe(dict, key):
    return dict[key] if key in dict else None


print(', '.join([
    'TITLE',
    'RESOLUTION',
    'HEIGHT',
    'WIDTH',
    'BITRATE',
    'ASPECT_RATIO',
    'AUDIO_CODEC',
    'VIDEO_CODEC',
    'FRAMERATE'
]))

for record in content['MediaContainer']['Metadata']:
    media = record['Media'][0]

    print(', '.join([
        record['title'],
        media['videoResolution'],
        str(media['height']),
        str(media['width']),
        str(safe(media, 'bitrate')),
        str(media['aspectRatio']),
        media['audioCodec'],
        media['videoCodec'],
        media['videoFrameRate']
    ]))

