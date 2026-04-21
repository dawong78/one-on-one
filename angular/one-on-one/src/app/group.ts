import { NumberSymbol } from "@angular/common";

export class Group {

  id: number = -1;
  name: string|null = "";

  constructor(name: string|null) {
    this.name = name;
  }

}
