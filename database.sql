drop table if exists account cascade;
create table account
(
    id         uuid primary key,
    name       text      not null,
    password   text      not null,
    email      text      not null,
    created_at timestamp not null,
    updated_at timestamp not null
);


drop table if exists document_type cascade;
create table document_type
(
    id          uuid primary key,
    name        text      not null,
    description text      not null,
    created_at  timestamp not null,
    updated_at  timestamp not null
);

drop table if exists document cascade;
create table document
(
    id               uuid primary key,
    name             text      not null,
    description      text      not null,
    document_type_id uuid      not null references document_type (id) on delete cascade on update cascade,
    account_id       uuid      not null references account (id) on delete cascade on update cascade,
    created_at       timestamp not null,
    updated_at       timestamp not null
);

drop table if exists document_process cascade;
create table document_process
(
    id               uuid primary key,
    from_document_id uuid      not null references document (id) on delete cascade on update cascade,
    to_document_id   uuid      not null references document (id) on delete cascade on update cascade,
    created_at       timestamp not null,
    updated_at       timestamp not null
);


drop table if exists file_document cascade;
create table file_document
(
    id             uuid primary key,
    document_id    uuid      not null references document (id) on delete cascade on update cascade,
    file_name      text      not null,
    file_extension text      not null,
    file_byte      bytea     not null,
    created_at     timestamp not null,
    updated_at     timestamp not null
);

drop table if exists web_document cascade;
create table web_document
(
    id          uuid primary key,
    document_id uuid      not null references document (id) on delete cascade on update cascade,
    web_url     text      not null,
    created_at  timestamp not null,
    updated_at  timestamp not null
);

drop table if exists text_document cascade;
create table text_document
(
    id           uuid primary key,
    document_id  uuid      not null references document (id) on delete cascade on update cascade,
    text_content text      not null,
    created_at   timestamp not null,
    updated_at   timestamp not null
);

-- populate all table account
insert into account (id, name, password, email, created_at, updated_at)
values
    ('db5adc50-df69-4bd0-b4d0-e300d3ff7560', 'admin', 'admin', 'admin@mail.com',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz),
    ('db5adc50-df69-4bd0-b4d0-e300d3ff7561', 'user', 'user', 'user@mail.com',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);


-- populate all table document_type
insert into document_type (id, name, description, created_at, updated_at)
values
    ('eb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'text', 'text description', timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz),
    ('eb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'file', 'file description', timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz),
    ('eb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'web', 'web description', timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);

-- populate table document and its sub tables
insert into document (id, name, description, document_type_id, account_id, created_at, updated_at)
values
    ('fb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'text document', 'text description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz),
    ('fb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'file document', 'file description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz),
    ('fb5adc50-df69-4bd0-b4d0-e300d3ff7563', 'web document', 'web description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);

insert into text_document (id, document_id, text_content, created_at, updated_at)
values ('4c3a1539-df81-4817-a224-05158ce6fd3a', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'text @123',
        timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);
insert into file_document (id, document_id, file_name, file_extension, file_byte, created_at, updated_at)
values ('4c3a1539-df81-4817-a224-05158ce6fd3b', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'file', 'pdf',
        'file_byte_35tv4c36vyv5etrgf', timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);
insert into web_document (id, document_id, web_url, created_at, updated_at)
values ('4c3a1539-df81-4817-a224-05158ce6fd3c', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7563', 'http://www.google.com',
        timezone('Asia/Jakarta', now())::timestamptz, timezone('Asia/Jakarta', now())::timestamptz);

-- populate table document_process from web document to file document
insert into document_process (id, from_document_id, to_document_id, created_at, updated_at)
values ('63624e7e-a1bd-418f-a97d-241490240f1a', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7563',
        'fb5adc50-df69-4bd0-b4d0-e300d3ff7562', timezone('Asia/Jakarta', now())::timestamptz,
        timezone('Asia/Jakarta', now())::timestamptz);



select *
from document_process
         inner join document as from_document on from_document.id = document_process.from_document_id
         inner join document as to_document on to_document.id = document_process.to_document_id
         inner join file_document on file_document.document_id = document_process.to_document_id
         inner join web_document on web_document.document_id = document_process.from_document_id
         inner join document_type as from_document_type on from_document_type.id = from_document.document_type_id
         inner join document_type as to_document_type on to_document_type.id = to_document.document_type_id
         inner join account on account.id = from_document.account_id;


select * from account