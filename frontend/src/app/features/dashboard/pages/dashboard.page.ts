import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, NavigationEnd } from '@angular/router';
import { DocumentApiService, DocumentDto, DocumentAnalysisDto, Page } from '../../../shared/services/document-api.service';
import { SignerApiService, SignerDto } from '../../../shared/services/signer-api.service';
import { DocumentsTableComponent } from '../components/documents-table/documents-table.component';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { CreateDocumentFormComponent } from '../components/create-document-form/create-document-form.component';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, RouterModule, DocumentsTableComponent, MatPaginatorModule, CreateDocumentFormComponent, MatCardModule, MatButtonModule, MatIconModule, MatToolbarModule],
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss']
})
export class DashboardPage implements OnInit {
  private readonly api = inject(DocumentApiService);
  private readonly router = inject(Router);
  private readonly signerApi = inject(SignerApiService);
  loading = signal<boolean>(false);
  total = signal<number>(0);
  documents = signal<DocumentDto[]>([]);
  page = signal<number>(1);
  pageSize = signal<number>(5);
  pageSizeOptions = [5, 10, 20, 50];

  // Wizard inline
  showWizard = signal<boolean>(false);
  createdDoc = signal<DocumentDto | null>(null);
  signers = signal<SignerDto[]>([]);
  signersLoading = signal<boolean>(false);
  sending = signal<boolean>(false);
  toast = signal<string | null>(null);

  ngOnInit(): void {
    this.load();
    // Recargar al volver a /dashboard
    this.router.events.subscribe(ev => {
      if (ev instanceof NavigationEnd && (ev.urlAfterRedirects?.endsWith('/dashboard') || ev.url?.endsWith('/dashboard'))) {
        this.load();
      }
    });
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
    this.createdDoc.set(doc);
    this.showWizard.set(true);
    this.toast.set('Documento creado. Ahora agrega 1–2 signers.');
    setTimeout(() => this.toast.set(null), 3000);
    this.loadSigners();
  }

  startWizard(): void {
    this.showWizard.set(true);
    this.createdDoc.set(null);
    this.signers.set([]);
  }

  exitWizard(): void {
    this.showWizard.set(false);
    this.createdDoc.set(null);
    this.signers.set([]);
  }

  private loadSigners(): void {
    const doc = this.createdDoc();
    if (!doc) return;
    this.signersLoading.set(true);
    this.signerApi.listByDocument(doc.id).subscribe({
      next: (items) => this.signers.set(items),
      complete: () => this.signersLoading.set(false),
      error: () => this.signersLoading.set(false)
    });
  }

  addSigner(name: string, email: string): void {
    const doc = this.createdDoc();
    if (!doc) return;
    this.signersLoading.set(true);
    this.signerApi.create(doc.id, name, email).subscribe({
      next: () => {
        this.toast.set('Signer agregado');
        setTimeout(() => this.toast.set(null), 2000);
        this.loadSigners();
      },
      complete: () => this.signersLoading.set(false),
      error: () => {
        this.signersLoading.set(false);
        this.toast.set('Error al agregar signer');
        setTimeout(() => this.toast.set(null), 2500);
      }
    });
  }

  removeSigner(id: number): void {
    this.signersLoading.set(true);
    this.signerApi.delete(id).subscribe({
      next: () => this.loadSigners(),
      complete: () => this.signersLoading.set(false),
      error: () => this.signersLoading.set(false)
    });
  }

  canSend(): boolean {
    const c = this.signers().length;
    return c >= 1 && c <= 2 && !this.sending();
  }

  sendCurrent(): void {
    const doc = this.createdDoc();
    if (!doc || !this.canSend()) return;
    this.sending.set(true);
    this.api.sendToSign(doc.id).subscribe({
      next: (d) => {
        this.createdDoc.set(d);
        this.toast.set('Documento enviado a firmar');
        setTimeout(() => this.toast.set(null), 3000);
      },
      complete: () => this.sending.set(false),
      error: () => {
        this.sending.set(false);
        this.toast.set('Error al enviar a firmar');
        setTimeout(() => this.toast.set(null), 3000);
      }
    });
  }

  onDeleted(id: number): void {
    this.documents.set(this.documents().filter(d => d.id !== id));
    this.total.update(t => Math.max(0, t - 1));
  }
}


