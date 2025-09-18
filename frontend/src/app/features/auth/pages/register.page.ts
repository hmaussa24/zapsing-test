import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from '../../../shared/services/auth.service';
import { AuthHeaderComponent } from '../../../shared/components/auth-header/auth-header.component';
import { AuthFooterComponent } from '../../../shared/components/auth-footer/auth-footer.component';

@Component({
  standalone: true,
  selector: 'app-register-page',
  imports: [CommonModule, ReactiveFormsModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatSnackBarModule, MatIconModule, AuthHeaderComponent, AuthFooterComponent],
  templateUrl: './register.page.html'
})
export class RegisterPage {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly snack = inject(MatSnackBar);

  form = this.fb.group({
    name: ['', [Validators.required, Validators.maxLength(255)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    api_token: ['', [Validators.required, Validators.minLength(10)]],
  });

  hideToken = true;

  submit(): void {
    if (this.form.invalid) return;
    const { name, email, password, api_token } = this.form.value;
    this.auth.register(name!, email!, password!, api_token!).subscribe({
      next: () => {
        this.snack.open('Registro exitoso, inicia sesión', 'OK', { duration: 2500 });
        this.router.navigate(['/auth/login']);
      },
      error: () => this.snack.open('No se pudo registrar', 'OK', { duration: 2500 })
    });
  }
}

