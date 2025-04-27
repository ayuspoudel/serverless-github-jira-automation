# Use AWS Lambda's Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Copy all local files into the container
COPY . .

# Install system libraries needed for pip builds
RUN yum install -y gcc gcc-c++ make libffi-devel
# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command for Lambda to run
CMD ["automated_triage.handler"]
