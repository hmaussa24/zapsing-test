import { inject } from '@angular/core';
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { AuthService } from '../services/auth.service';
import { catchError, switchMap, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.getAccessToken();
  const withAuth = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;

  return next(withAuth).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && auth.getRefreshToken()) {
        // Intentar refrescar y reintentar una vez
        return auth.refresh().pipe(
          switchMap(({ access }) => {
            // Guardar nuevo access y repetir request original
            localStorage.setItem('access_token', access);
            const retried = req.clone({ setHeaders: { Authorization: `Bearer ${access}` } });
            return next(retried);
          })
        );
      }
      return throwError(() => error);
    })
  );
};


