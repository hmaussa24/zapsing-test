import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DocumentApiService, DocumentDto, CreateDocumentDto, DocumentAnalysisDto } from '../../../app/shared/services/document-api.service';

describe('DocumentApiService', () => {
  let service: DocumentApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DocumentApiService]
    });
    service = TestBed.inject(DocumentApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('list', () => {
    it('should list documents with pagination', () => {
      const mockResponse = {
        count: 2,
        next: null,
        previous: null,
        results: [
          { id: 1, company_id: 1, name: 'Doc 1', pdf_url: 'http://example.com/doc1.pdf', status: 'created' },
          { id: 2, company_id: 1, name: 'Doc 2', pdf_url: 'http://example.com/doc2.pdf', status: 'created' }
        ]
      };

      service.list({ page: 1, page_size: 10 }).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/?page=1&page_size=10');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should list documents without parameters', () => {
      const mockResponse = {
        count: 1,
        next: null,
        previous: null,
        results: [
          { id: 1, company_id: 1, name: 'Doc 1', pdf_url: 'http://example.com/doc1.pdf', status: 'created' }
        ]
      };

      service.list().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });
  });

  describe('create', () => {
    it('should create document successfully', () => {
      const createDto: CreateDocumentDto = {
        name: 'Test Document',
        pdf_url: 'http://example.com/test.pdf'
      };

      const mockResponse: DocumentDto = {
        id: 1,
        company_id: 1,
        name: 'Test Document',
        pdf_url: 'http://example.com/test.pdf',
        status: 'created',
        created_at: '2024-01-01T00:00:00Z'
      };

      service.create(createDto).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(createDto);
      req.flush(mockResponse);
    });

    it('should handle creation errors', () => {
      const createDto: CreateDocumentDto = {
        name: '',
        pdf_url: 'invalid-url'
      };

      service.create(createDto).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(400);
        }
      });

      const req = httpMock.expectOne('/api/documents/');
      req.flush({ detail: 'Invalid data' }, { status: 400, statusText: 'Bad Request' });
    });
  });

  describe('getById', () => {
    it('should get document by id', () => {
      const mockResponse: DocumentDto = {
        id: 1,
        company_id: 1,
        name: 'Test Document',
        pdf_url: 'http://example.com/test.pdf',
        status: 'created'
      };

      service.getById(1).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/1/');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });
  });

  describe('updatePartial', () => {
    it('should update document partially', () => {
      const updateData = {
        name: 'Updated Document',
        status: 'sent'
      };

      const mockResponse: DocumentDto = {
        id: 1,
        company_id: 1,
        name: 'Updated Document',
        pdf_url: 'http://example.com/test.pdf',
        status: 'sent'
      };

      service.updatePartial(1, updateData).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/1/');
      expect(req.request.method).toBe('PATCH');
      expect(req.request.body).toEqual(updateData);
      req.flush(mockResponse);
    });
  });

  describe('delete', () => {
    it('should delete document', () => {
      service.delete(1).subscribe(response => {
        expect(response).toBeUndefined();
      });

      const req = httpMock.expectOne('/api/documents/1/');
      expect(req.request.method).toBe('DELETE');
      req.flush(null);
    });
  });

  describe('sendToSign', () => {
    it('should send document to sign', () => {
      const mockResponse: DocumentDto = {
        id: 1,
        company_id: 1,
        name: 'Test Document',
        pdf_url: 'http://example.com/test.pdf',
        status: 'sent',
        open_id: 'zapsign-open-id',
        token: 'zapsign-token'
      };

      service.sendToSign(1).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/1/send_to_sign/');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({});
      req.flush(mockResponse);
    });
  });

  describe('getAnalysis', () => {
    it('should get document analysis', () => {
      const mockResponse: DocumentAnalysisDto = {
        document_id: 1,
        summary: 'Document summary',
        labels: ['contract', 'legal'],
        entities: [{ type: 'person', value: 'John Doe' }],
        risk_score: 0.3,
        status: 'done',
        missing_topics: 'Payment terms',
        insights: 'Consider adding payment terms'
      };

      service.getAnalysis(1).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/documents/1/analysis/');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });
  });

  describe('requestAnalyze', () => {
    it('should request document analysis', () => {
      service.requestAnalyze(1).subscribe(response => {
        expect(response).toBeUndefined();
      });

      const req = httpMock.expectOne('/api/documents/1/analyze/');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({});
      req.flush(null);
    });
  });
});
