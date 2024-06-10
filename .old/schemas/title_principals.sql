DEFINE TABLE IF NOT EXISTS title_principals SCHEMAFULL;
DEFINE FIELD person ON TABLE title_principals TYPE record<name_basics>;
DEFINE FIELD category ON TABLE title_principals TYPE string;
DEFINE FIELD job ON TABLE title_principals TYPE option<string>;
DEFINE FIELD characters ON TABLE title_principals TYPE option<array<string>>;