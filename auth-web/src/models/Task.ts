export interface Task {
    id: number;
    name: string;
    dateSubmitted: Date;
    relationshipType: string;
    relationshipId: number;
    dueDate?: Date;
    type: string;
    status: string;
    relatedTo: number;
}

export interface Tasks {
    tasks: Task []
}
