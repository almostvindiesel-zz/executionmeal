drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  first_name text not null,
  drink_non_alcoholic text not null,
  drink_alcoholic text not null,
  appetizer text not null,
  entree text not null,
  side_1 text not null,
  side_2 text not null,
  dessert text not null,
  how_die  text not null,
  image_name text not null
);


