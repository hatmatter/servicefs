import boto3
import boto3.session


class AWS_IAM():
    def __init__(self,
                 aws_access_key_id=None,
                 aws_secret_access_key=None,
                 aws_profile=None,
                 aws_region=None,
                 **kwargs):
        self.session = boto3.session.Session(aws_access_key_id,
                                             aws_secret_access_key,
                                             region_name=aws_region,
                                             profile_name=aws_profile)

    def readdir(self, path, fh):
        return ['.', '..', 'AWS_IAM']
