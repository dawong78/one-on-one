import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Data } from './data';
import { Group, Person } from './group';
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

  currentUser = signal<any>(null);
  people = signal<Person[]>([]);
  groups = signal<any[]>([]);
  memberGroupIds = signal<number[]>([]);
  ownedGroupIds = signal<number[]>([]);

  newGroupName = new FormControl('');

  editGroupForm!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.editGroupForm = this.fb.group({
      selectedGroup: null
    });
    this.refresh();
  };

  refresh(): void {
    this.dataService.getMemberGroupIds().subscribe((data: number[]) => {
      this.memberGroupIds.set(data);
    });
    this.dataService.getOwnedGroupIds().subscribe((data: number[]) => {
      this.ownedGroupIds.set(data);
    });
    this.dataService.getPeople().subscribe((people: any[]) => {
      this.people.set(people);
      this.dataService.getGroups().subscribe((groups: any[]) => {
        this.groups.set(groups);
        // Convert person ids to person objects
        const idToPersonMap: Record<number, any> = {};
        for (let i = 0; i < people.length; i++) {
          idToPersonMap[people[i].id] = people[i];
        }
        for (let igroup = 0; igroup < groups.length; igroup++) {
          let group = groups[igroup]
          if (this.editGroupForm.value.selectedGroup) {
            if (this.editGroupForm.value.selectedGroup.id == group.id) {
              this.editGroupForm.value.selectedGroup = group;
            }
          }
          let newPeople = [];
          if (group.people) {
            for (let iperson = 0; iperson < group.people.length; iperson++) {
              newPeople.push(idToPersonMap[group.people[iperson]]);
            }
          }
          group.people = newPeople;
        }
      });
    })
    this.dataService.getCurrentUser().subscribe((data: any) => {
      this.currentUser.set(data);
    })
  }

  join_group(): void {
    console.log("join group called");
  }

  async addGroup() {
    const newGroup = new Group(-1, this.newGroupName.value ?? 'UNNAMED');
    console.log("current user: " + this.currentUser());
    newGroup.owner = this.currentUser().id;
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

  availablePeopleForGroup(group: any) {
    const groupMemberIds = new Set();
    for (let i = 0; i < group?.people.length; i++) {
      let person = group.people[i];
      groupMemberIds.add(person.id);
    }
    const availablePeople: any[] = [];
    const allPeople = this.people();
    for (let i = 0; i < allPeople.length; i++) {
      let person = allPeople[i];
      if (!groupMemberIds.has(person.id)) {
        availablePeople.push(person);
      }
    }
    return availablePeople;
  }

  addPersonToEditGroup(person: any) {
    const group = this.editGroupForm.value.selectedGroup;
    if (!group) {
      return;
    }
    const restGroup = new Group(group.id, group.name);
    console.log("adding to group");
    console.log(group)
    const id_to_person_map = new Map<number, any>();
    for (let i = 0; i < this.people.length; i++) {
      id_to_person_map.set(this.people()[i].id, this.people()[i]);
    }
    restGroup.owner = group.owner;
    restGroup.people = [];
    if (group.people) {
      for (let i = 0; i < group.people.length; i++) {
        restGroup.people.push(group.people[i].id);
      }
    }
    restGroup.people.push(person.id);
    console.log("add person to group");
    console.log(restGroup);
    this.dataService.updateGroup(restGroup).subscribe({
      next: (data) => this.refresh()
    });
  }

  removePersonFromEditGroup(person: any) {
    const group = this.editGroupForm.value.selectedGroup;
    if (!group) {
      return;
    }
    if (!group.people) {
      group.people = [];
    }
    group.people = group.people.filter((p: any) => p.id === person.id);
    this.dataService.updateGroup(group).subscribe({
      next: (data) => this.refresh()
    });
  }
}
