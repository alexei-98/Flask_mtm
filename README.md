# Flask_mtm
# Main goal: Display the Data from the MySQL Database "amicaldopj" in the HTML/Jinja Template through Flask and SQLAlchemy
# Changes TO DO: Line 16-20 --> Change the database name, user, password and host. Database should be created before starting the application because the app doesn't create one
# problems:
#  Line 70 --> Querying the 'Tags' table 
#  Line 90-95 --> The Tags Objects are splitted and inserted as single elements but the 'append' function generates the error "AttributeError: 'str' object has no attribute 'tags'"
# insights:
  Both Domains and Tags are inserted correctly, the problem should be with the association table not recording the inserted data.
  After resolving the inserted data in the association table, they should be displayed on the index.html page.
