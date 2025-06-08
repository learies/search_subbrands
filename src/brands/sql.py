GET_CHAIN_BRANDS = """
SELECT
    b.id,
    b."name",
    bd.domain_id,
    d."domain",
    bs.synonym_id,
    s.synonym,
    b.actual_count
FROM
    brand.brand_domains bd
JOIN
    meta.domains d
    ON d.id = bd.domain_id
JOIN
    brand.brand_synonyms bs
    ON bs.brand_id = bd.brand_id
JOIN
    meta.synonyms s
    ON s.id = bs.synonym_id
JOIN
    brand.brands b
    ON b.id = bd.brand_id
    AND b.is_active = TRUE
    AND b.is_chain = TRUE
    AND b.actual_count > 0
ORDER BY
    b.actual_count DESC
"""

MERGE_SUBBRANDS = """
DO $$
DECLARE
    target_brand_id INT := {brand_id};
    subbrand_ids INT[] := ARRAY[{subbrand_ids}];
    subbrand_id INT;
BEGIN
    FOREACH subbrand_id IN ARRAY subbrand_ids
    LOOP

        -- brand_domains
        INSERT INTO brand.brand_domains (brand_id, domain_id)
        SELECT target_brand_id AS brand_id, domain_id
        FROM brand.brand_domains
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_normalized_urls
        INSERT INTO brand.brand_normalized_urls (brand_id, normalized_url_id)
        SELECT target_brand_id AS brand_id, normalized_url_id
        FROM brand.brand_normalized_urls
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_synonyms
        INSERT INTO brand.brand_synonyms (brand_id, synonym_id)
        SELECT target_brand_id AS brand_id, synonym_id
        FROM brand.brand_synonyms
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_phones
        INSERT INTO brand.brand_phones (brand_id, phone_id)
        SELECT target_brand_id AS brand_id, phone_id
        FROM brand.brand_phones
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_emails
        INSERT INTO brand.brand_emails (brand_id, email_id)
        SELECT target_brand_id AS brand_id, email_id
        FROM brand.brand_emails
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_countries
        INSERT INTO brand.brand_countries (brand_id, country_id)
        SELECT target_brand_id AS brand_id, country_id
        FROM brand.brand_countries
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_source_categories
        INSERT INTO brand.brand_source_categories (brand_id, source_category_id)
        SELECT target_brand_id AS brand_id, source_category_id
        FROM brand.brand_source_categories
        WHERE brand_id = subbrand_id
        ON CONFLICT DO NOTHING;

        -- brand_organizations
        UPDATE brand.brand_organizations
        SET brand_id = target_brand_id, updated = NOW()
        WHERE brand_id = subbrand_id;

        -- update subbrand_id
        UPDATE brand.brands
        SET
            is_active = FALSE,
            updated = NOW(),
            actual_count = 0,
            parent_brand_id = target_brand_id
        WHERE id = subbrand_id;

    END LOOP;
END $$;
"""
