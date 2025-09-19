import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from '../../../app/shared/services/auth.service';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Limpiar mocks antes de cada test
    jest.clearAllMocks();
    
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('login', () => {
    it('should login successfully', () => {
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token'
      };

      service.login('test@example.com', 'password').subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/auth/login');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({
        email: 'test@example.com',
        password: 'password'
      });
      req.flush(mockResponse);
    });

    it('should store tokens after successful login', () => {
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token'
      };

      service.login('test@example.com', 'password').subscribe();

      const req = httpMock.expectOne('/api/auth/login');
      req.flush(mockResponse);

      expect(localStorageMock.setItem).toHaveBeenCalledWith('access_token', 'mock-access-token');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('refresh_token', 'mock-refresh-token');
    });
  });

  describe('register', () => {
    it('should register successfully', () => {
      const mockResponse = { id: 1, name: 'Test User', email: 'test@example.com' };

      service.register('Test User', 'test@example.com', 'password', 'api-token').subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/auth/register');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({
        name: 'Test User',
        email: 'test@example.com',
        password: 'password',
        api_token: 'api-token'
      });
      req.flush(mockResponse);
    });
  });

  describe('me', () => {
    it('should get user info', () => {
      const mockResponse = { id: 1, name: 'Test User', email: 'test@example.com' };

      service.me().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/auth/me');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });
  });

  describe('refresh', () => {
    it('should refresh token successfully', () => {
      localStorageMock.getItem.mockReturnValue('mock-refresh-token');
      const mockResponse = { access: 'new-access-token' };

      service.refresh().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/auth/refresh');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({
        refresh: 'mock-refresh-token'
      });
      req.flush(mockResponse);
    });
  });

  describe('token management', () => {
    it('should get access token', () => {
      localStorageMock.getItem.mockReturnValue('mock-access-token');
      expect(service.getAccessToken()).toBe('mock-access-token');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('access_token');
    });

    it('should return null when no access token', () => {
      localStorageMock.getItem.mockReturnValue(null);
      expect(service.getAccessToken()).toBeNull();
    });

    it('should get refresh token', () => {
      localStorageMock.getItem.mockReturnValue('mock-refresh-token');
      expect(service.getRefreshToken()).toBe('mock-refresh-token');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('refresh_token');
    });

    it('should return null when no refresh token', () => {
      localStorageMock.getItem.mockReturnValue(null);
      expect(service.getRefreshToken()).toBeNull();
    });

    it('should check authentication status', () => {
      localStorageMock.getItem.mockReturnValue(null);
      expect(service.isAuthenticated()).toBe(false);
      
      localStorageMock.getItem.mockReturnValue('mock-access-token');
      expect(service.isAuthenticated()).toBe(true);
    });

    it('should logout and clear tokens', () => {
      service.logout();
      
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('access_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('refresh_token');
    });
  });

  describe('setTokens', () => {
    it('should set access token only', () => {
      service['setTokens']({ access: 'access-only' });
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith('access_token', 'access-only');
      expect(localStorageMock.setItem).not.toHaveBeenCalledWith('refresh_token', expect.anything());
    });

    it('should set both tokens', () => {
      service['setTokens']({ 
        access: 'access-token', 
        refresh: 'refresh-token' 
      });
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith('access_token', 'access-token');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('refresh_token', 'refresh-token');
    });
  });
});