import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DocumentDetailComponent } from '../../documents/components/document-detail/document-detail.component';

@Component({
  standalone: true,
  selector: 'app-document-detail-page',
  imports: [CommonModule, RouterModule, DocumentDetailComponent],
  template: `<app-document-detail></app-document-detail>`
})
export class DocumentDetailPage {}
