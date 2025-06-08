TABLE_NAME = "brand_subbrands_log"

CHECK_TABLE_EXISTS = f"""
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'services'
    AND table_name = '{TABLE_NAME}'
);
"""

CREATE_SUBBRANDS_LOG = f"""
CREATE TABLE IF NOT EXISTS services.{TABLE_NAME} (
    brand_id BIGINT,
    domain VARCHAR(255) NOT NULL,
    synonym VARCHAR(255) NOT NULL,
    subbrand_id BIGINT NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW()
);
"""

TRUNCATE_SUBBRANDS_LOG = f"""
TRUNCATE TABLE services.{TABLE_NAME};
"""

INSERT_SUBBRANDS_TO_LOG = f"""
INSERT INTO services.{TABLE_NAME} (brand_id, domain, synonym, subbrand_id)
VALUES (%s, %s, %s, %s);
"""

DROP_SUBBRANDS_LOG = f"""
DROP TABLE IF EXISTS services.{TABLE_NAME};
"""
