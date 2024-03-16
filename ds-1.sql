drop table if exists account cascade;
create table account
(
    id       uuid primary key,
    name     text not null,
    password text not null,
    email    text not null
);


drop table if exists document_type cascade;
create table document_type
(
    id          uuid primary key,
    name        text not null,
    description text not null
);

drop table if exists document cascade;
create table document
(
    id               uuid primary key,
    name             text not null,
    description      text not null,
    document_type_id uuid not null references document_type (id) on delete cascade on update cascade,
    account_id       uuid not null references account (id) on delete cascade on update cascade

);

drop table if exists document_process cascade;
create table document_process
(
    id                  uuid primary key,
    initial_document_id uuid  not null references document (id) on delete cascade on update cascade,
    final_document_id   uuid  not null references document (id) on delete cascade on update cascade,
    process_duration    float not null
);


drop table if exists file_document cascade;
create table file_document
(
    id             uuid primary key,
    document_id    uuid  not null references document (id) on delete cascade on update cascade,
    file_name      text  not null,
    file_extension text  not null,
    file_data      bytea not null
);

drop table if exists web_document cascade;
create table web_document
(
    id          uuid primary key,
    document_id uuid not null references document (id) on delete cascade on update cascade,
    web_url     text not null
);

drop table if exists text_document cascade;
create table text_document
(
    id           uuid primary key,
    document_id  uuid not null references document (id) on delete cascade on update cascade,
    text_content text not null
);

drop table if exists event cascade;
create table event
(
    id        uuid primary key,
    dao_id    uuid        not null,
    dao_name  text        not null,
    operation text        not null,
    timestamp timestamptz not null
);

-- populate all table accounts
insert into account (id, name, password, email)
values ('db5adc50-df69-4bd0-b4d0-e300d3ff7560', 'admin', 'admin', 'admin@mail.com'),
       ('db5adc50-df69-4bd0-b4d0-e300d3ff7561', 'user', 'user', 'user@mail.com');


-- populate all table document_types
insert into document_type (id, name, description)
values ('eb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'text', 'text description'),
       ('eb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'file', 'file description'),
       ('eb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'web', 'web description');

-- populate table documents and its sub tables
insert into document (id, name, description, document_type_id, account_id)
values ('fb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'text document', 'text description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560'),
       ('fb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'file document', 'file description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560'),
       ('fb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'web document', 'web description',
        'eb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560');

insert into text_document (id, document_id, text_content)
values ('4c3a1539-df81-4817-a224-05158ce6fd3a', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7560',
        'In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a documents or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available. It is also used to temporarily replace text in a process called greeking, which allows designers to consider the form of a webpage or publication, without the meaning of the text influencing the design. Lorem ipsum is typically a corrupted version of De finibus bonorum et malorum, a 1st-century BC text by the Roman statesman and philosopher Cicero, with words altered, added, and removed to make it nonsensical and improper Latin. Versions of the Lorem ipsum text have been used in typesetting at least since the 1960s, when it was popularized by advertisements for Letraset transfer sheets.[1] Lorem ipsum was introduced to the digital world in the mid-1980s, when Aldus employed it in graphic and word-processing templates for its desktop publishing program PageMaker. Other popular word processors, including Pages and Microsoft Word, have since adopted Lorem ipsum,[2] as have many LaTeX packages,[3][4][5] web content managers such as Joomla! and WordPress, and CSS libraries such as Semantic UI.[6]');
insert into file_document (id, document_id, file_name, file_extension, file_data)
values ('4c3a1539-df81-4817-a224-05158ce6fd3b', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7561', 'file', '.pdf',
        'file_byte_35tv4c36vyv5etrgf');
insert into web_document (id, document_id, web_url)
values ('4c3a1539-df81-4817-a224-05158ce6fd3c', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7562', 'http://www.google.com');

-- populate table document_processes from web documents to file documents
insert into document_process (id, initial_document_id, final_document_id, process_duration)
values ('63624e7e-a1bd-418f-a97d-241490240f1a', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7562',
        'fb5adc50-df69-4bd0-b4d0-e300d3ff7561', 0.1);

-- populate table events
insert into event (id, dao_id, dao_name, operation, timestamp)
values ('3ea947bf-8cf8-43e3-b69c-112b8503f4a0', 'fb5adc50-df69-4bd0-b4d0-e300d3ff7560', 'document',
        'create', now()::timestamptz),
       ('3ea947bf-8cf8-43e3-b69c-112b8503f4a1', '63624e7e-a1bd-418f-a97d-241490240f1a', 'document_process',
        'create', now()::timestamptz),
       ('3ea947bf-8cf8-43e3-b69c-112b8503f4a2', '4c3a1539-df81-4817-a224-05158ce6fd3c', 'web_document',
        'create', now()::timestamptz),
       ('3ea947bf-8cf8-43e3-b69c-112b8503f4a3', '4c3a1539-df81-4817-a224-05158ce6fd3a', 'text_document',
        'create', now()::timestamptz),
       ('3ea947bf-8cf8-43e3-b69c-112b8503f4a4', '4c3a1539-df81-4817-a224-05158ce6fd3b', 'file_document',
        'create', now()::timestamptz),
       ('3ea947bf-8cf8-43e3-b69c-112b8503f4a5', 'db5adc50-df69-4bd0-b4d0-e300d3ff7560', 'account',
        'create', now()::timestamptz);



select *
from document_process
         inner join document as from_document on from_document.id = document_process.initial_document_id
         inner join document as to_document on to_document.id = document_process.final_document_id
         inner join file_document on file_document.document_id = document_process.final_document_id
         inner join web_document on web_document.document_id = document_process.initial_document_id
         inner join document_type as from_document_type on from_document_type.id = from_document.document_type_id
         inner join document_type as to_document_type on to_document_type.id = to_document.document_type_id
         inner join account on account.id = from_document.account_id;


select *
from file_document;


select *
from document d
         inner join document_type dt on dt.id = d.document_type_id
         inner join account a on a.id = d.account_id
         inner join text_document td on d.id = td.document_id
where d.id = 'fb5adc50-df69-4bd0-b4d0-e300d3ff7560';

select *
from document_type;

select *
from account;


select encode(fd.file_data, 'escape'), *
from file_document fd;

select *
from file_document fd;
