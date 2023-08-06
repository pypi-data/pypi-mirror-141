import boto3, os


class Cloud:

    local_path = '/tmp/'
    remote_path = 'public/images/thumbs/'


    def __init__(self, bucket=''):
        session = boto3.session.Session()
        self.client = session.client('s3',
                                     region_name=os.environ.get('DIGITALOCEAN_SPACES_REGION'),
                                     endpoint_url=os.environ.get('DIGITALOCEAN_SPACES_ENDPOINT'),
                                     aws_access_key_id=os.environ.get('DIGITALOCEAN_SPACES_KEY'),
                                     aws_secret_access_key=os.environ.get('DIGITALOCEAN_SPACES_SECRET')
                                     )
        self.bucket = bucket
        if not bucket:
            self.bucket = os.environ.get('DIGITALOCEAN_SPACES_BUCKET')

    def download_file(self, file_key):
        download_path = self.local_path + file_key
        remote_path = self.remote_path + file_key
        print(remote_path)
        self.client.download_file(Bucket=self.bucket, Key=remote_path, Filename='/tmp/' + file_key)
        return download_path
