import { Component, Input } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { DocumentDto } from '../../../../shared/services/document-api.service';

@Component({
  selector: 'app-documents-table',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './documents-table.component.html',
  styleUrls: ['./documents-table.component.scss']
})
export class DocumentsTableComponent {
  @Input() documents: DocumentDto[] = [];
  @Input() loading = false;
}


