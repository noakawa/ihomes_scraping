CREATE TABLE `Property` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `link` varchar(255) UNIQUE,
  `sale_or_rent` varchar(255),
  `conditions` varchar(255),
  `type_of_property_id` int,
  `floor_in_building` int,
  `floor` int,
  `rooms` int,
  `built_area` int,
  `furnished` varchar(255),
  `first_listed` datetime,
  `city_id` int
);

CREATE TABLE `Type_of_property` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type` varchar(255) UNIQUE
);

 CREATE TABLE `Price` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `property_id` int,
  `date_of_today` datetime,
  `price` int
);

CREATE TABLE `Cities` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `city_name` varchar(255) UNIQUE
);

ALTER TABLE `Price` ADD FOREIGN KEY (`property_id`) REFERENCES Property(`id`);

ALTER TABLE `Property` ADD FOREIGN KEY (`type_of_property_id`) REFERENCES `Type_of_property` (`id`);

ALTER TABLE `Property` ADD FOREIGN KEY (`city_id`) REFERENCES `Cities` (`id`);
