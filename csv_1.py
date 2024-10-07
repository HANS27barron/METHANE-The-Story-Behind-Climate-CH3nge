import boto3
from netCDF4 import Dataset
import pandas as pd
import os

# S3 Bucket and file details
session = boto3.session.Session()
s3_client = session.client("s3")
bucket_name = "ghgc-data-store-dev"  # Replace with your actual bucket
cdf_file_key = "path_in_s3/your_file.cdf"  # Replace with your netCDF file key in S3
local_cdf_file = "local_file.cdf"
csv_output_file = "output_file.csv"

# Step 1: Download netCDF file from S3
def download_cdf_from_s3(bucket, s3_key, local_file):
    s3_client.download_file(bucket, s3_key, local_file)
    print(f"Downloaded {s3_key} from S3 to {local_file}")

# Step 2: Convert netCDF to CSV
def netcdf_to_csv(netcdf_file, csv_file):
    # Open the netCDF file
    nc = Dataset(netcdf_file, 'r')

    # Extract data (adjust variables based on your .cdf structure)
    data = {}
    for var in nc.variables:
        data[var] = nc.variables[var][:]

    # Close the netCDF file
    nc.close()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Write to CSV
    df.to_csv(csv_file, index=False)
    print(f"Converted {netcdf_file} to {csv_file}")

# Step 3: (Optional) Upload CSV to S3
def upload_csv_to_s3(bucket, csv_file, s3_key):
    s3_client.upload_file(csv_file, bucket, s3_key)
    print(f"Uploaded {csv_file} to S3 at {s3_key}")

# Execute the steps
download_cdf_from_s3(bucket_name, cdf_file_key, local_cdf_file)
netcdf_to_csv(local_cdf_file, csv_output_file)

# (Optional) Upload CSV back to S3
csv_s3_key = "path_in_s3/output_file.csv"  # Define where to store the CSV in S3
upload_csv_to_s3(bucket_name, csv_output_file, csv_s3_key)
