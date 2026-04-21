import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Group } from './group';

@Injectable({
  providedIn: 'root',
})
export class Data {

  private http = inject(HttpClient);
  private apiUrl = "http://localhost:8000/";

  restUrl() {
    return this.apiUrl + "match/rest/";
  }
  groupUrl() {
    return this.restUrl() + "groups/";
  }
  groupIdUrl(groupId: number) {
    return this.restUrl() + "groups/" + groupId + "/";
  }

  getGroups(): Observable<any[]> {
    return this.http.get<any[]>(this.groupUrl());
  }

  addGroup(group: Group): Observable<any> {
    // const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    // return this.http.post<any>(this.groupUrl(), group, { headers });
    return this.http.post<any>(this.groupUrl(), group);
  }

  removeGroup(groupId: number): Observable<any> {
    return this.http.delete<any>(this.groupIdUrl(groupId));
  }

  resetGroup(groupId: number): Observable<any> {
    return this.http.post<any>(this.groupIdUrl(groupId) + 'clear_results/', '');
  }

  matchGroup(groupId: number): Observable<any> {
    return this.http.post<any>(this.groupIdUrl(groupId) + 'run_match/', '');
  }

  getMemberGroupIds(): Observable<number[]> {
    return this.http.get<number[]>(this.groupUrl() + 'member_group_ids/')
  }
}
