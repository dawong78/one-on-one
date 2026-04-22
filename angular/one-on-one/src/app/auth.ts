import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Auth {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/token/';

  login(username: string, password: string): Observable<any> {
    return this.http.post(this.apiUrl, { username: username, password: password });
  }

  refreshToken(refresh: string): Observable<any> {
    return this.http.post(`${this.apiUrl}refresh/`, { refresh });
  }

}
