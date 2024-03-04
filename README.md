# RESTFull_API
https://documenter.getpostman.com/view/33325990/2sA2xcaueF
Documentation


Here is a simple API building
with the help of SQLAlchemy , I created an API with the ability to GET/POST/PATCH/DELETE
With the  help of POSTman I tested the routes and published the document. 


class Cafe(db.Model): -> 
  This object, is created by SQLAlchemy Library and With mapped_column() i created Numbers 
  of columns in the database that holds information about people's favorit Cafes and their
  information 

with "request.args.get()", the program catches users Inputs and use them for DELETE or PATCH, 
