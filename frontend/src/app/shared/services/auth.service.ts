import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly accessKey = 'access_token';
  private readonly refreshKey = 'refresh_token';

  private setTokens(tokens: { access: string; refresh?: string }) {
    localStorage.setItem(this.accessKey, tokens.access);
    if (tokens.refresh) localStorage.setItem(this.refreshKey, tokens.refresh);
  }

  login(email: string, password: string): Observable<{ access: string; refresh: string }> {
    return this.http.post<{ access: string; refresh: string }>(`/api/auth/login`, { email, password }).pipe(
      tap(res => this.setTokens(res))
    );
  }

  register(name: string, email: string, password: string, api_token: string): Observable<any> {
    return this.http.post(`/api/auth/register`, { name, email, password, api_token });
  }

  me(): Observable<{ id: number; name: string; email: string }> {
    return this.http.get<{ id: number; name: string; email: string }>(`/api/auth/me`);
  }

  refresh(): Observable<{ access: string }> {
    return this.http.post<{ access: string }>(`/api/auth/refresh`, { refresh: this.getRefreshToken() });
  }

  getAccessToken(): string | null { return localStorage.getItem(this.accessKey); }
  getRefreshToken(): string | null { return localStorage.getItem(this.refreshKey); }
  isAuthenticated(): boolean { return !!this.getAccessToken(); }
  logout(): void {
    localStorage.removeItem(this.accessKey);
    localStorage.removeItem(this.refreshKey);
  }
}


