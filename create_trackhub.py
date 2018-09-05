import json, re, os
import boto3
import trackhub

s3_client = boto3.client('s3')


def handler(event, context):
    print("received event: " + json.dumps(event, indent=2))
    print("body is" + json.dumps(event['body'], indent=2))
    body = json.loads(event['body'])
    bucket = body['s3BucketName']
    # /tmp is the only writeable system
    tmp_dir = '/tmp/' + body['hubName']

    # First we initialize the components of a track hub
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name=body['hubName'],
        short_label=body['shortLabel'],
        long_label=body['longLabel'],
        genome=body['genome'],
        email=body['email'])

    # Next, we add a track for every sample.
    for file_info in body['samples']:
        file_URL = file_info['URL']

        if 'name' in file_info:
            name = file_info['name']
        else:
            name = file_info['shortLabel']
        name = re.sub(' ', '_', name)
        name = trackhub.helpers.sanitize(name)
        track = trackhub.Track(
            name=name,          # track names can't have any spaces or special chars.
            url=file_URL,      # filename to build this track from
            visibility='full',  # shows the full signal
            color=file_info['color'],
            autoScale='on',     # allow the track to autoscale
            tracktype=file_info['trackType'], # required when making a track
        )

        # Each track is added to the trackdb
        trackdb.add_tracks(track)

    # In this example we "upload" the hub locally. Files are created in the
    # "example_hub" directory, along with symlinks to the tracks' data files.
    trackhub.upload.stage_hub(hub=hub, staging=tmp_dir)

    # sync the directory to s3
    for r, d, f in os.walk(tmp_dir):
        for file in f:
            full_path = os.path.join(r, file)
            s3_path = re.sub(tmp_dir, body['hubName'], full_path)
            print("writing {} to {}".format(full_path, s3_path))
            s3_client.upload_file(full_path, bucket, s3_path,
                                  ExtraArgs={'ACL': 'public-read'})

    hubPath = "https://s3-us-west-2.amazonaws.com/dm-trackhubs/{}/{}".format(
        body['hubName'],
        body['hubName'] + '.hub.txt'
    )
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps({'hubPath': hubPath})
    }