create table Airline(
    airline_name varchar(50),
    primary key(airline_name));

create table airplane(
    id_num varchar(50),
    airline_name varchar(50),
    num_seat int,
    primary key(id_num,airline_name),
    foreign key(airline_name) references Airline(airline_name));

create table airport(
    code varchar(20),
    name varchar(50),
    city varchar(50),
    primary key(code));

create table flight(
    airline_name varchar(50),
    flight_num varchar(20),
    depature_date varchar(20),
    depature_time varchar(10),
    depature_airport varchar(20),
    arrival_date varchar(20),
    arrival_time varchar(10),
    arrival_airport varchar(20),
    base_price float(3),
    id_num varchar(50),
    flight_status varchar(20),
    primary key(airline_name,flight_num,depature_date,depature_time),
    foreign key (airline_name) references airline(airline_name),
    foreign key (id_num) references airplane(id_num),
    foreign key (depature_airport) references airport(code),
    foreign key (arrival_airport) references airport(code));

create table staff(
    user_name varchar(50),
    staff_password varchar(50),
    first_name varchar(50),
    last_name varchar(50),
    date_of_birth varchar(20),
    airline_name varchar(50),
    primary key(user_name),
    foreign key(airline_name) references airline(airline_name));

create table staff_phone(
    user_name varchar(50),
    staff_phone varchar(20),
    primary key(user_name,staff_phone),
    foreign key(user_name) references staff(user_name));

create table customer(
    email varchar(50),
    name varchar(50),
    customer_password varchar(50),
    building_num varchar(10),
    street varchar(50),
    city varchar(30),
    state varchar(30),
    customer_phone varchar(20),
    passport_num varchar(20),
    passport_exp varchar(20),
    passport_country varchar(20),
    date_of_birth varchar(20),
    primary key(email));
    
create table ticket(
    ticket_id bigint not null auto_increment,
    email varchar(50),
    airline_name varchar(50),
    flight_num varchar(20),
    depature_date varchar(20),
    depature_time varchar(10),
    primary key(ticket_id),
    foreign key(email) references customer(email),
    foreign key (airline_name,flight_num,depature_date,depature_time) references flight(airline_name,flight_num,depature_date,depature_time));

create table purchase(
    ticket_id bigint,
    email varchar(50),
    card_type varchar(10),
    card_num varchar(30),
    name_on varchar(50),
    exp_card varchar(20),
    p_datetime timestamp default current_timestamp,
    sold_price float(3),
    primary key(ticket_id,email),
    foreign key(ticket_id) references ticket(ticket_id),
    foreign key(email) references customer(email));
    
create table comment_rate(
    email varchar(50),
    airline_name varchar(50),
    flight_num varchar(20),
    depature_date varchar(20),
    depature_time varchar(10),
    rate numeric(2,1),
    comment varchar(300),
    primary key(email,airline_name,flight_num,depature_date,depature_time),
    foreign key(email) references customer(email),
    foreign key(airline_name,flight_num,depature_date,depature_time) references flight(airline_name,flight_num,depature_date,depature_time));
    