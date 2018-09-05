import glob, re, os, sys, uuid
import json
import trackhub

with open("sample.json") as fh:
    data = json.load(fh)

tmp_dir = '/tmp/' + data['hubName']

# First we initialize the components of a track hub
hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name=data['hubName'],
    short_label=data['shortLabel'],
    long_label=data['longLabel'],
    genome=data['genome'],
    email=data['email'])

# Next, we add a track for every bigwig found.  In practice, you would
# point to your own files. In this example we use the path to the data
# included with trackhub.

for file_info in data['samples']:
    fileURL = file_info['URL']

    if 'name' in file_info:
        name = file_info['name']
    else:
        name = file_info['shortLabel']
    name = re.sub(' ', '_', name)
    name = trackhub.helpers.sanitize(name)
    track = trackhub.Track(
        name=name,  # track names can't have any spaces or special chars.
        url=fileURL,  # filename to build this track from
        visibility='full',  # shows the full signal
        color=file_info['color'],
        autoScale='on',  # allow the track to autoscale
        tracktype=file_info['trackType'],  # required when making a track
    )

    # Each track is added to the trackdb
    trackdb.add_tracks(track)

# In this example we "upload" the hub locally. Files are created in the
# "example_hub" directory, along with symlinks to the tracks' data files.
# This directory can then be pushed to GitHub or rsynced to a server.
trackhub.upload.stage_hub(hub=hub, staging=tmp_dir)

for r, d, f in os.walk(tmp_dir):
    for file in f:
        full_path = os.path.join(r, file)
        s3_path = re.sub(tmp_dir, data['hubName'], full_path)
        print("writing {} to {}".format(full_path, s3_path))


