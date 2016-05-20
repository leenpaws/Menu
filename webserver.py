
from BaseHTTPServer import  BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database_setup import Restaurant, Base, MenuItem


#Handler

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            #   Objective 1 visiting /restaurants lists all the
            #   restaurant names in the database
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #objective 3 step 2 create restaurants/new
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
            #   Objective 2
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #Objective 1: read from database
                result = session.query(Restaurant).all()
                output = "<html><body>"
                for restaurant in result:
                    print
                    output += "<p>%s</p>" % restaurant.name
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                output += "</html></body>"
                self.wfile.write(output)
                return
            # Objective 4 rename restaurant by going to /restaurant/id/edit
            if self.path.endswith("/edit"):
                #   third value of this array contains res. ID number
                restaurantIDPath = self.path.split("/")[2]
                #filter by ID to get number
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
                    self.wfile.write(output)


            #Objective 5: delete restaurant
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
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
                    self.wfile.write(output)
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)



#Get is to get info using Urls
#Post method is to post to server

def do_POST(self):
    try:
        self.send_response(301)
        self.end_headers()

        if self.path.endswith("/restaurant/name"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant Object
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        #Objective 4 to edit restaurant name:
        if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                #grab input
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                #reset name field to entry created in form-add to session-commit
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        #Objective 5: delete restaurant
        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(
                id=restaurantIDPath).one()
            if myRestaurantQuery:
                session.delete(myRestaurantQuery)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

    except:
        pass
#main
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()


    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()




if __name__ == '__main__':
    main()