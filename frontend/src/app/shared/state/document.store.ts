import { Injectable, inject, signal } from '@angular/core';
import { DocumentApiService, DocumentDto, CreateDocumentDto } from '../services/document-api.service';

@Injectable({ providedIn: 'root' })
export class DocumentStore {
  private readonly api = inject(DocumentApiService);

  readonly documents = signal<DocumentDto[]>([]);
  readonly loading = signal<boolean>(false);

  load(): void {
    this.loading.set(true);
    this.api.list().subscribe({
      next: (items) => this.documents.set(items),
      error: () => this.loading.set(false),
      complete: () => this.loading.set(false),
    });
  }

  addLocal(doc: DocumentDto): void {
    this.documents.update((arr) => [doc, ...arr]);
  }
}


