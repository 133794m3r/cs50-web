create table reviews
(
    id            serial   not null
        constraint reviews_pkey
            primary key,
    review_score  smallint not null,
    review_text   varchar,
    reviewed_time timestamp default CURRENT_TIMESTAMP,
    isbn          varchar  not null,
    user_id       integer  not null
);

alter table reviews
    owner to root;

INSERT INTO public.reviews (id, review_score, review_text, reviewed_time, isbn, user_id) VALUES (0, 5, 'This is a test review.', '2020-06-18 23:31:05.635728', '1451648537', 1);
INSERT INTO public.reviews (id, review_score, review_text, reviewed_time, isbn, user_id) VALUES (1, 5, 'i am leaving a simple review.', '2020-06-19 17:49:20.998963', '0743231511', 2);
INSERT INTO public.reviews (id, review_score, review_text, reviewed_time, isbn, user_id) VALUES (2, 3, 'I don''t care for the style of writing.', '2020-06-19 18:06:44.967942', '1451648537', 3);
INSERT INTO public.reviews (id, review_score, review_text, reviewed_time, isbn, user_id) VALUES (3, 5, 'I LOVE THIS BOOK SO MUCH!', '2020-06-19 18:16:26.256359', '0375868704', 4);