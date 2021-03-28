import { AuthService } from '../services/auth.service';
import { Injectable } from '@angular/core';
import { CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(public auth: AuthService, public router: Router) {}

  canActivate(route: any, state: RouterStateSnapshot) {
      return this.auth.user$.pipe(map(user => {
        if(user) return true;
        
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url }});
        return false;
      }));
    }
}