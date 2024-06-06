DEFINE TABLE IF NOT EXISTS name_basics SCHEMAFULL;
DEFINE FIELD primaryName ON TABLE name_basics TYPE string;
DEFINE FIELD birthYear ON TABLE name_basics TYPE number;
DEFINE FIELD deathYear ON TABLE name_basics TYPE option<number>;
DEFINE FIELD primaryProfession ON TABLE name_basics TYPE array<string>;