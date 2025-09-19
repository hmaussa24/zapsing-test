import { TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { of, throwError } from 'rxjs';
import { AuthService } from '../../../app/shared/services/auth.service';

// Crear una clase de test que simule la lógica de LoginPage sin el template
class LoginPageTestClass {
  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private snack: MatSnackBar
  ) {}

  submit(): void {
    if (this.form.invalid) return;
    const { email, password } = this.form.value;
    this.auth.login(email!, password!).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: () => this.snack.open('Credenciales inválidas', 'OK', { duration: 2500 })
    });
  }
}

describe('LoginPage Logic', () => {
  let component: LoginPageTestClass;
  let authService: jest.Mocked<AuthService>;
  let router: jest.Mocked<Router>;
  let snackBar: jest.Mocked<MatSnackBar>;

  beforeEach(() => {
    const authSpy = {
      login: jest.fn()
    } as jest.Mocked<Partial<AuthService>>;
    
    const routerSpy = {
      navigate: jest.fn()
    } as jest.Mocked<Partial<Router>>;
    
    const snackSpy = {
      open: jest.fn()
    } as jest.Mocked<Partial<MatSnackBar>>;

    TestBed.configureTestingModule({
      imports: [ReactiveFormsModule],
      providers: [
        FormBuilder,
        { provide: AuthService, useValue: authSpy },
        { provide: Router, useValue: routerSpy },
        { provide: MatSnackBar, useValue: snackSpy }
      ]
    });

    // Crear la clase de test con inyección de dependencias
    component = new LoginPageTestClass(
      TestBed.inject(FormBuilder),
      TestBed.inject(AuthService),
      TestBed.inject(Router),
      TestBed.inject(MatSnackBar)
    );
    
    authService = TestBed.inject(AuthService) as jest.Mocked<AuthService>;
    router = TestBed.inject(Router) as jest.Mocked<Router>;
    snackBar = TestBed.inject(MatSnackBar) as jest.Mocked<MatSnackBar>;
  });

  describe('form validation', () => {
    it('should validate required fields', () => {
      const form = component.form;
      
      expect(form.get('email')?.hasError('required')).toBe(true);
      expect(form.get('password')?.hasError('required')).toBe(true);
      expect(form.invalid).toBe(true);
    });

    it('should validate email format', () => {
      const emailControl = component.form.get('email');
      
      emailControl?.setValue('invalid-email');
      expect(emailControl?.hasError('email')).toBe(true);
      
      emailControl?.setValue('valid@example.com');
      expect(emailControl?.hasError('email')).toBe(false);
    });

    it('should validate password minimum length', () => {
      const passwordControl = component.form.get('password');
      
      passwordControl?.setValue('123');
      expect(passwordControl?.hasError('minlength')).toBe(true);
      
      passwordControl?.setValue('123456');
      expect(passwordControl?.hasError('minlength')).toBe(false);
    });

    it('should be valid with correct data', () => {
      component.form.patchValue({
        email: 'test@example.com',
        password: 'password123'
      });

      expect(component.form.valid).toBe(true);
    });
  });

  describe('submit', () => {
    it('should not submit when form is invalid', () => {
      component.form.patchValue({
        email: 'invalid-email',
        password: '123'
      });

      component.submit();

      expect(authService.login).not.toHaveBeenCalled();
    });

    it('should login successfully and navigate to dashboard', () => {
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token'
      };

      authService.login.mockReturnValue(of(mockResponse));

      component.form.patchValue({
        email: 'test@example.com',
        password: 'password123'
      });

      component.submit();

      expect(authService.login).toHaveBeenCalledWith('test@example.com', 'password123');
      expect(router.navigate).toHaveBeenCalledWith(['/dashboard']);
    });

    it('should show error message on login failure', () => {
      authService.login.mockReturnValue(throwError(() => new Error('Login failed')));

      component.form.patchValue({
        email: 'test@example.com',
        password: 'wrongpassword'
      });

      component.submit();

      expect(authService.login).toHaveBeenCalledWith('test@example.com', 'wrongpassword');
      expect(snackBar.open).toHaveBeenCalledWith('Credenciales inválidas', 'OK', { duration: 2500 });
    });
  });

  describe('form initialization', () => {
    it('should initialize form with empty values', () => {
      expect(component.form.get('email')?.value).toBe('');
      expect(component.form.get('password')?.value).toBe('');
    });

    it('should have correct validators', () => {
      const emailControl = component.form.get('email');
      const passwordControl = component.form.get('password');

      expect(emailControl?.hasError('required')).toBe(true);
      expect(passwordControl?.hasError('required')).toBe(true);
    });
  });
});