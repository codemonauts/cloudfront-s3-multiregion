# Cloudfront S3 Multiregion

This Lambda@Edge function tries to find the best bucket to serve static content because Cloudfront can't directly talk
to an S3 multiregion access point.


## Assumptions / Setup
This script assumes that there is a bucket with the name `{BASE_NAME}` in the region `{FALLBACK_REGION}`. The buckets in all
other regions are named like `{BASE_NAME}-{region-name}`.

Then deploy this function to *us-east-1* and attach it to the *Origin Request* of your Cloudfront distribution.
