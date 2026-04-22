import { Component, inject, OnInit, output, signal } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Auth } from '../auth';
import { Data } from '../data';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {
  loginForm: FormGroup;
  private authService = inject(Auth);
  private dataService = inject(Data);

  loginStatus = signal('Not Logged In');

  onLoggedIn = output<any>();

  constructor(private fb: FormBuilder) {
    // Initialize the FormGroup with validation rules
    this.loginForm = this.fb.group({
      username: [''],
      password: [''],
    });
  }

  ngOnInit(): void {
    this.checkIsLoggedIn();
  };

  checkIsLoggedIn(): void {
    this.dataService.getCurrentUser().subscribe({
      next: (data) => {
        if (data) {
          this.loginStatus.set('Logged In')
        } else {
          this.loginStatus.set('Not Logged In');
        }
          this.onLoggedIn.emit(this.loginStatus());
      }
    })
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value.username, this.loginForm.value.password).subscribe({
        next: (data: any) => {
          localStorage.setItem('access_token', data.access);
          localStorage.setItem('refresh_token', data.refresh);
          this.checkIsLoggedIn();
        },
        error: (err) => {
          console.error(err);
        }
      });
    }
  }
}
