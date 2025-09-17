from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
import json

from modules.document.application.use_cases.handle_zapsign_webhook import HandleZapSignWebhookUseCase
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository


@csrf_exempt
def zapsign_webhook(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)

    if not isinstance(body, dict):
        return JsonResponse({'detail': 'Invalid payload'}, status=400)

    try:
        use_case = HandleZapSignWebhookUseCase(
            document_commands=DjangoDocumentRepository(),
            document_queries=DjangoDocumentRepository(),
        )
        result = use_case.execute(body)
    except ValueError:
        return JsonResponse({'detail': 'Missing identifier'}, status=400)

    if result is None:
        # Idempotente si no se encuentra el documento
        return JsonResponse({}, status=204)
    return JsonResponse({}, status=200)


