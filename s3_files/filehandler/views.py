from django.http import JsonResponse
from cryptography.fernet import Fernet
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Initialize the Fernet key
key = Fernet.generate_key()
cipher = Fernet(key)


@csrf_exempt
def upload_file(request):
    """
    Accepts a POST request with a file, encrypts the file, and uploads it to S3.

    Args:
    - request: the HTTP request object

    Returns:
    - JsonResponse: a JSON response indicating success or failure
    """
    # Check if the request method is POST and a file is present
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        encrypted_data = cipher.encrypt(uploaded_file.read())

        # Upload encrypted data to S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=uploaded_file._name,
            Body=encrypted_data,
        )

        return JsonResponse({"message": "File uploaded and encrypted successfully."})
    else:
        return JsonResponse({"error": "No file provided."}, status=400)
