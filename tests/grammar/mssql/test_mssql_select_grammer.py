import unittest
from src.masonite.orm.grammar.mssql_grammar import MSSQLGrammar
from src.masonite.orm.builder.QueryBuilder import QueryBuilder
from src.masonite.orm.grammar.GrammarFactory import GrammarFactory


class TestMSSQLSelectGrammar(unittest.TestCase):
    def setUp(self):
        self.builder = QueryBuilder(
            GrammarFactory.make("mssql"),
            table="users",
            connection_details={
                "database": "rothco_ll",
                "username": "root",
                "password": "",
                "prefix": "dbo.",
            },
        )

    def test_can_compile_select(self):
        to_sql = self.builder.to_sql()
        sql = "SELECT * FROM [dbo.users]"
        self.assertEqual(to_sql, sql)

    def test_can_compile_with_columns(self):
        to_sql = self.builder.select("username", "password").to_sql()
        sql = "SELECT [username], [password] FROM [dbo.users]"
        self.assertEqual(to_sql, sql)

    def test_can_compile_with_where(self):
        to_sql = self.builder.select("username", "password").where("id", 1).to_sql()
        sql = "SELECT [username], [password] FROM [dbo.users] WHERE [id] = '1'"
        self.assertEqual(to_sql, sql)

    def test_can_compile_with_several_where(self):
        to_sql = (
            self.builder.select("username", "password")
            .where("id", 1)
            .where("username", "joe")
            .to_sql()
        )
        sql = "SELECT [username], [password] FROM [dbo.users] WHERE [id] = '1' AND [username] = 'joe'"
        self.assertEqual(to_sql, sql)

    def test_can_compile_with_several_where_and_limit(self):
        to_sql = (
            self.builder.select("username", "password")
            .where("id", 1)
            .where("username", "joe")
            .limit(10)
            .to_sql()
        )
        sql = "SELECT TOP 10 [username], [password] FROM [dbo.users] WHERE [id] = '1' AND [username] = 'joe'"
        self.assertEqual(to_sql, sql)
