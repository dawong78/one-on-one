import { NumberSymbol } from "@angular/common";

export class Group {

  id: number = -1;
  owner: any = {};
  name: string = "";
  people: any[] = [];

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }

}

export class Person {
  id: number = -1;
  display_name: string = '';
}
