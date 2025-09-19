import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SignerApiService, SignerDto } from '../../../app/shared/services/signer-api.service';

describe('SignerApiService', () => {
  let service: SignerApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SignerApiService]
    });
    service = TestBed.inject(SignerApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('listByDocument', () => {
    it('should list signers by document', () => {
      const mockResponse: SignerDto[] = [
        { id: 1, document_id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, document_id: 1, name: 'Jane Smith', email: 'jane@example.com' }
      ];

      service.listByDocument(1).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/signers/?document_id=1');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should handle empty signers list', () => {
      const mockResponse: SignerDto[] = [];

      service.listByDocument(1).subscribe(response => {
        expect(response).toEqual([]);
      });

      const req = httpMock.expectOne('/api/signers/?document_id=1');
      req.flush(mockResponse);
    });
  });

  describe('create', () => {
    it('should create signer successfully', () => {
      const mockResponse: SignerDto = {
        id: 1,
        document_id: 1,
        name: 'John Doe',
        email: 'john@example.com'
      };

      service.create(1, 'John Doe', 'john@example.com').subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('/api/signers/');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({
        document_id: 1,
        name: 'John Doe',
        email: 'john@example.com'
      });
      req.flush(mockResponse);
    });

    it('should handle creation errors', () => {
      service.create(1, 'John Doe', 'invalid-email').subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(400);
        }
      });

      const req = httpMock.expectOne('/api/signers/');
      req.flush({ detail: 'Invalid email format' }, { status: 400, statusText: 'Bad Request' });
    });

    it('should handle duplicate email error', () => {
      service.create(1, 'John Doe', 'john@example.com').subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(400);
        }
      });

      const req = httpMock.expectOne('/api/signers/');
      req.flush({ detail: 'Email already exists for this document' }, { status: 400, statusText: 'Bad Request' });
    });

    it('should handle max signers limit error', () => {
      service.create(1, 'John Doe', 'john@example.com').subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(400);
        }
      });

      const req = httpMock.expectOne('/api/signers/');
      req.flush({ detail: 'Max 2 signers per document' }, { status: 400, statusText: 'Bad Request' });
    });
  });

  describe('delete', () => {
    it('should delete signer successfully', () => {
      service.delete(1).subscribe(response => {
        expect(response).toBeUndefined();
      });

      const req = httpMock.expectOne('/api/signers/1/');
      expect(req.request.method).toBe('DELETE');
      req.flush(null);
    });

    it('should handle deletion errors', () => {
      service.delete(999).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(404);
        }
      });

      const req = httpMock.expectOne('/api/signers/999/');
      req.flush({ detail: 'Not found' }, { status: 404, statusText: 'Not Found' });
    });
  });
});
