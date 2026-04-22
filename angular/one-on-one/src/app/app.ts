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
export class App implements OnInit {
  protected readonly title = signal('one-on-one');
  private dataService = inject(Data)

  groups = signal<any[]>([]);
  memberGroupIds = signal<number[]>([]);
  ownedGroupIds = signal<number[]>([]);

  newGroupName = new FormControl('');

  ngOnInit(): void {
    this.refresh();
  };

  refresh(): void {
    this.dataService.getGroups().subscribe((data: any[]) => {
      this.groups.set(data);
      this.dataService.getMemberGroupIds().subscribe((data: number[]) => {
        this.memberGroupIds.set(data);
      });
      this.dataService.getOwnedGroupIds().subscribe((data: number[]) => {
        this.ownedGroupIds.set(data);
      });
    });
  }

  join_group(): void {
    console.log("join group called");
  }

  async addGroup() {
    const newGroup = new Group(this.newGroupName.value);
    this.dataService.addGroup(newGroup).subscribe((data: any) => {
      this.refresh();
    });
  }

  removeGroup(groupId: number) {
    this.dataService.removeGroup(groupId).subscribe((data: any) => {
      this.refresh();
    });
  }

  resetGroup(groupId: number) {
    this.dataService.resetGroup(groupId).subscribe((data: any) => {
      this.refresh();
    })
  }

  matchGroup(groupId: number) {
    this.dataService.matchGroup(groupId).subscribe((data: any) => {
      this.refresh();
    })
  }
}
