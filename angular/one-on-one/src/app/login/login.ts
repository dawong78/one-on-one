import { Component, inject, output, signal } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Auth } from '../auth';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  loginForm: FormGroup;
  private authService = inject(Auth);

  login_status = signal('Not Logged In');

  onLoggedIn = output<any>();

  constructor(private fb: FormBuilder) {
    // Initialize the FormGroup with validation rules
    this.loginForm = this.fb.group({
      username: [''],
      password: [''],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value.username, this.loginForm.value.password).subscribe({
        next: (data: any) => {
          localStorage.setItem('access_token', data.access);
          localStorage.setItem('refresh_token', data.refresh);
          console.log("login success");
          this.login_status.set('Logged In');
          this.onLoggedIn.emit('loggin success')
        },
        error: (err) => {
          console.error(err);
        }
      });
    }
  }
}
