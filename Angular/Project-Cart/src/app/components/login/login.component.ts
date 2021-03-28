import { AuthService } from '../../services/auth.service';
import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  isSignedIn = false;
  constructor(public auth: AuthService) {}

  login() {
    this.auth.logInWithGoogle();
  }
  
}
