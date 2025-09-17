import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DocumentApiService, DocumentDto, Page } from '../../../shared/services/document-api.service';
import { DocumentsTableComponent } from '../components/documents-table/documents-table.component';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { CreateDocumentFormComponent } from '../components/create-document-form/create-document-form.component';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, RouterModule, DocumentsTableComponent, MatPaginatorModule, CreateDocumentFormComponent],
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss']
})
export class DashboardPage implements OnInit {
  private readonly api = inject(DocumentApiService);
  loading = signal<boolean>(false);
  total = signal<number>(0);
  documents = signal<DocumentDto[]>([]);
  page = signal<number>(1);
  pageSize = signal<number>(5);
  pageSizeOptions = [5, 10, 20, 50];

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.api.list({ company_id: 1, page: this.page(), page_size: this.pageSize() }).subscribe({
      next: (resp: Page<DocumentDto>) => {
        this.total.set(resp.count);
        this.documents.set(resp.results);
      },
      error: () => this.loading.set(false),
      complete: () => this.loading.set(false)
    });
  }

  hasPrev(): boolean {
    return this.page() > 1;
  }

  hasNext(): boolean {
    return this.page() * this.pageSize() < this.total();
  }

  prevPage(): void {
    if (!this.hasPrev()) return;
    this.page.update(v => v - 1);
    this.load();
  }

  nextPage(): void {
    if (!this.hasNext()) return;
    this.page.update(v => v + 1);
    this.load();
  }

  onPageChange(ev: PageEvent): void {
    this.page.set(ev.pageIndex + 1);
    this.pageSize.set(ev.pageSize);
    this.load();
  }

  onCreated(doc: DocumentDto): void {
    // Mantener orden por created_at desc: recargar primera página
    this.page.set(1);
    this.load();
  }
}


