import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  public apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  public async submitForm(formData: any): Promise<any> {
    const data = await this.http.post(`${this.apiUrl}/query`, [formData]).toPromise();
    return data;
  }

  public async getHealth(): Promise<any> {
    const data = await this.http.get(`${this.apiUrl}/health`).toPromise();
    return data;
  }
}
