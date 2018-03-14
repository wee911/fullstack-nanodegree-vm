from http.server import BaseHTTPRequestHandler, HTTPServer

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
            message += "<html><body>Hello!</body></html>"
            self.wfile.write(bytes(message, 'utf8'))
            print (message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)



def main():
    try:
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        port = 8081
        server_address = ('', port)
        httpd = HTTPServer(server_address, WebServerHandler)
        print ("Web Server running on port %s" % port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ("^C entered, stopping web server....")
        httpd.socket.close()


if __name__ == '__main__':
    main()