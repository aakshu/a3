# import modules to run server
from concurrent import futures
import grpc
import library_pb2
import library_pb2_grpc

# import Genre to utilize in the database
from library_pb2 import Genre

# Books Database - A temporary dictionary to emulate database
books = {
    "1000": {
        "title": "Harry Potter 3",
        "author": "JK Rowling",
        "genre": Genre.THRILLER,
        "publishing_year": 2004
    },
    "1001": {
        "title": "Percy Jackson",
        "author": "Rick Riordan",
        "genre": Genre.ROMANCE,
        "publishing_year": 2003
    }
}

# Servicer class to create and run the server
class InventoryServicer(library_pb2_grpc.InventoryServicer):

    # function to create a book and add it to the database
    def CreateBook(self, request, context):
        # print out request received
        print("CreateBook request received:")
        print(request)

        # create new book object to add to the database
        new_book = {}
        new_book["title"] = request.title
        new_book["author"] = request.author
        new_book["genre"] = request.genre
        new_book["publishing_year"] = request.publishing_year

        # validate that the isbn is unique and doesn't already exist in the database
        if request.isbn not in books.keys():
            # add book to the DB since isbn is valid
            books[request.isbn] = new_book
            # create isbn object to return to the client
            isbn_object = library_pb2.ISBN(isbn=request.isbn)
        else:
            # if isbn is not valid, throw error to client
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('The isbn provided already exists in the database')
            return library_pb2.ISBN()

        # return the isbn to the client
        return isbn_object

    # function to retrieve book details based on isbn provided
    def GetBook(self, request, context):
        # print out request received
        print("GetBook request received:")
        print(request)

        # if isbn is not valid, throw error to client
        if request.isbn not in books.keys():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('The isbn provided does not exist in the database')
            return library_pb2.Book()

        # if isbn is valid, return the queried book
        queried_book = books[request.isbn]
        response = library_pb2.Book(isbn=request.isbn, title=queried_book["title"], author=queried_book["author"], genre=queried_book["genre"], publishing_year=queried_book["publishing_year"])
        return response

# function to start and run server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_InventoryServicer_to_server(InventoryServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

# run the server when script is run
if __name__ == "__main__":
    serve()