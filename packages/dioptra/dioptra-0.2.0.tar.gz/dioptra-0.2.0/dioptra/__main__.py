import os
import fire

from dioptra.api import Logger

API_KEY = os.environ.get('DIOPTRA_API_KEY')
DIOPTRA_BATCH_BUCKET = os.environ.get('DIOPTRA_BATCH_BUCKET', 'dioptra-batch-input-prod')

def upload_batch(ndjson_file, validate_sample=0.01):
    """Upload a batch of data to Dioptra.
    :param str ndjson_file: The path of the batch file in newline-delimited json (.ndjson) format.
    :param float validate_sample: Validate a random sample of the data (between 0-1) 
    """
    dioptra_logger = Logger(api_key=API_KEY)
    dioptra_logger.commit_ndjson_file(
        ndjson_file,
        validate_sample=validate_sample,
        batch_bucket=DIOPTRA_BATCH_BUCKET
    )

if __name__ == '__main__':
    fire.Fire({
        'upload_batch': upload_batch
    }, name='dioptra')
