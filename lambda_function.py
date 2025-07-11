"""
Small AWS Lambda function to find the best bucket to serve static content
because Cloudfront can't directly talk to an S3 multiregion access point.
"""

import os
from config import FALLBACK_REGION, REGIONS, BASE_NAME


def find_best_region(current_region):
    """
    Find the geographical nearest region for a given source region
    """

    if current_region == FALLBACK_REGION:
        return FALLBACK_REGION

    # if current_region is eu-central-1
    # search_options become: [ eu-central-1, eu-central, eu ]
    # This way the options get broader gradualy and find the "best" bucket
    a, b, _ = current_region.split("-")
    search_options = [current_region, f"{a}-{b}", a]

    for option in search_options:
        for r in REGIONS:
            if r.startswith(option):
                return r

    # Return the fallback region if we didn't found a match with our algorithm
    return FALLBACK_REGION


def build_bucket_name(region):
    """
    Take a region name and build a FQDN for the S3 bucket
    """

    if region == FALLBACK_REGION:
        # Don't append the region suffix for the default bucket
        bucket_name = f"{BASE_NAME}"
    else:
        bucket_name = f"{BASE_NAME}-{region}"

    return f"{bucket_name}.s3.{region}.amazonaws.com"


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    Entrypoint for AWS Lambda
    """

    request = event["Records"][0]["cf"]["request"]

    # Fallback to FALLBACK_REGION if we can't get a region
    current_region = os.environ.get("AWS_REGION", FALLBACK_REGION)

    best_region = find_best_region(current_region)

    print(f"{current_region} got routed to {best_region}")

    domain_name = build_bucket_name(best_region)

    # Rewrite request to the newly found bucket
    request["origin"]["s3"]["region"] = best_region
    request["origin"]["s3"]["domainName"] = domain_name
    request["headers"]["host"] = [{"key": "host", "value": domain_name}]

    return request
