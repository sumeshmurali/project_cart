import { UserService } from './user.service';
import { AppUser } from './../models/app-user';
import { Injectable } from '@angular/core';
import { AngularFireAuth } from "@angular/fire/auth";
import { ActivatedRoute } from '@angular/router';
import app from 'firebase/app';
import 'firebase/auth';
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable()

export class AuthService {

  user$: Observable<app.User | null>;

  constructor(public afAuth: AngularFireAuth, private route: ActivatedRoute, private userService: UserService) { 
    this.user$ = afAuth.authState;
  }

  logInWithGoogle(){
  let returnUrl = this.route.snapshot.queryParamMap.get('returnUrl') || '/';
  localStorage.setItem('returnUrl', returnUrl);

  this.afAuth.signInWithRedirect(new app.auth.GoogleAuthProvider());
  }

  logOutWithGoogle() {
    this.afAuth.signOut();  
  }

  get appUser$() : Observable<AppUser> { 
    return this.user$.pipe(switchMap(user => {
      if(user) return this.userService.get(user.uid);

      return of(null);
    } ));
  }
}