create table users
(
    id              serial  not null
        constraint users_pk
            primary key,
    username        varchar not null,
    password        varchar not null,
    mobile_password varchar not null,
    old_method      boolean default false,
    must_update     boolean default false
);

comment on table users is 'Holds login information for users.';

comment on column users.mobile_password is 'On mobile devices password _might_ have the first character if it''s a letter be uppercase.';

alter table users
    owner to root;

INSERT INTO public.users (id, username, password, mobile_password, old_method, must_update) VALUES (1, 'asdf', 'DAgBEAagZBxeEH3WPF/JLW07aGf9W59loHfyrDpaHoO3Pu3M3whTgsGRyefW4/I6UhJiSw==', 'DAgBEDNyyoUQTAh3ILjbKIMxJEhzApxd5SkNRRozpg/USaWdMTAtQgEER3QV1CuzHSWxMA==', false, false);
INSERT INTO public.users (id, username, password, mobile_password, old_method, must_update) VALUES (2, 'jimmy', 'DAgBEIXFCrh5ijvsmZcZ+M8+//OTBeEA5gp/LI87CVqnSs84eWEMs9gfLpAeghzegh9R3w==', 'DAgBEHOPc80zdHGFZjg6LLjoi18sydo7Y2cfoXLvlvZEmsajKnolhVmbaICLsq6h0iILDA==', false, false);
INSERT INTO public.users (id, username, password, mobile_password, old_method, must_update) VALUES (3, 'jimmy1', 'DAgBEF2ciCUhwQEf5qQORjOl2j/A+1Mfm2InM6H1pb+7UIF98HlsYnQ6F8vYF7hWtjQC2Q==', 'DAgBEDmk0tKfQ9H/HFIPm6+YvseVOnA7hBYtuJbzFNAif+M5+pjtTLYy6S50qO2kEBM6mw==', false, false);
INSERT INTO public.users (id, username, password, mobile_password, old_method, must_update) VALUES (4, 'jimmy2', 'DAgBEDE5ahJc/vrpEPGVoYFIvcepGvC+5QxvFNJFr4Iaw8No4W48QLp2eBVOb12sgGbYcw==', 'DAgBENcGbHkOm4FCNqS/BxF+dUivsLtBhovuCNkBynDD8PSUALquZBNmP9mRyjFM69aBdA==', false, false);