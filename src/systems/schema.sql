create table if not exists projects (
    id text primary key,
    name text not null,
    root_path text not null,
    revision integer not null default 0
);

create table if not exists tasks (
    id text primary key,
    project_id text not null,
    title text not null,
    status text not null,
    dependencies_json text not null default '[]',
    foreign key(project_id) references projects(id)
);

create table if not exists events (
    id integer primary key,
    project_id text not null,
    kind text not null,
    payload_json text not null,
    created_at text not null
);
