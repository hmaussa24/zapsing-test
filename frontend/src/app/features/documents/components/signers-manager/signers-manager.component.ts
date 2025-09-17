import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { SignerApiService, SignerDto } from '../../../../shared/services/signer-api.service';

@Component({
  standalone: true,
  selector: 'app-signers-manager',
  imports: [
    CommonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
  ],
  templateUrl: './signers-manager.component.html',
  styleUrls: ['./signers-manager.component.scss']
})
export class SignersManagerComponent implements OnChanges {
  private readonly signerApi = inject(SignerApiService);
  private readonly snack = inject(MatSnackBar);

  @Input() documentId: number | null = null;
  @Input() disabled = false;
  @Output() signersChanged = new EventEmitter<number>();

  loading = signal<boolean>(false);
  adding = signal<boolean>(false);
  signers = signal<SignerDto[]>([]);
  error = signal<string | null>(null);

  ngOnChanges(changes: SimpleChanges): void {
    if ('documentId' in changes) {
      this.load();
    }
  }

  load(): void {
    if (!this.documentId) return;
    this.loading.set(true);
    this.signerApi.listByDocument(this.documentId).subscribe({
      next: items => { this.signers.set(items); this.signersChanged.emit(items.length); },
      complete: () => this.loading.set(false),
      error: () => this.loading.set(false)
    });
  }

  add(ev: Event): void {
    ev.preventDefault();
    if (!this.documentId || this.disabled) return;
    const form = ev.target as HTMLFormElement;
    const name = (form.elements.namedItem('name') as HTMLInputElement).value;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    this.error.set(null);
    this.adding.set(true);
    this.signerApi.create(this.documentId, name, email).subscribe({
      next: s => {
        this.signers.set([...this.signers(), s]);
        this.signersChanged.emit(this.signers().length);
        this.snack.open('Signer agregado', 'OK', { duration: 2000 });
        form.reset();
      },
      complete: () => this.adding.set(false),
      error: () => { this.adding.set(false); this.error.set('Error agregando signer'); this.snack.open('Error agregando signer', 'OK', { duration: 2500 }); }
    });
  }

  remove(id: number): void {
    if (this.disabled) return;
    this.loading.set(true);
    this.signerApi.delete(id).subscribe({
      next: () => {
        this.signers.set(this.signers().filter(s => s.id !== id));
        this.signersChanged.emit(this.signers().length);
      },
      complete: () => this.loading.set(false),
      error: () => this.loading.set(false)
    });
  }
}

