import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DocumentDto {
  id: number;
  company_id: number;
  name: string;
  pdf_url: string;
  status: string;
  open_id?: string | null;
  token?: string | null;
  created_at?: string;
}

export interface CreateDocumentDto {
  company_id: number;
  name: string;
  pdf_url: string;
}

export interface Page<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class DocumentApiService {
  private readonly http = inject(HttpClient);
  private readonly base = '/api/documents/';

  list(params?: { company_id?: number; page?: number; page_size?: number }): Observable<Page<DocumentDto>> {
    const q: string[] = [];
    if (params?.company_id != null) q.push(`company_id=${params.company_id}`);
    if (params?.page != null) q.push(`page=${params.page}`);
    if (params?.page_size != null) q.push(`page_size=${params.page_size}`);
    const query = q.length ? `?${q.join('&')}` : '';
    return this.http.get<Page<DocumentDto>>(`${this.base}${query}`);
  }

  create(payload: CreateDocumentDto): Observable<DocumentDto> {
    return this.http.post<DocumentDto>(this.base, payload);
  }

  getById(id: number): Observable<DocumentDto> {
    return this.http.get<DocumentDto>(`${this.base}${id}/`);
  }

  updatePartial(id: number, patch: Partial<CreateDocumentDto & Pick<DocumentDto,'status'>>): Observable<DocumentDto> {
    return this.http.patch<DocumentDto>(`${this.base}${id}/`, patch);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }

  sendToSign(id: number): Observable<DocumentDto> {
    return this.http.post<DocumentDto>(`${this.base}${id}/send_to_sign/`, {});
  }
}


