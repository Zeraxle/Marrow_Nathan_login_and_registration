from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('login_validation_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL('login_validation_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users(first_name, last_name, email, password) 
                VALUES(%(first_name)s,%(last_name)s,%(email)s, %(password)s);
                """
        result = connectToMySQL('login_validation_schema').query_db(query,data)
        return result
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('login_validation_schema').query_db(query, user)
        if len(results) >= 1:
            flash('Email is taken.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email', 'register')
            is_valid = False
        if len('first_name') < 3:
            flash('First name must be at least 3 characters', 'register')
            is_valid = False
        if len('last_name') < 3:
            flash('Last name must be at least 3 characters', 'register')
            is_valid = False
        if len(user['password']) < 9:
            flash('Password length must be at least 8 characters', 'register')
            is_valid = False
        if len(user['password']) != user['password_confirm']:
            flash('Password must match', 'register')
            is_valid = False
        return is_valid
    
