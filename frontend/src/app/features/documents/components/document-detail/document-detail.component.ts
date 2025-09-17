import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { DocumentApiService, DocumentDto } from '../../../../shared/services/document-api.service';
import { SignerApiService, SignerDto } from '../../../../shared/services/signer-api.service';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  standalone: true,
  selector: 'app-document-detail',
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './document-detail.component.html',
  styleUrls: ['./document-detail.component.scss']
})
export class DocumentDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(DocumentApiService);
  private readonly signerApi = inject(SignerApiService);
  private readonly snack = inject(MatSnackBar);
  id = signal<number>(0);
  doc = signal<DocumentDto | null>(null);
  sending = signal<boolean>(false);
  error = signal<string | null>(null);
  signers = signal<SignerDto[]>([]);
  loadingDoc = signal<boolean>(false);
  loadingSigners = signal<boolean>(false);

  ngOnInit(): void {
    this.id.set(Number(this.route.snapshot.paramMap.get('id')));
    this.loadingDoc.set(true);
    this.api.getById(this.id()).subscribe({
      next: d => this.doc.set(d),
      complete: () => this.loadingDoc.set(false),
      error: () => this.loadingDoc.set(false)
    });
    this.loadSigners();
  }

  private loadSigners(): void {
    this.loadingSigners.set(true);
    this.signerApi.listByDocument(this.id()).subscribe({
      next: items => this.signers.set(items),
      complete: () => this.loadingSigners.set(false),
      error: () => this.loadingSigners.set(false)
    });
  }

  add(ev: Event): void {
    ev.preventDefault();
    const form = ev.target as HTMLFormElement;
    const name = (form.elements.namedItem('name') as HTMLInputElement).value;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    this.error.set(null);
    this.loadingSigners.set(true);
    this.signerApi.create(this.id(), name, email).subscribe({
      next: () => { form.reset(); this.snack.open('Signer agregado', 'OK', { duration: 2000 }); this.loadSigners(); },
      complete: () => this.loadingSigners.set(false),
      error: () => { this.loadingSigners.set(false); this.error.set('Error creando el signer'); this.snack.open('Error creando el signer', 'OK', { duration: 2500 }); }
    });
  }

  remove(signerId: number): void {
    this.loadingSigners.set(true);
    this.signerApi.delete(signerId).subscribe({
      next: () => this.loadSigners(),
      complete: () => this.loadingSigners.set(false),
      error: () => this.loadingSigners.set(false)
    });
  }

  send(): void {
    this.sending.set(true);
    this.api.sendToSign(this.id()).subscribe({
      next: d => { this.doc.set(d); this.snack.open('Documento enviado', 'OK', { duration: 2500 }); },
      complete: () => this.sending.set(false),
      error: () => { this.sending.set(false); this.snack.open('Error al enviar', 'OK', { duration: 2500 }); }
    });
  }
}


