# COVID-19 Contact Tracing
The web-application extracts location information from 11 subjects for the past 7 days and determines a contact graph. The contact graph has 11 nodes. If a subject has been in contact with another subject then there is an edge between those two nodes, if not then no edge. Since we are in a time where it is not ideal to be outside, I have used a pre-existing dataset.

(Dataset used: Yonsei dataset, that consists of database files for 11 subjects including location information.)

indexLoc.html takes a Subject ID and Date as input. It then calls index.js script which in turn calls process.php. The php script runs db-server.py in the local machine to read the databases and build the contact graph.

The output is a contact_graph.txt file with the adjacency matrix of the contact graph.

Steps -

1. Install "nginx" and "php" in your system.
2. Edit "nginx.conf" and "php.ini" files accordingly (I have provided my configuration files).
3. Copy the indexLoc.html, index.js, process.php, db-server.py and the data files into "nginx/html" folder.
4. Install "Python3" and "SQLAlchemy" to successfully run the application.
4. Run "php-cgi.exe -b 127.0.0.1:9000" in the PHP folder, then start Nginx server.
5. Open localhost in a browser to render the HTML webpage.
6. Select "Subject ID" and enter "Date" and click on "Download Contact Graph" button (I have provided my downloaded contact graph file for Subject ID: 1 and Date: 05/06/2011).