<h1>Start the server</h1>
<pre>node index.js</pre>

<h1>Paths</h1>
JPEG: <pre>http://localhost:3000/jpeg/url</pre>
HTML: <pre>http://localhost:3000/html/url</pre>

<h1>Example Usage</h1>
Take http://www.example.com's screenshot and save it as example.jpeg:
<pre>curl -X GET "http://localhost:3000/jpeg/http://www.example.com" > example.jpeg</pre> 
Render http://www.example.com and return its HTML content as example.html:
<pre>curl -X GET "http://localhost:3000/html/http://www.example.com" > example.html</pre> 