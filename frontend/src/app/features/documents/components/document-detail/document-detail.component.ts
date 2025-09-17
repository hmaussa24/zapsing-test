import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { DocumentApiService, DocumentDto } from '../../../../shared/services/document-api.service';

@Component({
  standalone: true,
  selector: 'app-document-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './document-detail.component.html',
  styleUrls: ['./document-detail.component.scss']
})
export class DocumentDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(DocumentApiService);
  id = signal<number>(0);
  doc = signal<DocumentDto | null>(null);
  sending = signal<boolean>(false);
  error = signal<string | null>(null);
  signers = signal<Array<{id:number; name:string; email:string}>>([]);

  ngOnInit(): void {
    this.id.set(Number(this.route.snapshot.paramMap.get('id')));
    this.api.getById(this.id()).subscribe(d => this.doc.set(d));
    this.loadSigners();
  }

  private loadSigners(): void {
    fetch(`/api/signers/?document_id=${this.id()}`).then(r => r.json()).then(data => this.signers.set(data));
  }

  add(ev: Event): void {
    ev.preventDefault();
    const form = ev.target as HTMLFormElement;
    const name = (form.elements.namedItem('name') as HTMLInputElement).value;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    this.error.set(null);
    fetch('/api/signers/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_id: this.id(), name, email })
    }).then(async r => {
      if (!r.ok) throw new Error('No se pudo crear');
      form.reset();
      this.loadSigners();
    }).catch(() => this.error.set('Error creando el signer'));
  }

  remove(signerId: number): void {
    fetch(`/api/signers/${signerId}/`, { method: 'DELETE' }).then(() => this.loadSigners());
  }

  send(): void {
    this.sending.set(true);
    fetch(`/api/documents/${this.id()}/send_to_sign/`, { method: 'POST' })
      .then(r => r.json())
      .then(d => this.doc.set(d))
      .finally(() => this.sending.set(false));
  }
}


