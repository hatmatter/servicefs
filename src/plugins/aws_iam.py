import boto3
import boto3.session


class AWS_IAM():
    def __init__(self, aws_access_key_id, aws_secret_access_key, profile, region):
        self.session = boto3.session.Session(aws_access_key_id,
                                             aws_secret_access_key,
                                             region_name=region_name,
                                             profile_name=profile)

    def readdir(self, path, fh):
        return ['.', '..', 'AWS_IAM']
