from influxdb_client import AuthorizationsApi, Authorization

from dms_influx2.exceptions import BucketApiError


class Authorizations(AuthorizationsApi):
    def __init__(self, client):
        self.org = client.org
        self.organizations_api = client.organizations_api
        self.buckets_api = client.buckets_api
        super().__init__(client)

    def create_single_bucket_authorization(self, bucket_name: str, description: str = None, org_name: str = None,
                                           read: bool = True, write: bool = False, )-> Authorization:
        if org_name is None:
            org_name = self.org

        if not self.buckets_api().bucket_exists(bucket_name=bucket_name):
            raise BucketApiError(f"Bucket '{bucket_name}' does not exists")

        org = self.organizations_api().get_organization(org_name=org_name)
        bucket = self.buckets_api().find_bucket_by_name(bucket_name=bucket_name)
        permissions_read = {
            'action': 'read',
            'resource': {
                'id': bucket.id,
                'name': bucket.name,
                'org': org,
                'org_id': org.id,
                'type': 'buckets'
            }
        }
        permissions_write = {
            'action': 'write',
            'resource': {
                'id': bucket.id,
                'name': bucket.name,
                'org': org,
                'org_id': org.id,
                'type': 'buckets'
            }
        }
        permissions = []
        if read:
            permissions.append(permissions_read)
        if write:
            permissions.append(permissions_write)
        authorization = Authorization(org_id=org.id, permissions=permissions, description=description)
        return self.create_authorization(authorization=authorization)

