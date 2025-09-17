import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DocumentDto } from '../../../../shared/services/document-api.service';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { DocumentApiService } from '../../../../shared/services/document-api.service';

@Component({
  selector: 'app-documents-table',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterModule, MatIconModule, MatButtonModule],
  templateUrl: './documents-table.component.html',
  styleUrls: ['./documents-table.component.scss']
})
export class DocumentsTableComponent {
  @Input() documents: DocumentDto[] = [];
  @Input() loading = false;
  @Output() deleted = new EventEmitter<number>();

  private readonly api = inject(DocumentApiService);
  riskClass(score?: number | null): string {
    if (score == null) return 'chip';
    if (score < 0.34) return 'chip chip--ok';
    if (score < 0.67) return 'chip chip--pending';
    return 'chip chip--error';
  }

  onDelete(ev: Event, id: number): void {
    ev.preventDefault();
    ev.stopPropagation();
    if (!confirm('¿Eliminar este documento?')) return;
    this.api.delete(id).subscribe({
      next: () => this.deleted.emit(id),
    });
  }
}


