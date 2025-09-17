import { Routes } from '@angular/router';
import { ShellComponent } from './core/layouts/shell/shell.component';

export const routes: Routes = [
  {
    path: '',
    component: ShellComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
      { path: 'dashboard', loadComponent: () => import('./features/dashboard/pages/dashboard.page').then(m => m.DashboardPage) },
      { path: 'documents/new', loadComponent: () => import('./features/documents/pages/create-document.page').then(m => m.CreateDocumentPage) },
      { path: 'documents/:id', loadComponent: () => import('./features/documents/pages/document-detail.page').then(m => m.DocumentDetailPage) }
    ]
  },
  { path: '**', redirectTo: '' }
];
