import { Component, inject, OnInit, signal } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Data } from './data';
import { Group } from './group';
import { Login } from './login/login';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ReactiveFormsModule, Login],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit{
  protected readonly title = signal('one-on-one');
  private dataService = inject(Data)

  groups = signal<any[]>([]);
  member_group_ids: number[] = [];

  new_group_name = new FormControl('');

  ngOnInit(): void {
    this.refresh();
  };

  refresh(): void {
    this.dataService.getGroups().subscribe((data: any[]) => {
      this.groups.set(data)
    });
    this.dataService.getMemberGroupIds().subscribe((data: number[]) => {
      this.member_group_ids = data;
    })
  }

  join_group(): void {
    console.log("join group called");
  }

  async add_group() {
    const newGroup = new Group(this.new_group_name.value);
    this.dataService.addGroup(newGroup).subscribe((data: any) => {
      this.refresh();
    });
  }
}
