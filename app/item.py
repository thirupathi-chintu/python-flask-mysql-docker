from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from connection import connection

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="wajib"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item

        return {'message': 'Item not found'}, 404


    @classmethod
    def find_by_name(cls, name):
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=%s"
        cursor.execute(query, (name,))
        row = cursor.fetchone()

        if row:
            return {'item': {'name': row[1],'price': row[2]}}

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "an name '{}' has been exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name,'price': data['price']}

        try:
            self.insert(item)
        except TypeError as e:
            print(e)
            return {'message': e}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (NULL, %s, %s)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()

    @jwt_required()
    def delete(self, name):

        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=%s"
        cursor.execute(query, (name,))
        connection.commit()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:

            try:
                self.insert(updated_item)
            except:
                return {"message": "an error"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "an error"}, 500

        return updated_item

    @classmethod
    def update(cls, item):
        cursor = connection.cursor()
        query = "UPDATE items SET price=%s WHERE name=%s"
        cursor.execute(query, (item['price'],item['name']))
        connection.commit()


class ItemList(Resource):

    @jwt_required()
    def get(self):
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        cursor.execute(query)
        result = cursor.fetchall()
        items = []

        for row in result:
            items.append({'name': row[1], 'price': row[2]})

        connection.commit()

        return {"items": items}
