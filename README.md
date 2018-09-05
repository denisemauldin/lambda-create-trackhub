# Lambda S3 trackhub

Use API Gateway to accept a JSON object of trackhub information.  
Use AWS Lambda to run a python script that uses daler/trackhub to create a trackhub and save it to S3.


Setup instructions


1) Create a zip file of Python code

https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python

Create a virtual environment
Install the requirements.txt

Add site packages to base directory of zip

	cd $VIRTUAL_ENV 
	zip -r9 ~/CreateTrackhub.zip .

Add create_trackhub.py to zip

	cd lambda-create-trackhub
	zip -g CreateTrackhub.zip create_trackhub.py

2) Create a Lambda function and upload the zip file to the function

Go to lambda console.

	https://console.aws.amazon.com/lambda

Create Function
Upload ZIP file in 'Function code'

3) Create a Role that can write to S3 by following:

Creating a function will prompt you to create a role.

https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html

It needs to be able to have S3 permissions for GetObject, GetObjectAcl, PutObject, PutObjectAcl

4) Use 'Add triggers' to create an api gateway that calls the function

https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-lambda.html

Have it require an API key.

5) Call lambda function using API Gateway POST request

Include x-api-key in header with API key as value.
Body is raw JSON (application/json) with sample.json included in body
It should return a JSON object with 'hubPath' key that points to the hubName.hub.txt that was created in S3.

# useful links

https://docs.aws.amazon.com/lambda/latest/dg/setup-awscli.html
