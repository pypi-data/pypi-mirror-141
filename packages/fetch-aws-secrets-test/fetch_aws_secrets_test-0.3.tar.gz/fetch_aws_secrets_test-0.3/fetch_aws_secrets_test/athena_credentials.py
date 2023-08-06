# connect to athena and allow to run SQL queries

from pyathena import connect
from pyathena.pandas.cursor import PandasCursor
import configparser
import os


def fetch_data_from_s3(
    aws_profile, credential_path, s3_staging_dir, aws_region, schema_name
):
    config = configparser.ConfigParser()
    config.read_file(open(credential_path))

    os.environ["AWS_ACCESS_KEY_ID"] = config.get(aws_profile, "AWS_ACCESS_KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = config.get(
        aws_profile, "AWS_SECRET_ACCESS_KEY"
    )

    cursor = connect(
        aws_access_key=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        s3_staging_dir=s3_staging_dir,
        region_name=aws_region,
        schema_name=schema_name,
        cursor_class=PandasCursor,
    ).cursor()

    return cursor
