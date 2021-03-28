import { SellComponent } from './components/sell/sell.component';
import { CartComponent } from './components/cart/cart.component';
import { HomeComponent } from './components/home/home.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CheckOutComponent } from './components/check-out/check-out.component';
import { ContactComponent } from './components/contact/contact.component';
import { LoginComponent } from './components/login/login.component';
import { OrderSucessComponent } from './components/order-sucess/order-sucess.component';
import { TeamComponent } from './components/team/team.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'projects', component: HomeComponent},
  { path: 'sell', component: SellComponent},
  { path: 'team', component: TeamComponent}, 
  { path: 'contact', component: ContactComponent},
  { path: 'login', component: LoginComponent},
  { path: 'cart', component: CartComponent},

  { path: 'check-out', component: CheckOutComponent, canActivate: [AuthGuard]},
  { path: 'order-sucess', component: OrderSucessComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
