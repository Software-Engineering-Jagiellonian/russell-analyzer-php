CREATE TABLE IF NOT EXISTS public.php_metrics_project
(
    id BIGSERIAL PRIMARY KEY,
    repository_language_file_id bigint,
    ahh integer,
    andc integer,
    calls integer,
    ccn integer,
    ccn2 integer,
    cloc integer,
    clsa integer,
    clsc integer,
    eloc integer,
    fanout integer,
    leafs integer,
    lloc integer,
    loc integer,
    maxdit integer,
    ncloc integer,
    noc integer,
    nof integer,
    noi integer,
    nom integer,
    nop integer,
    roots integer,
    CONSTRAINT repository_language_file_id FOREIGN KEY (repository_language_file_id)
        REFERENCES public.repository_language_file (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.php_metrics_package
(
    id BIGSERIAL PRIMARY KEY,
    repository_language_file_id bigint,
    cr double precision,
    noc integer,
    nof integer,
    noi integer,
    nom integer,
    rcr double precision,
    CONSTRAINT repository_language_file_id FOREIGN KEY (repository_language_file_id)
        REFERENCES public.repository_language_file (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.php_metrics_class
(
    id BIGSERIAL PRIMARY KEY,
    repository_language_file_id bigint,
    ca integer,
    cbo integer,
    ce integer,
    cis integer,
    cloc integer,
    cr double precision,
    csz integer,
    dit integer,
    eloc integer,
    lloc integer,
    loc integer,
    noam integer,
    nocc integer,
    noom integer,
    ncloc integer,
    nom integer,
    npm integer,
    rcr double precision,
    vars integer,
    varsi integer,
    varsnp integer,
    wmc integer,
    wmci integer,
    wmcnp integer,
    CONSTRAINT repository_language_file_id FOREIGN KEY (repository_language_file_id)
        REFERENCES public.repository_language_file (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.php_metrics_method
(
    id BIGSERIAL PRIMARY KEY,
    repository_language_file_id bigint,
    ccn integer,
    ccn2 integer,
    cloc integer,
    eloc integer,
    hb double precision,
    hd double precision,
    he double precision,
    hi double precision,
    hl double precision,
    hnd integer,
    hnt integer,
    ht double precision,
    hv double precision,
    lloc integer,
    loc integer,
    mi double precision,
    ncloc integer,
    npath integer,
    CONSTRAINT repository_language_file_id FOREIGN KEY (repository_language_file_id)
        REFERENCES public.repository_language_file (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);