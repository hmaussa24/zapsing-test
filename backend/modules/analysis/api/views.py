from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

from modules.analysis.application.use_cases.handle_analysis_webhook import HandleAnalysisWebhookUseCase
from modules.analysis.infrastructure.repositories.analysis_repository_django import DjangoAnalysisRepository
from django.conf import settings


@csrf_exempt
def analysis_webhook(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    # Auth header
    expected = getattr(settings, 'AUTOMATION_API_KEY', None)
    provided = request.headers.get('X-Automation-Key')
    if not expected or provided != expected:
        return JsonResponse({'detail': 'Unauthorized'}, status=401)

    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)

    try:
        use_case = HandleAnalysisWebhookUseCase(
            analysis_commands=DjangoAnalysisRepository(),
            analysis_queries=DjangoAnalysisRepository(),
        )
        result = use_case.execute(body)
    except ValueError:
        return JsonResponse({'detail': 'Invalid payload'}, status=400)
    except Exception:
        # No romper el webhook si el documento aún no existe, responder 204
        return JsonResponse({}, status=204)

    if result is None:
        return JsonResponse({}, status=204)
    return JsonResponse({}, status=200)

