import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):


        return render(request, "index.html")

    def post(self, request):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3 = session.client('s3')

        # response = s3.create_bucket(
        #     Bucket=request.POST.get('name'),
        #     # CreateBucketConfiguration={
        #     #     'LocationConstraint': us-east-1'
        #     # }
        # )
        #
        # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # send_mail(
            #     'S3 Bucket Created',
            #     'Your Bucket was created successfully!',
            #     'majestyempirebiz@gmail.com',
            #     [request.POST.get('email')],
            #     fail_silently=False,
            # )
        #     return JsonResponse({'message': 'Your Bucket was created successfully!'})

        return JsonResponse({'message': 'Error encountered'})