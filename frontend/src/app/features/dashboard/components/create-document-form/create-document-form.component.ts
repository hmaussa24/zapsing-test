import { Component, EventEmitter, Input, OnDestroy, Output, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { DocumentApiService, DocumentDto } from '../../../../shared/services/document-api.service';

@Component({
  selector: 'app-create-document-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './create-document-form.component.html',
  styleUrls: ['./create-document-form.component.scss']
})
export class CreateDocumentFormComponent implements OnDestroy {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(DocumentApiService);

  // companyId ya no es necesario; backend usa JWT
  @Output() documentCreated = new EventEmitter<DocumentDto>();

  loading = signal<boolean>(false);
  success = signal<string | null>(null);
  error = signal<string | null>(null);
  private successTimer: any;

  form = this.fb.group({
    name: ['', [Validators.required, Validators.maxLength(200)]],
    pdf_url: ['', [Validators.required, Validators.maxLength(4096), this.endsWithPdfValidator()]]
  });

  private endsWithPdfValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const value: string = (control.value ?? '').toString().trim();
      if (!value) return null; // handled by required
      // Acepta .../file.pdf o .../file.pdf?query=...
      const regex = /\.pdf(\?|$)/i;
      return regex.test(value) ? null : { endsWithPdf: true };
    };
  }

  submit(): void {
    if (this.form.invalid || this.loading()) return;
    this.loading.set(true);
    const { name, pdf_url } = this.form.getRawValue();
    const normalizedName = (name ?? '').trim().replace(/\s+/g, ' ');
    const normalizedPdfUrl = (pdf_url ?? '').trim();
    this.api.create({ name: normalizedName, pdf_url: normalizedPdfUrl }).subscribe({
      next: (doc) => {
        this.success.set('Documento creado correctamente');
        this.error.set(null);
        this.form.reset();
        this.documentCreated.emit(doc);
        clearTimeout(this.successTimer);
        this.successTimer = setTimeout(() => this.success.set(null), 3000);
      },
      error: (e) => {
        this.error.set('No se pudo crear el documento');
        this.success.set(null);
      },
      complete: () => this.loading.set(false)
    });
  }

  ngOnDestroy(): void {
    clearTimeout(this.successTimer);
  }
}


