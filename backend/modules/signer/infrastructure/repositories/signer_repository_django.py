from modules.signer.application.ports import SignerCommandRepository, SignerQueryRepository
from modules.signer.application.dtos import SignerDTO
from modules.signer.infrastructure.django_app.models import Signer


class DjangoSignerRepository(SignerCommandRepository, SignerQueryRepository):
    def create(self, document_id: int, name: str, email: str) -> SignerDTO:
        obj = Signer.objects.create(document_id=document_id, name=name.strip(), email=email.strip().lower())
        return SignerDTO(id=obj.id, document_id=obj.document_id, name=obj.name, email=obj.email, created_at=obj.created_at)

    def delete(self, signer_id: int) -> bool:
        deleted, _ = Signer.objects.filter(id=signer_id).delete()
        return deleted > 0

    def count_by_document(self, document_id: int) -> int:
        return Signer.objects.filter(document_id=document_id).count()

    def get_by_document_and_email(self, document_id: int, email: str) -> SignerDTO | None:
        try:
            obj = Signer.objects.get(document_id=document_id, email=email.strip().lower())
        except Signer.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return SignerDTO(id=obj.id, document_id=obj.document_id, name=obj.name, email=obj.email, created_at=obj.created_at)

    def list_by_document(self, document_id: int) -> list[SignerDTO]:
        return [
            SignerDTO(id=o.id, document_id=o.document_id, name=o.name, email=o.email, created_at=o.created_at)
            for o in Signer.objects.filter(document_id=document_id).order_by('id')
        ]


