# import modules to run client
import grpc
import service.library_pb2  as library_pb2
import service.library_pb2_grpc as library_pb2_grpc

# import Genre to validate client input
from service.library_pb2 import Genre

# run client code
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        # create stub to interact with server
        stub = library_pb2_grpc.InventoryStub(channel)

        # display menu for user to select choice
        print("1. CreateBook")
        print("2. GetBook")
        rpc_call = input("Which rpc would you like to call: ")

        # if user wants to create book, take input and call corresponding server method
        if rpc_call == "1":
            # take input
            isbn = input("Enter unique isbn of book: ")
            title = input("Enter title of book:")
            author = input("Enter author of book:")

            # take input for genre and validate if it is correct
            genre = input("Enter genre of book:")
            while(genre not in Genre.keys()):
                print("The genre you entered is not a valid one, these are the following genre's supported currently (case sensitive):")
                for genre_name in Genre.keys():
                    print(genre_name)
                genre = input("Enter genre of book:")

            # take year input
            year = int(input("Enter publishing year formatted as YYYY: "))
            
            # create book request to send to server
            create_book_request = library_pb2.Book(isbn=isbn, title=title, author=author, genre=genre, publishing_year=year)

            # send request to server using stub and print response
            response = stub.CreateBook(create_book_request)
            print("Create book rpc response received: ")
            print(response)
        
        # if user wants to get book, take input and call corresponding server method
        elif rpc_call == "2":
            # take input
            isbn = input("Enter unique isbn of book to query: ")

            # create isbn request to send to server
            isbn_request = library_pb2.ISBN(isbn=isbn)
            
            # send request to server using stub and print response
            response = stub.GetBook(isbn_request)
            print("Get book rpc response received: ")
            print(response)

        # print error msg if user choice is invalid
        else:
            print("Invalid choice")

# if script is called, run client code
if __name__ == "__main__":
    run()