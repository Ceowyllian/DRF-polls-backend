DROP TRIGGER IF EXISTS question_insert_trigger ON polls_question;
DROP TRIGGER IF EXISTS question_update_trigger ON polls_question;

CREATE OR REPLACE FUNCTION create_search_vector(_title text, _text text)
    RETURNS tsvector
    LANGUAGE plpgsql AS
$$
BEGIN
    RETURN setweight(to_tsvector(coalesce(_title, '')), 'A') ||
           setweight(to_tsvector(coalesce(_text, '')), 'B');
END;
$$;

CREATE OR REPLACE FUNCTION question_update_search_vector()
    RETURNS TRIGGER
    LANGUAGE plpgsql AS
$$
BEGIN
    UPDATE polls_questionvector
    SET title_and_text = create_search_vector(NEW.title, NEW.text)
    WHERE question_id = NEW.id;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION question_insert_search_vector()
    RETURNS TRIGGER
    LANGUAGE plpgsql AS
$$
BEGIN
    INSERT INTO polls_questionvector (question_id, title_and_text)
    VALUES (NEW.id, create_search_vector(NEW.title, NEW.text));
    RETURN NEW;
END;
$$;

CREATE TRIGGER question_update_trigger
    AFTER UPDATE OF "title", "text"
    ON polls_question
    FOR EACH ROW
EXECUTE PROCEDURE question_update_search_vector();

CREATE TRIGGER question_insert_trigger
    AFTER INSERT
    ON polls_question
    FOR EACH ROW
EXECUTE PROCEDURE question_insert_search_vector();
