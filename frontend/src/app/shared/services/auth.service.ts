import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly tokenKey = 'access_token';

  login(email: string, password: string): Observable<{ access: string }> {
    return this.http.post<{ access: string }>(`/api/auth/login`, { email, password }).pipe(
      tap(res => localStorage.setItem(this.tokenKey, res.access))
    );
  }

  register(name: string, email: string, password: string): Observable<any> {
    return this.http.post(`/api/auth/register`, { name, email, password });
  }

  me(): Observable<{ id: number; name: string; email: string }> {
    return this.http.get<{ id: number; name: string; email: string }>(`/api/auth/me`);
  }

  getToken(): string | null { return localStorage.getItem(this.tokenKey); }
  isAuthenticated(): boolean { return !!this.getToken(); }
  logout(): void { localStorage.removeItem(this.tokenKey); }
}


