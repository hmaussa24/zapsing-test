import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { DocumentAnalysisDto } from '../../../../shared/services/document-api.service';

@Component({
  standalone: true,
  selector: 'app-analysis-card',
  imports: [CommonModule, MatCardModule, MatProgressSpinnerModule],
  templateUrl: './analysis-card.component.html',
  styleUrls: ['./analysis-card.component.scss']
})
export class AnalysisCardComponent {
  @Input() analysis: DocumentAnalysisDto | null = null;
  @Input() loading = false;
}


