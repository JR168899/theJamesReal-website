CREATE SCHEMA IF NOT EXISTS jamesreal_content;
CREATE TABLE IF NOT EXISTS jamesreal_content.editions (
 edition_date date NOT NULL,
 kind text NOT NULL CHECK(kind IN ('english','recipes','legacy_english','health')),
 level text NOT NULL DEFAULT '',
 payload jsonb NOT NULL,
 source_sha256 text NOT NULL,
 prepared_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY (edition_date,kind,level)
);
CREATE INDEX IF NOT EXISTS editions_kind_date_idx ON jamesreal_content.editions(kind,edition_date DESC);
COMMENT ON SCHEMA jamesreal_content IS 'Prepared James Real content. No runtime generation, public static exports contain no subscriber information.';
