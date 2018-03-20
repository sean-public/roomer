BEGIN;

--
-- Create model Doorway
--
CREATE TABLE "web_api_doorway" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL);
--
-- Create model DPU
 --
CREATE TABLE "web_api_dpu" ("id" integer unsigned NOT NULL PRIMARY KEY, "active" bool NOT NULL, "name" varchar(100) NOT NULL, "doorway_id" integer NULL REFERENCES "web_api_doorway" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Occupancy
--
CREATE TABLE "web_api_occupancy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "timestamp" datetime NOT NULL, "count" smallint unsigned NOT NULL);
--
-- Create model Space
--
CREATE TABLE "web_api_space" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "active" bool NOT NULL);
--
-- Add field space to occupancy
--
ALTER TABLE "web_api_occupancy" RENAME TO "web_api_occupancy__old";
CREATE TABLE "web_api_occupancy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "timestamp" datetime NOT NULL, "count" smallint unsigned NOT NULL, "space_id" integer NOT NULL REFERENCES "web_api_space" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "web_api_occupancy" ("id", "timestamp", "count", "space_id") SELECT "id", "timestamp", "count", NULL FROM "web_api_occupancy__old";
DROP TABLE "web_api_occupancy__old";
CREATE INDEX "web_api_dpu_doorway_id_4ad7f601" ON "web_api_dpu" ("doorway_id");
CREATE INDEX "web_api_occupancy_space_id_506a10a9" ON "web_api_occupancy" ("space_id");
--
-- Add field entering_to to doorway
--
ALTER TABLE "web_api_doorway" RENAME TO "web_api_doorway__old";
CREATE TABLE "web_api_doorway" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "entering_to_id" integer NOT NULL REFERENCES "web_api_space" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "web_api_doorway" ("id", "name", "entering_to_id") SELECT "id", "name", NULL FROM "web_api_doorway__old";
DROP TABLE "web_api_doorway__old";
CREATE INDEX "web_api_doorway_entering_to_id_db0e4b35" ON "web_api_doorway" ("entering_to_id");
--
-- Add field exiting_to to doorway
--
ALTER TABLE "web_api_doorway" RENAME TO "web_api_doorway__old";
CREATE TABLE "web_api_doorway" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "entering_to_id" integer NOT NULL REFERENCES "web_api_space" ("id") DEFERRABLE INITIALLY DEFERRED, "exiting_to_id" integer NOT NULL REFERENCES "web_api_space" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "web_api_doorway" ("id", "name", "entering_to_id", "exiting_to_id") SELECT "id", "name", "entering_to_id", NULL FROM "web_api_doorway__old";
DROP TABLE "web_api_doorway__old";
CREATE INDEX "web_api_doorway_entering_to_id_db0e4b35" ON "web_api_doorway" ("entering_to_id");
CREATE INDEX "web_api_doorway_exiting_to_id_d822b5d6" ON "web_api_doorway" ("exiting_to_id");
--
-- Create index web_api_occ_space_i_a0ba15_idx on field(s) space of model occupancy
--
CREATE INDEX "web_api_occ_space_i_a0ba15_idx" ON "web_api_occupancy" ("space_id");
--
-- Create index web_api_occ_timesta_55dd9b_idx on field(s) timestamp of model occupancy
--
CREATE INDEX "web_api_occ_timesta_55dd9b_idx" ON "web_api_occupancy" ("timestamp");
--
-- Alter unique_together for occupancy (1 constraint(s))
--
CREATE UNIQUE INDEX web_api_occupancy_space_id_timestamp_fff4fefb_uniq ON "web_api_occupancy" ("space_id", "timestamp");
--
-- Add an "outside" space that we will always assume exists in the DB for external doorways.
--
INSERT INTO "web_api_space" ("name", "active") VALUES ("outside", 1);

COMMIT;
 