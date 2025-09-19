import { TestBed } from '@angular/core/testing';
import { HttpRequest, HttpHandler, HttpErrorResponse } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';
import { AuthService } from '../../../app/shared/services/auth.service';
import { authInterceptor } from '../../../app/shared/interceptors/auth.interceptor';

describe('AuthInterceptor', () => {
  let authService: jest.Mocked<AuthService>;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    const authSpy = {
      getAccessToken: jest.fn(),
      getRefreshToken: jest.fn(),
      refresh: jest.fn()
    } as jest.Mocked<Partial<AuthService>>;

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        { provide: AuthService, useValue: authSpy }
      ]
    });

    authService = TestBed.inject(AuthService) as jest.Mocked<AuthService>;
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should add authorization header when token exists', () => {
    authService.getAccessToken.mockReturnValue('mock-access-token');

    const request = new HttpRequest('GET', '/api/test');
    const nextHandler = jest.fn().mockReturnValue(of({}));

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe()
    );

    expect(nextHandler).toHaveBeenCalled();
    const interceptedRequest = nextHandler.mock.calls[0][0];
    expect(interceptedRequest.headers.get('Authorization')).toBe('Bearer mock-access-token');
  });

  it('should not add authorization header when no token', () => {
    authService.getAccessToken.mockReturnValue(null);

    const request = new HttpRequest('GET', '/api/test');
    const nextHandler = jest.fn().mockReturnValue(of({}));

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe()
    );

    expect(nextHandler).toHaveBeenCalled();
    const interceptedRequest = nextHandler.mock.calls[0][0];
    expect(interceptedRequest.headers.get('Authorization')).toBeNull();
  });

  it('should refresh token on 401 and retry request', () => {
    authService.getAccessToken.mockReturnValue('expired-token');
    authService.getRefreshToken.mockReturnValue('valid-refresh-token');
    authService.refresh.mockReturnValue(of({ access: 'new-access-token' }));

    const request = new HttpRequest('GET', '/api/test');
    let callCount = 0;
    const nextHandler = jest.fn().mockImplementation((req) => {
      callCount++;
      if (callCount === 1) {
        // Primera llamada falla con 401
        return throwError(() => new HttpErrorResponse({ status: 401 }));
      } else {
        // Segunda llamada (retry) es exitosa
        return of({ data: 'success' });
      }
    });

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe(response => {
        expect(response).toEqual({ data: 'success' });
      })
    );

    expect(authService.refresh).toHaveBeenCalled();
    expect(nextHandler).toHaveBeenCalledTimes(2);
    
    // Verificar que el retry tiene el nuevo token
    const retryRequest = nextHandler.mock.calls[1][0];
    expect(retryRequest.headers.get('Authorization')).toBe('Bearer new-access-token');
  });

  it('should handle refresh token failure', () => {
    authService.getAccessToken.mockReturnValue('expired-token');
    authService.getRefreshToken.mockReturnValue('invalid-refresh-token');
    authService.refresh.mockReturnValue(throwError(() => new HttpErrorResponse({ status: 401 })));

    const request = new HttpRequest('GET', '/api/test');
    const nextHandler = jest.fn().mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 401 }))
    );

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(401);
        }
      })
    );

    expect(authService.refresh).toHaveBeenCalled();
    expect(nextHandler).toHaveBeenCalledTimes(1);
  });

  it('should not retry on non-401 errors', () => {
    authService.getAccessToken.mockReturnValue('valid-token');

    const request = new HttpRequest('GET', '/api/test');
    const nextHandler = jest.fn().mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 500 }))
    );

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(500);
        }
      })
    );

    expect(authService.refresh).not.toHaveBeenCalled();
    expect(nextHandler).toHaveBeenCalledTimes(1);
  });

  it('should not retry when no refresh token', () => {
    authService.getAccessToken.mockReturnValue('expired-token');
    authService.getRefreshToken.mockReturnValue(null);

    const request = new HttpRequest('GET', '/api/test');
    const nextHandler = jest.fn().mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 401 }))
    );

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authInterceptor(request, nextHandler).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(401);
        }
      })
    );

    expect(authService.refresh).not.toHaveBeenCalled();
    expect(nextHandler).toHaveBeenCalledTimes(1);
  });
});