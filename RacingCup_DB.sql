-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Хранимая процедура для входа пользователя
CREATE OR REPLACE FUNCTION login(
    p_login VARCHAR(50),
    p_password VARCHAR(50)
)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM Users 
        WHERE login = p_login AND password = p_password
    );
END;
$$ LANGUAGE plpgsql;

-- Хранимая процедура для регистрации пользователя
CREATE OR REPLACE FUNCTION registration(
    p_login VARCHAR(50),
    p_password VARCHAR(50)
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем, существует ли уже пользователь с таким логином
    IF EXISTS (SELECT 1 FROM Users WHERE login = p_login) THEN
        RETURN FALSE;
    ELSE
        -- Если нет, создаем нового пользователя
        INSERT INTO Users (login, password) VALUES (p_login, p_password);
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;