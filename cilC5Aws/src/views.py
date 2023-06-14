import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3 = session.client('s3')
        response = s3.list_buckets()

        # Retrieve the list of buckets
        buckets = response['Buckets']
        print(buckets)

        return render(request, "index.html", {"buckets": buckets})

    def post(self, request):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        print(aws_access_key_id, aws_secret_access_key)

        session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3 = session.client('s3')

        try:
            print("In try")
            response = s3.create_bucket(
                Bucket=request.POST.get('name').lower().replace(" ", "-"),
                CreateBucketConfiguration={
                    'LocationConstraint': 'us-east-2'
                }
            )

            # TODO: Check if bucket already exist
            print(response['ResponseMetadata']['HTTPStatusCode'])

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("Got here")
                send_mail(
                    'S3 Bucket Created',
                    'Your Bucket was created successfully!',
                    settings.FROM_EMAIL,
                    [request.POST.get('email')],
                    fail_silently=False,
                )
                return JsonResponse({'message': 'Your Bucket was created successfully!'})
        except:
            print("In except")
            return JsonResponse({'message': 'Error encountered'})


class DeleteBucket(View):
    def post(self, request):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        print(request.POST.get("bucket"))

        # Create an S3 client using the session
        s3 = session.client('s3')

        # Specify the bucket name to delete
        bucket_name = request.POST.get("bucket")

        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)

        print(f"Bucket '{bucket_name}' deleted successfully.")
        return JsonResponse({'message': f"Bucket '{bucket_name}' deleted successfully."})
