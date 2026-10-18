# Atlas Operations Manual

## Authentication Overview

The Atlas service accepts signed access tokens issued by the identity gateway.

## Token Rotation

Access-token signing keys rotate every 24 hours, and the current key identifier is ATLAS-KV-104.

## Cache Behavior

The service caches validated token metadata for five minutes to reduce repeated verification work.

## Deployment Notes

Atlas runs in three regional clusters and uses rolling deployments.
