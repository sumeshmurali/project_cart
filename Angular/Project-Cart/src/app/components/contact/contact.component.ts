import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {
;
  constructor() { }

  ngOnInit(): void {
  }
  submit(contactForm: NgForm){
    console.log(contactForm.value);
    contactForm.reset();
  }
}