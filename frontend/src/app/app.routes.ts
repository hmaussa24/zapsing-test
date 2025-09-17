import { Routes } from '@angular/router';
import { ShellComponent } from './core/layouts/shell/shell.component';

export const routes: Routes = [
  {
    path: '',
    component: ShellComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
      { path: 'dashboard', loadComponent: () => import('./features/dashboard/pages/dashboard.page').then(m => m.DashboardPage) }
    ]
  },
  { path: '**', redirectTo: '' }
];
