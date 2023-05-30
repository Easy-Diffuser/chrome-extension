import os
import http.server

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        
        image = post_body.decode('utf-8')
    
        with open('./index.html', 'r') as f:
            lines = f.readlines()
            
        to_modify = ""
        to_modify_num = -1
        
        for i, line in enumerate(lines):
            if line.strip()[:15] == '<img id="image"':
                source = line[line.find("src"):line.find("alt") - 1]
                source = source[:4] + f'"{image}"'
                to_modify = line[:line.find("src")] + source + line[line.find("alt") - 1:]
                to_modify_num = i
                break
        
        lines[to_modify_num] = to_modify
                
        with open('./index.html', 'w') as f:
            f.writelines(lines)
        
        
        

if __name__ == '__main__':
    print("Server Run")
    default_image = "./images/no-image.png"
    
    with open('./index.html', 'r') as f:
        lines = f.readlines()
        
    to_modify = ""
    to_modify_num = -1
    
    for i, line in enumerate(lines):
        if line.strip()[:15] == '<img id="image"':
            source = line[line.find("src"):line.find("alt") - 1]
            source = source[:4] + f'"{default_image}"'
            to_modify = line[:line.find("src")] + source + line[line.find("alt") - 1:]
            to_modify_num = i
            break
    
    lines[to_modify_num] = to_modify
            
    with open('./index.html', 'w') as f:
        f.writelines(lines)
                
    
    PORT = 9889
    
    handler = HTTPRequestHandler
    handler.extensions_map['.js'] = 'application/javascript'


    server = http.server.HTTPServer(('', PORT), handler)

    server.serve_forever()