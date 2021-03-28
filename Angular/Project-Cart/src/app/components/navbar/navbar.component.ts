import { ShoppingCartService } from './../../services/shopping-cart.service';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, Observable } from 'rxjs';
import { AppUser } from 'src/app/models/app-user';
import { Product } from 'src/app/models/product';
import { AuthService } from 'src/app/services/auth.service';
import { ProductService } from 'src/app/services/product.service';
import { ShoppingCart } from 'src/app/models/shopping-cart';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {

  appUser: AppUser | undefined;
  products: Product[];
  filteredProducts: any[];
  subscription: Subscription;
  cart$: Observable<ShoppingCart>;

  constructor(private auth: AuthService, 
              private productService: ProductService,
              private shoppingCartService: ShoppingCartService) {}

  logout(){
    this.auth.logOutWithGoogle();
  }

  filter(query: string) {
    this.filteredProducts = (query) ?
      this.products.filter(p => p.title.toLowerCase().includes(query.toLowerCase())) :
      this.products;
  }

  async ngOnInit() {
    this.auth.appUser$.subscribe(appUser => this.appUser = appUser); 

    this.subscription = this.productService.getAllProducts()
      .subscribe(products => this.filteredProducts= this.products = products);

    this.cart$ = await (await this.shoppingCartService.getCart());
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

}
