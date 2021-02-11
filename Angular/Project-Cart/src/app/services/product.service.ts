import { Injectable } from '@angular/core';
import { AngularFireDatabase } from '@angular/fire/database';
import { map } from 'rxjs/operators';
import { Product } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  
  constructor(private db: AngularFireDatabase) { }

  getAllProducts() {
    return this.db.list<Product>('/products').snapshotChanges().pipe(
      map(actions =>
        actions.map(a => ({ 
          key: a.key, 
          title: a.payload.val().title,
          price: a.payload.val().price,
          category: a.payload.val().category,
          imageUrl: a.payload.val().imageUrl}))
      )
    );
  }

}