import { Component, EventEmitter, Output, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { DocumentApiService, DocumentDto } from '../../../../shared/services/document-api.service';

@Component({
  standalone: true,
  selector: 'app-create-document',
  imports: [CommonModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatProgressSpinnerModule],
  templateUrl: './create-document.component.html',
  styleUrls: ['./create-document.component.scss']
})
export class CreateDocumentComponent {
  private readonly fb = inject(FormBuilder);
  private readonly docs = inject(DocumentApiService);
  @Output() created = new EventEmitter<DocumentDto>();
  creating = signal<boolean>(false);
  createdFlag = signal<boolean>(false);

  form = this.fb.group({
    name: ['', [Validators.required, Validators.maxLength(200)]],
    pdf_url: ['', [Validators.required]]
  });

  submit(): void {
    if (this.form.invalid || this.creating()) return;
    this.creating.set(true);
    const raw = this.form.getRawValue();
    this.docs.create({ name: (raw.name ?? '').trim(), pdf_url: (raw.pdf_url ?? '').trim() }).subscribe({
      next: (d) => { this.form.disable(); this.createdFlag.set(true); this.created.emit(d); },
      complete: () => this.creating.set(false),
      error: () => this.creating.set(false)
    });
  }
}


