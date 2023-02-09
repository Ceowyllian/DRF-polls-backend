DROP FUNCTION IF EXISTS create_search_vector;

DROP FUNCTION IF EXISTS question_update_search_vector;

DROP FUNCTION IF EXISTS question_insert_search_vector;

DROP TRIGGER IF EXISTS question_insert_trigger ON polls_question;

DROP TRIGGER IF EXISTS question_update_trigger ON polls_question;
