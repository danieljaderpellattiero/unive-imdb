DEFINE TABLE IF NOT EXISTS title_akas SCHEMAFULL;
DEFINE FIELD localTitle ON TABLE title_akas TYPE string;
DEFINE FIELD region ON TABLE title_akas TYPE string;
DEFINE FIELD language ON TABLE title_akas TYPE string;
DEFINE FIELD types ON TABLE title_akas TYPE array<string>;
DEFINE FIELD attributes ON TABLE title_akas TYPE array<string>;
DEFINE FIELD isOriginal ON TABLE title_akas TYPE bool;