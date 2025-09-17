import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { DocumentApiService, DocumentDto } from '../../../shared/services/document-api.service';
import { SignerApiService, SignerDto } from '../../../shared/services/signer-api.service';
import { CreateDocumentComponent } from '../../documents/components/create-document/create-document.component';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  standalone: true,
  selector: 'app-create-document-page',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
  , CreateDocumentComponent],
  template: `
  <section class="container" style="display:grid; gap:16px;">
    <mat-card>
      <mat-card-header>
        <mat-card-title>Nuevo documento</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <app-create-document (created)="onCreated($event)"></app-create-document>
      </mat-card-content>
    </mat-card>

    <mat-card *ngIf="doc() as d">
      <mat-card-header>
        <mat-card-title>Signers ({{ signers().length }}/2)</mat-card-title>
        <mat-card-subtitle>Agrega 1–2 antes de enviar</mat-card-subtitle>
      </mat-card-header>
      <mat-card-content>
        <form (submit)="addSigner($event)" style="display:flex; gap:8px; align-items:flex-end; flex-wrap:wrap;">
          <mat-form-field appearance="outline">
            <mat-label>Nombre</mat-label>
            <input matInput name="name" required />
          </mat-form-field>
          <mat-form-field appearance="outline">
            <mat-label>Email</mat-label>
            <input matInput name="email" type="email" required />
          </mat-form-field>
          <button mat-raised-button color="primary" type="submit" [disabled]="adding()">
            <mat-icon *ngIf="!adding()">person_add</mat-icon>
            <span *ngIf="!adding()">Agregar</span>
            <mat-progress-spinner *ngIf="adding()" diameter="18" mode="indeterminate"></mat-progress-spinner>
          </button>
        </form>
        <div style="margin-top:8px;">
          <div *ngFor="let s of signers()" style="display:flex; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px solid #eee;">
            <div>{{ s.name }} — {{ s.email }}</div>
            <button mat-button color="warn" (click)="removeSigner(s.id)">
              <mat-icon>delete</mat-icon>
              Eliminar
            </button>
          </div>
        </div>
      </mat-card-content>
      <mat-card-actions>
        <button mat-stroked-button (click)="goBack()">Salir</button>
        <button mat-raised-button color="accent" (click)="send()" [disabled]="!canSend()">
          <mat-icon>send</mat-icon>
          Enviar a firmar
        </button>
      </mat-card-actions>
    </mat-card>
  </section>
  `
})
export class CreateDocumentPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly docs = inject(DocumentApiService);
  private readonly signersApi = inject(SignerApiService);
  private readonly router = inject(Router);
  private readonly snack = inject(MatSnackBar);

  creating = signal<boolean>(false);
  adding = signal<boolean>(false);
  doc = signal<DocumentDto | null>(null);
  signers = signal<SignerDto[]>([]);
  toast = signal<string | null>(null);

  ngOnInit(): void {}

  onCreated(d: DocumentDto): void { this.doc.set(d); this.snack.open('Documento creado, agrega 1–2 signers', 'OK', { duration: 2500 }); }

  addSigner(ev: Event): void {
    ev.preventDefault();
    const form = ev.target as HTMLFormElement;
    const name = (form.elements.namedItem('name') as HTMLInputElement).value;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const d = this.doc(); if (!d) return;
    this.adding.set(true);
    this.signersApi.create(d.id, name, email).subscribe({
      next: (s) => { this.signers.set([...this.signers(), s]); form.reset(); this.snack.open('Signer agregado', 'OK', { duration: 2000 }); },
      complete: () => this.adding.set(false),
      error: () => { this.adding.set(false); this.snack.open('Error agregando signer', 'OK', { duration: 2500 }); }
    });
  }

  removeSigner(id: number): void {
    this.signersApi.delete(id).subscribe(() => this.signers.set(this.signers().filter(s => s.id !== id)));
  }

  canSend(): boolean { const c = this.signers().length; return !!this.doc() && c >= 1 && c <= 2; }

  send(): void {
    const d = this.doc(); if (!d || !this.canSend()) return;
    this.docs.sendToSign(d.id).subscribe({
      next: (upd) => { this.doc.set(upd); this.snack.open('Enviado a firmar', 'OK', { duration: 2500 }); },
      error: () => { this.snack.open('Error al enviar', 'OK', { duration: 2500 }); }
    });
  }

  goBack(): void { this.router.navigate(['/dashboard']); }
}


