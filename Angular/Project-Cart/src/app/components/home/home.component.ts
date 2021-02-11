import { Subscription } from 'rxjs';
import { ShoppingCartService } from './../../services/shopping-cart.service';
import { CategoryService } from './../../services/category.service';
import { ActivatedRoute } from '@angular/router';
import { ProductService } from './../../services/product.service';
import { Component, Input, OnDestroy, OnInit} from '@angular/core';
import { Product } from './../../models/product';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy{

  @Input('product') product: Product;
  @Input('show-actions') showActions = true;

  products: Product[] = [];
  filteredProducts: Product[] = [];
  category: string;
  categories$; 
  cart: any;
  subscription: Subscription

  constructor(
    public productService: ProductService,
    public categoryService: CategoryService,
    public cartService: ShoppingCartService, 
    private shoppingCartService: ShoppingCartService,
    public route: ActivatedRoute) { }

  addToCart(product: Product) {
    this.cartService.addToCart(product);
  }

  async ngOnInit() {
    this.categories$ = this.categoryService.getAllCategories();

    this.productService.getAllProducts().subscribe(products => {
      this.products = products;
      this.route.queryParamMap.subscribe(params => {
        this.category = params.get('category');
  
        this.filteredProducts = (this.category) ?
          this.products.filter(p => p.category === this.category) :
          this.products;
      });
    });

    this.subscription = (await this.shoppingCartService.getCart())
      .subscribe(cart => this.cart = cart);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
    
}