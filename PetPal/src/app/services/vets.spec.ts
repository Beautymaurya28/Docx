import { TestBed } from '@angular/core/testing';

import { Vets } from './vets.service';

describe('Vets', () => {
  let service: Vets;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Vets);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
