CREATE TABLE `Property` (
  `id` int PRIMARY KEY,
  `link` varchar(255),
  `sale_or_rent` varchar(255),
  `condition` varchar(255),
  `type_of_property_id` int,
  `floor_in_building` int,
  `floor` int,
  `rooms` int,
  `built_area` float,
  `furnished` varchar(255),
  `first_listed` datetime,
  `city_id` int
);

CREATE TABLE `Type_of_property` (
  `id` int PRIMARY KEY,
  `type` varchar(255)
);

CREATE TABLE `Price` (
  `id` int PRIMARY KEY,
  `property_id` int,
  `date_of_today` datetime,
  `price` float
);

CREATE TABLE `Cities` (
  `id` int PRIMARY KEY,
  `city_name` varchar(255)
);

ALTER TABLE `Property` ADD FOREIGN KEY (`id`) REFERENCES `Price` (`property_id`);

ALTER TABLE `Property` ADD FOREIGN KEY (`type_of_property_id`) REFERENCES `Type_of_property` (`id`);

ALTER TABLE `Property` ADD FOREIGN KEY (`city_id`) REFERENCES `Cities` (`id`);
