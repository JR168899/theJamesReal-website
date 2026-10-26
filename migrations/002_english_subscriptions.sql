CREATE SCHEMA IF NOT EXISTS jamesreal_mail;
CREATE TABLE IF NOT EXISTS jamesreal_mail.subscribers (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), email text UNIQUE NOT NULL,
 levels text[] NOT NULL CHECK (cardinality(levels) BETWEEN 1 AND 6 AND levels <@ ARRAY['A1','A2','B1','B2','C1','C2']::text[]),
 active boolean NOT NULL DEFAULT false, confirmed_at timestamptz, consent_at timestamptz NOT NULL DEFAULT now(),
 unsubscribe_hash text UNIQUE NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS jamesreal_mail.requests (
 token_hash text PRIMARY KEY, email text NOT NULL, levels text[] NOT NULL,
 expires_at timestamptz NOT NULL, used_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS english_request_email_time ON jamesreal_mail.requests(email,created_at);
CREATE TABLE IF NOT EXISTS jamesreal_mail.deliveries (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), subscriber_id uuid NOT NULL REFERENCES jamesreal_mail.subscribers(id),
 edition_date date NOT NULL, level text NOT NULL CHECK(level IN ('A1','A2','B1','B2','C1','C2')),
 status text NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','sending','sent','failed')),
 provider_id text, attempts int NOT NULL DEFAULT 0, lease_until timestamptz, sent_at timestamptz, last_error text,
 UNIQUE(subscriber_id,edition_date,level)
);
CREATE TABLE IF NOT EXISTS jamesreal_mail.rate_limits (
 request_hash text NOT NULL, hour timestamptz NOT NULL, count int NOT NULL DEFAULT 1,
 PRIMARY KEY(request_hash,hour)
);
COMMENT ON SCHEMA jamesreal_mail IS 'Private opt-in subscriptions. Never export subscriber data to GitHub or public site assets.';
