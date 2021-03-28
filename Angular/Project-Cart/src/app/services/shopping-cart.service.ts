import { ShoppingCart } from './../models/shopping-cart';
import { AngularFireDatabase, AngularFireObject } from '@angular/fire/database';
import { Injectable } from '@angular/core';
import { Product } from '../models/product';
import { take, map } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ShoppingCartService {

  constructor(private db: AngularFireDatabase) { }

  private create() {
    return this.db.list('/shopping-carts').push({
      dateCreated: new Date().getTime()
    });
  }

  async getCart(): Promise<Observable<ShoppingCart>> {
    let cartId = await this.getOrCreateCartId();
    return this.db.object('/shopping-carts/' + cartId)
      .snapshotChanges().pipe(map(x => new ShoppingCart(x.payload.exportVal().items)));
  }

  private getItem(cartId: string, productId: string) {
    return this.db.object('/shopping-carts/' + cartId + '/items/' + productId);
  }

  private async getOrCreateCartId() {
    let cartId = localStorage.getItem('cartId');
    if (cartId) return cartId;
 
    let result = await this.create();
    localStorage.setItem('cartId', result.key);
    return result.key;
  }

  /*async updateItem(product: Product, change: number) {
    let cartId = await this.getOrCreateCartId();
    let item$: Observable<any> = this.db.object('/shopping-carts/' + cartId + '/items/' + product.key).valueChanges();
    let item$$ = this.db.object('/shopping-carts/' + cartId + '/items/' + product.key);
    item$.pipe(take(1)).subscribe( item => {
       if( item === null ) {
          item$$.set({product: product, quantity: change});
      }else{
          item$$.update({quantity: item.quantity + change});
     }
  });
}*/
/*private async updateItem(product: Product, change: number) {
  let cartId = await this.getOrCreateCartId();
  let item$ = this.getItem(cartId, product.key);
  item$.valueChanges().pipe(take(1)).subscribe(item => {
    let quantity = (item.quantity || 0) + change;
    if (quantity === 0) item$.remove();
    else item$.update({ 
      title: product.title,
      imageUrl: product.imageUrl,
      price: product.price,
      quantity: quantity
    });
  });
}*/
async updateItem(product: Product, change: number) {
  let cartId = await this.getOrCreateCartId();
  let item$: Observable<any> = this.db.object('/shopping-carts/' + cartId + '/items/' + product.key).valueChanges();
  let item$$ = this.db.object('/shopping-carts/' + cartId + '/items/' + product.key);
  item$.pipe(take(1)).subscribe( item => {
     if( item === null ) {
        item$$.set({product: product, quantity: change});
    }else{
        item$$.update({quantity: item.quantity + change});
   }
});
}

  async addToCart(product: Product) {
    this.updateItem(product, 1);
  }
  async removeFromCart(product: Product) {
    this.updateItem(product, -1);
  }
  clearCart() {}

}
