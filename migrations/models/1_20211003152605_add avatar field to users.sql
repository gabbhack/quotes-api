-- upgrade --
ALTER TABLE "users" ADD "avatar" TEXT;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "avatar";
