import { Routes } from '@angular/router';
import { ShellComponent } from './core/layouts/shell/shell.component';
import { authGuard } from './shared/guards/auth.guard';

export const routes: Routes = [
  { path: 'auth/login', loadComponent: () => import('./features/auth/pages/login.page').then(m => m.LoginPage) },
  { path: 'auth/register', loadComponent: () => import('./features/auth/pages/register.page').then(m => m.RegisterPage) },
  {
    path: '',
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
      { path: 'dashboard', loadComponent: () => import('./features/dashboard/pages/dashboard.page').then(m => m.DashboardPage) },
      { path: 'documents/new', loadComponent: () => import('./features/documents/pages/create-document.page').then(m => m.CreateDocumentPage) },
      { path: 'documents/:id', loadComponent: () => import('./features/documents/pages/document-detail.page').then(m => m.DocumentDetailPage) }
    ]
  },
  { path: '**', redirectTo: '' }
];
