import logging
import argparse
import psycopg2


logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection=psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
        connection.rollback()
        command="update snippets set message=%s where keyword=%s"
        cursor.execute(command,(snippet,name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve a snippet with an associated name."""
    logging.info("Getting snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select keyword, message from snippets where keyword=(%s)"
    cursor.execute(command,(name,))
    answer=cursor.fetchone()
    connection.commit()
    logging.debug("Snippet retrieved successfully")
    if not answer:
        return "404: Snippet Not Found"
    return answer[0]

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")

    logging.debug("constructing a get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="name of the snippet")


    arguments = parser.parse_args()
    #convert parsed arguments from Namespace to dictionary
    arguments= vars(arguments)
    command = arguments.pop("command")

    if command=="put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet= get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
        


if __name__=="__main__":
	main()
