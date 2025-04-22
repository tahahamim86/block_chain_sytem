import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AccessToken, ExternalAppUser, DiseaseDiagnosis, MedicalRecord, DiagnosisBlock
from .utils import rebuild_user_blockchain  # Rebuild blockchain for a specific user


@api_view(['GET'])
def check_user_token(request, app_user_id):
    """
    Checks if a user has an associated token.
    """
    try:
        # Check if the user exists
        user = ExternalAppUser.objects.get(id=app_user_id)
        # Check if the user has an associated token
        has_token = AccessToken.objects.filter(app_user=user).exists()
        return Response({
            "app_user_id": app_user_id,
            "has_token": has_token
        })
    except ExternalAppUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def set_user_token(request):
    """
    Sets or updates the user's access token.
    """
    app_user_id = request.data.get("app_user_id")
    token = request.data.get("token")

    # Validate input data
    if not app_user_id or not token:
        return Response({"error": "Missing app_user_id or token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve or create an access token for the user
        user = ExternalAppUser.objects.get(id=app_user_id)
        AccessToken.objects.update_or_create(
            app_user=user,
            defaults={"token": token}
        )
        return Response({"message": f"Token set for user {user.email}"})
    except ExternalAppUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_docs_by_token(request, app_user_id):
    """
    Retrieves the documents of a user based on a valid token.
    Rebuilds the user's blockchain when accessing documents.
    """
    token = request.GET.get("token")

    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve user and check if they exist
        user = ExternalAppUser.objects.get(id=app_user_id)
    except ExternalAppUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the provided token matches the user's stored token
    try:
        access = AccessToken.objects.get(app_user=user)
        if access.token != token:
            return Response({"error": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
    except AccessToken.DoesNotExist:
        return Response({"error": "Access token not found"}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve medical record for the user
    try:
        medical_record = MedicalRecord.objects.get(app_user=user)
    except MedicalRecord.DoesNotExist:
        return Response({"status": "No medical record found"}, status=status.HTTP_404_NOT_FOUND)

    # Rebuild the blockchain for this user whenever documents are accessed
    rebuild_user_blockchain(user.id)

    # Get all diagnoses for the user's medical record
    diagnoses = DiseaseDiagnosis.objects.filter(medical_record=medical_record)

    # Prepare the response data for each diagnosis
    doc_list = []
    for diag in diagnoses:
        try:
            # Try fetching the related block for the diagnosis
            block = DiagnosisBlock.objects.get(diagnosis=diag)
            # Validate the block's integrity by checking if the computed hash matches the stored block hash
            is_valid = block.compute_hash() == block.block_hash
        except DiagnosisBlock.DoesNotExist:
            is_valid = False

        # Append diagnosis details and validity status to the response list
        doc_list.append({
            "id": diag.id,
            "disease_name": diag.disease_name,
            "diagnosis_date": diag.diagnosis_date,
            "diagnostic_details": diag.diagnostic_details,
            "image": base64.b64encode(diag.image).decode("utf-8") if diag.image else None,
            "hash_valid": is_valid
        })

    # Return the documents in the response
    return Response({
        "status": "Access granted",
        "documents": doc_list
    })
