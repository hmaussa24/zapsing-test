import { TestBed } from '@angular/core/testing';
import { Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../../../app/shared/services/auth.service';
import { authGuard } from '../../../app/shared/guards/auth.guard';

describe('AuthGuard', () => {
  let authService: jest.Mocked<AuthService>;
  let router: jest.Mocked<Router>;
  let mockRoute: Partial<ActivatedRouteSnapshot>;
  let mockState: Partial<RouterStateSnapshot>;

  beforeEach(() => {
    const authSpy = {
      isAuthenticated: jest.fn()
    } as jest.Mocked<Partial<AuthService>>;
    
    const routerSpy = {
      navigate: jest.fn()
    } as jest.Mocked<Partial<Router>>;

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authSpy },
        { provide: Router, useValue: routerSpy }
      ]
    });

    authService = TestBed.inject(AuthService) as jest.Mocked<AuthService>;
    router = TestBed.inject(Router) as jest.Mocked<Router>;
    
    mockRoute = {};
    mockState = { url: '/test' } as RouterStateSnapshot;
  });

  it('should allow access when authenticated', () => {
    authService.isAuthenticated.mockReturnValue(true);

    // Simular el contexto de inyección
    const result = TestBed.runInInjectionContext(() => 
      authGuard(mockRoute as ActivatedRouteSnapshot, mockState as RouterStateSnapshot)
    );

    expect(result).toBe(true);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should redirect to login when not authenticated', () => {
    authService.isAuthenticated.mockReturnValue(false);

    // Simular el contexto de inyección
    const result = TestBed.runInInjectionContext(() => 
      authGuard(mockRoute as ActivatedRouteSnapshot, mockState as RouterStateSnapshot)
    );

    expect(result).toBe(false);
    expect(router.navigate).toHaveBeenCalledWith(['/auth/login']);
  });

  it('should call isAuthenticated method', () => {
    authService.isAuthenticated.mockReturnValue(true);

    // Simular el contexto de inyección
    TestBed.runInInjectionContext(() => 
      authGuard(mockRoute as ActivatedRouteSnapshot, mockState as RouterStateSnapshot)
    );

    expect(authService.isAuthenticated).toHaveBeenCalled();
  });
});