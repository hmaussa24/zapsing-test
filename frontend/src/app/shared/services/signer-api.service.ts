import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SignerDto {
  id: number;
  document_id: number;
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class SignerApiService {
  private readonly http = inject(HttpClient);
  private readonly base = '/api/signers/';

  listByDocument(documentId: number): Observable<SignerDto[]> {
    return this.http.get<SignerDto[]>(`${this.base}?document_id=${documentId}`);
  }

  create(documentId: number, name: string, email: string): Observable<SignerDto> {
    return this.http.post<SignerDto>(this.base, { document_id: documentId, name, email });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }
}


