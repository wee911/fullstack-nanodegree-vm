from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# HTTPRequestHandler class
class WebServerHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        print(self.path)
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Hello!</h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like 
            me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form> '''
            message += "</body></html>"
            self.wfile.write(bytes(message, 'utf8'))
            print(message)
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>&#161Hola<a href='/hello'>Back to Hello</a></body></html>"
            self.wfile.write(bytes(message, 'utf8'))
            print(message)
            return

        if self.path.endswith("/restaurants"):
            restaurants = session.query(Restaurant).all()
            output = ""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Objective 3 Step 1 - Create a Link to create a new menu item
            output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
            output += "<html><body>"
            for restaurant in restaurants:
                print(restaurant.name)
                output += restaurant.name
                output += "</br>"
                output += "<a href='/restaurants/%s/edit'>edit</a>" % restaurant.id
                output += "</br>"
                output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                output += "</br></br></br>"
            output += "</body></html>"
            self.wfile.write(bytes(output, 'utf8'))
            return

        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(
                id=restaurantIDPath).one()
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, 'utf8'))
                return
        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(
                id=restaurantIDPath).one()
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, 'utf8'))
                return
        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]

            myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                output += "<input type = 'submit' value = 'Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf8'))
            return
        if self.path.endswith("/restaurants/new"):
            output = ""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output += "<html><body>"
            output += "<h1>Make a New Restaurant</h1>"
            output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
            output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
            output += "<input type='submit' value='Create'>"
            output += "</form></body></html>"
            self.wfile.write(bytes(output, 'utf8'))
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # POST
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    print(messagecontent[0].decode("utf-8"))
                    newRestaurant = Restaurant(name=messagecontent[0].decode("utf-8"))
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0].decode("utf-8")
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    return
        except:
            pass


def main():
    try:
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        port = 8081
        server_address = ('', port)
        httpd = HTTPServer(server_address, WebServerHandler)
        print("Web Server running on port %s" % port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server....")
        httpd.socket.close()


if __name__ == '__main__':
    main()
