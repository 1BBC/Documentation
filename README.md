# Documentation

1. vim /etc/apache2/sites-enabled/example.com.conf

Listen 81
#Main server config
<VirtualHost _default_:81>
  AddDefaultCharset utf8
  DocumentRoot "/usr/abills/Documentation"
  ErrorDocument 404 "/"

  <Directory "/usr/abills/Documentation">
    AllowOverride All
    Order allow,deny
    Allow from all
    Require all granted
    Satisfy Any


  AddHandler cgi-script .cgi
  Options Indexes ExecCGI FollowSymLinks
  DirectoryIndex index.cgi
  </Directory>



</VirtualHost>


2. http://[your ip]:81/doc.cgi
