import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

// This interface matches our 'VetPublic' model from the backend
export interface Vet {
  place_id: string;
  name: string;
  address: string;
  lat: number;
  lng: number;
  rating: number;
  total_ratings: number;
  phone?: string;
}

@Injectable({
  providedIn: 'root'
})
export class VetsService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  /**
   * Gets nearby vets. The Auth Interceptor will add the token.
   */
  getNearbyVets(lat: number, lng: number): Observable<Vet[]> {
    // Our backend endpoint expects lat and lng as query parameters
    return this.http.get<Vet[]>(`${this.apiUrl}/api/vets/nearby`, {
      params: {
        lat: lat.toString(),
        lng: lng.toString()
      }
    });
  }
}