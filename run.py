
from EcommerceApp import app, db

if __name__ == '__main__':
    # Ensure that the database is created and initialized before running the app
    with app.app_context():
        # db.drop_all()
        db.create_all()

    # Run the app in debug mode on 0.0.0.0 (accessible from outside the local machine)
    app.run(debug=True, port=8080)


# if __name__ == '__main__':
#     from backend impo

#     # Ensure that the database is created and initialized before running the app
#     with app.app_context():
#         db.create_all()

#     # Run the app in debug mode on 0.0.0.0 (accessible from outside the local machine)
#     app.run(debug=True, host='0.0.0.0', port=8080)




# # run.py
# if __name__ == '__main__':
#     from backend import app, db

#     with app.app_context():
#         db.create_all()

#     app.run(debug=True, host='0.0.0.0', port=8080)



