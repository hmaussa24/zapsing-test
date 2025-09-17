import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  getCompanyId(): number {
    const stored = localStorage.getItem('company_id');
    return stored ? Number(stored) : 1; // stub hasta implementar login
  }
}


