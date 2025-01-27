import flash as flash
from flask import Flask, render_template,request, redirect, url_for, session, flash ,request
import mysql.connector

app = Flask(__name__)
app.secret_key = 'VIJAY24'

# Configuration for serving static files
app.config['STATIC_FOLDER'] = 'static'
app.config['DEBUG'] = 'True'

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vijay",
    database="food_donation"
)
mycursor = mydb.cursor()

                                    #HOME
@app.route('/')
def home():
    if 'logged_in' in session:
        user = request.args.get('user')  # Get user information from the URL
        login_message = "Login successful!"
    else:
        login_message = "You are not logged in."
    testimonials = [
        {"name": "Maria G.", "text": "I'm so grateful for the food donations I've received through Food Guardians. The food has been high-quality and has made a big difference for my family.", "date": "3 days ago"},
        {"name": "Ben L.", "text": "I work at a grocery store and we have a lot of surplus food that would otherwise go to waste. Food Guardians makes it easy to connect with local organizations who can put the food to good use.", "date": "5 days ago"},
        {"name": "Isabella H.", "text": "Our restaurant has been struggling during the pandemic, but Food Guardians has helped us donate excess food to people in our community. It's been a great way to reduce food waste and support those in need.", "date": "1 week ago"},
    ]
    donations = [
        {"type": "Fresh bread from local bakery", "distance": "2 miles away"},
        {"type": "Produce from local farm", "distance": "5 miles away"},
        {"type": "Prepared meals from local restaurant", "distance": "10 miles away"},
        {"type": "Canned goods from local grocery store", "distance": "15 miles away"},
    ]
    volunteers = [
        {"name": "Dhanakarthikeyan.P", "email": "Demerkarthi@gmail.com", "phone": "123-456-7890", "location": "Madurai"},
        {"name": "Balanarayanan.P", "email": "Dhonibala@gmail.com", "phone": "456-789-0123", "location": "Madurai"},
        {"name": "Hariramsurya.V G", "email": "hariram@gmail.com", "phone": "789-012-3456", "location": "Madurai"},
        {"name": "Bhuvaneshwaran.P", "email": "bhuvanesh@gmail.com", "phone": "456-789-0123", "location": "Madurai"},
        {"name": "Vijay.B", "email": "vijaye@gmaile.com", "phone": "789-012-3456", "location": "Madurai"}
    ]

    return render_template('index.html', testimonials=testimonials, donations=donations,volunteers=volunteers, login_message=login_message)


                                    #SIGNUP MODULE

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Insert new user into the database with phone number
        # Assume you have your database connection and cursor set up already
        sql = "INSERT INTO users (username, email, phone, password) VALUES (%s, %s, %s, %s)"
        val = (username, email, phone, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        mydb.commit()

        # Redirect to login page after successful registration
        return redirect(url_for('login', success_message="Successfully registered!"))

    return render_template('signup.html')


                            #LOGIN MODULE
# Route for the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if user exists in the database
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        if user:
            # Set session variables to indicate successful login
            session['logged_in'] = True
            session['user_id'] = user[0]  # Assuming user id is in the first column
            # Redirect to the home page
            return redirect(url_for('home'))
        else:
            error = "Login failed. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')


# Route for deleting a login
@app.route('/delete_login/<int:user_id>', methods=['POST'])
def delete_login(user_id):
    if 'admin' in session:  # Check if user is logged in as admin
        # Create MySQL cursor
        mycursor = mydb.cursor()

        # Delete the login from the database
        sql = "DELETE FROM users WHERE id = %s"
        val = (user_id,)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect(url_for('logindetails'))  # Redirect to the login details page
    else:
        return redirect(url_for('admin_login'))

# Route for the profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve user input for updating information
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Update user information in the database
        sql = "UPDATE users SET username = %s, email = %s, phone = %s,password = %s WHERE id = %s"
        val = (username, email, phone, password, session['user_id'])
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirect to the profile page after updating information
        return redirect(url_for('profile'))

    # Retrieve user information from the database
    user_id = session['user_id']
    sql = "SELECT * FROM users WHERE id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()

    return render_template('profile.html', user=user)

# Route for the logindetails page
@app.route('/logindetails')
def logindetails():
    if 'admin' in session:

        # Fetch all login details
        mycursor.execute("SELECT * FROM users")
        login_details = mycursor.fetchall()

        return render_template('logindetails.html', login_details=login_details,)
    else:
        return redirect(url_for('admin_login',))

# Route for logging out
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the home page
    return redirect(url_for('home'))


                                #DONATE MODULE
# Route for the donate form
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if 'logged_in' in session:
        if request.method == 'POST':
            # Retrieve form data
            organization_name = request.form['Organization Name']
            food_type = request.form['foodType']
            quantity = request.form['quantity']
            donor_name = request.form['donorName']
            donor_address = request.form['donorAddress']
            donor_phone = request.form['donorPhone']
            donation_method = request.form['donationMethod']
            drop_off_location = request.form['drop_off_location']
            # Insert donation into the database (replace placeholders with actual database code)
            sql = "INSERT INTO donations (organization_name, food_type, quantity, donor_name, donor_address, donor_phone, donation_method, drop_off_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (organization_name, food_type, quantity, donor_name, donor_address, donor_phone, donation_method, drop_off_location)
            # Replace the following lines with your actual database connection and cursor execution
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('donatesuccess'))  # Redirect to another route after successful submission
        return render_template('donate.html')  # Render the donate.html template for GET requests
    else:
        return redirect(url_for('login'))


@app.route('/donationdetails', methods=['GET', 'POST'])
def donation_details():
    if 'admin' in session:
        if request.method == 'POST':
            received_from = request.form.get('received_from')
            donated_for = request.form.get('donated_for')
            donation_id = request.form.get('donation_id')  # Assuming you have a form field for donation_id

            # Update the received_from and donated_for values in the database
            try:
                sql = "UPDATE donations SET received_from = %s, donated_for = %s WHERE id = %s"
                val = (received_from, donated_for, donation_id)
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as err:
                print(f"Error updating donation details: {err}")

        # Fetch updated donation details from the database
        try:
            mycursor.execute("SELECT * FROM donations")
            donation_details = mycursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching updated donation details: {err}")
            donation_details = []  # Provide an empty list in case of error

        return render_template('donationdetails.html', donation_details=donation_details)
    else:
        return redirect(url_for('admin_login'))


# Define a route for view details
@app.route('/view/<int:donation_id>', methods=['GET'])
def view(donation_id):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vijay",
        database="food_donation"
    )

    mycursor = mydb.cursor()
    query = "SELECT * FROM donations WHERE id = %s"
    mycursor.execute(query, (donation_id,))
    donation = mycursor.fetchone()
    mycursor.close()
    mydb.close()

    # Pass the donation details to the HTML template for rendering
    return render_template('view.html', donation=donation)


# Route for the edit_donation page
@app.route('/edit_donation/<int:donation_id>', methods=['GET', 'POST'])
def edit_donation(donation_id):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vijay",
        database="food_donation"
    )
    mycursor = mydb.cursor()

    if request.method == 'GET':
        mycursor.execute("SELECT * FROM donations WHERE id = %s", (donation_id,))
        donation_details = mycursor.fetchall()
        mycursor.close()
        return render_template('edit_donation.html', donation_details=donation_details)

    if request.method == 'POST':
        received_from = request.form['received_from']
        donated_for = request.form['donated_for']

        mycursor.execute("UPDATE donations SET received_from = %s, donated_for = %s WHERE id = %s",
                         (received_from, donated_for, donation_id))
        mydb.commit()
        mycursor.close()
        return redirect(url_for('view', donation_id=donation_id))

# Route for the Donate page
@app.route('/donatesuccess')
def donatesuccess():
    return render_template('donatesuccess.html')

                                    #REQUEST MODULE

# Route for the request form
@app.route('/request', methods=['GET', 'POST'])
def request_food_donation():
    if 'logged_in' in session:
        if request.method == 'POST':
            informer_name = request.form['informer_name']
            informer_address = request.form['informer_address']
            informer_number = request.form['informer_number']
            needer_address = request.form['needer_address']
            landmark = request.form['landmark']
            num_people = request.form['num_people']

            # Insert request into the database
            sql = "INSERT INTO requests (informer_name, informer_address, informer_number, needer_address, landmark, num_people) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (informer_name, informer_address, informer_number, needer_address, landmark, num_people)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('requestsuccess'))
        return render_template('request.html')
    else:
        return redirect(url_for('login'))


@app.route('/requestdetails', methods=['GET', 'POST'])
def requestdetails():
    if 'admin' in session:
        if request.method == 'POST':
            # Handle POST request data if needed
            pass

        # Fetch request details from the database
        try:
            mycursor.execute("SELECT * FROM requests")
            request_details = mycursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching request details: {err}")
            request_details = []  # Provide an empty list in case of error

        return render_template('requestdetails.html', request_details=request_details)
    else:
        return redirect(url_for('admin_login'))

# Route for the requestsuccess page
@app.route('/requestsuccess')
def requestsuccess():
    return render_template('requestsuccess.html')

                                        #ADMIN MODULE
# Route for the admin login form
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if admin credentials are correct
        if username == 'admin' and password == '000000':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Login failed. Please try again."
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')


# Route for the admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('admin_login',))




                                #VOLUNTEERS MODULE

@app.route('/volunteer_request', methods=['POST'])
def volunteer_request():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        # Insert new user into the database with phone number
        # Assume you have your database connection and cursor set up already
        mycursor = mydb.cursor()
        sql = "INSERT INTO VolunteerRequests (name, phone) VALUES (%s, %s)"
        val = (name, phone)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()

        # Redirect to a success page after successful registration


    return render_template('index.html')


# Route for the vol_reg_details page
@app.route('/vol_reg_details')
def vol_reg_details():
    if 'admin' in session:

        # Fetch all vol_reg_details
        mycursor.execute("SELECT * FROM VolunteerRequests")
        vol_reg_details = mycursor.fetchall()

        return render_template('vol_reg_details.html', vol_reg_details=vol_reg_details,)
    else:
        return redirect(url_for('admin_login',))

# Route for deleting a volunteer
@app.route('/delete_volunteer_rqt/<int:volunteer_id>', methods=['POST'])
def delete_volunteer_rqt(volunteer_id):
    if 'admin' in session:
        # Delete the volunteer from the database
        mycursor.execute("DELETE FROM VolunteerRequests WHERE id = %s", (volunteer_id,))
        mydb.commit()

        flash('Volunteer deleted successfully', 'success')
        return redirect(url_for('vol_reg_details'))

    else:
        return redirect(url_for('admin_login'))

# Route for the volunteers login form
@app.route('/volunteers_login', methods=['GET', 'POST'])
def volunteers_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if volunteer exists in the database
        sql = "SELECT * FROM volunteers WHERE email = %s AND phone = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        volunteer = mycursor.fetchone()
        if volunteer:
            # Set session variables to indicate successful login
            session['volunteer_logged_in'] = True
            session['volunteer_id'] = volunteer[0]  # Assuming volunteer id is in the first column
            # Redirect to the volunteer dashboard
            return redirect(url_for('volunteers_dashboard'))
        else:
            error = "Login failed. Please check your email or password and try again."
            return render_template('volunteers_login.html', error=error)
    return render_template('volunteers_login.html')


# Route for the profile page
@app.route('/volunteer_profile', methods=['GET', 'POST'])
def volunteer_profile():
    # Check if volunteer is logged in
    if 'volunteer_logged_in' not in session:
        return redirect(url_for('volunteers_login'))

    if request.method == 'POST':
        # Retrieve volunteer input for updating information
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']

        # Update volunteer information in the database
        sql = "UPDATE volunteers SET name = %s, email = %s, phone = %s, location = %s WHERE id = %s"
        val = (name, email, phone, location, session['volunteer_id'])
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirect to the profile page after updating information
        return redirect(url_for('volunteer_profile'))

    # Retrieve volunteer information from the database
    volunteer_id = session['volunteer_id']
    sql = "SELECT * FROM volunteers WHERE id = %s"
    val = (volunteer_id,)
    mycursor.execute(sql, val)
    volunteer = mycursor.fetchone()

    return render_template('volunteer_profile.html', volunteer=volunteer)


# Route for the volunteers dashboard
@app.route('/volunteers_dashboard')
def volunteers_dashboard():
    if 'admin' in session:
        return render_template('volunteers_dashboard.html')
    else:
        return redirect(url_for('volunteers_login',))

# Route for the volunteers page
@app.route('/volunteers')
def volunteers():
    if 'admin' in session:

        # Fetch all volunteers details
        mycursor.execute("SELECT * FROM volunteers")
        volunteers_details = mycursor.fetchall()

        return render_template('volunteers.html', volunteers_details=volunteers_details, )
    else:
        return redirect(url_for('admin_login'))

@app.route('/add_volunteer', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']

        # Insert new volunteer into the database
        sql = "INSERT INTO volunteers (name, email, phone, location) VALUES (%s, %s, %s, %s)"
        val = (name, email, phone, location)
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirect to a success page or another route after successful addition
        return redirect(url_for('volunteers', success_message="Successfully added!"))

    return render_template('add_volunteer.html')


# Route for editing a volunteer
@app.route('/edit_volunteer/<int:volunteer_id>', methods=['GET', 'POST'])
def edit_volunteer(volunteer_id):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            location = request.form['location']

            # Update the volunteer details in the database
            sql = "UPDATE volunteers SET name = %s, email = %s, phone = %s, location = %s WHERE id = %s"
            val = (name, email, phone, location, volunteer_id)
            mycursor.execute(sql, val)
            mydb.commit()

            flash('Volunteer details updated successfully', 'success')
            return redirect(url_for('volunteers'))

        # Fetch the volunteer details to display in the edit form
        mycursor.execute("SELECT * FROM volunteers WHERE id = %s", (volunteer_id,))
        volunteer = mycursor.fetchone()

        if volunteer:
            return render_template('edit_volunteer.html', volunteer=volunteer)
        else:
            flash('Volunteer not found', 'error')
            return redirect(url_for('volunteers'))
    else:
        return redirect(url_for('admin_login'))


# Route for deleting a volunteer
@app.route('/delete_volunteer/<int:volunteer_id>', methods=['POST'])
def delete_volunteer(volunteer_id):
    if 'admin' in session:
        # Delete the volunteer from the database
        mycursor.execute("DELETE FROM volunteers WHERE id = %s", (volunteer_id,))
        mydb.commit()

        flash('Volunteer deleted successfully', 'success')
        return redirect(url_for('volunteers'))

    else:
        return redirect(url_for('admin_login'))

                            #TRUST MODULE
@app.route('/trust')
def trust():
    if 'admin' in session:

        # Fetch all trust details
        mycursor.execute("SELECT * FROM trust")
        trust_details = mycursor.fetchall()

        return render_template('trust.html', trust_details=trust_details, )
    else:
        return redirect(url_for('admin_login'))

@app.route('/add_trust', methods=['GET', 'POST'])
def add_trust():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        category = request.form['category']
        contact = request.form['contact']

        # Insert new trust into the database
        sql = "INSERT INTO trust (name, location, category, contact) VALUES (%s, %s, %s, %s)"
        val = (name, location, category, contact)
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirect to a success page or another route after successful addition
        return redirect(url_for('admin_dashboard', success_message="Successfully added!"))

    return render_template('add_trust.html')

# Route for editing a trust
@app.route('/edit_trust/<int:trust_id>', methods=['GET', 'POST'])
def edit_trust(trust_id):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['name']
            location = request.form['location']
            category = request.form['category']
            contact = request.form['contact']

            # Update the volunteer details in the database
            sql = "UPDATE trust SET name = %s, location = %s, category = %s, contact = %s WHERE id = %s"
            val = (name, location, category, contact, trust_id)
            mycursor.execute(sql, val)
            mydb.commit()

            flash('trust details updated successfully', 'success')
            return redirect(url_for('trust'))

        # Fetch the volunteer details to display in the edit form
        mycursor.execute("SELECT * FROM trust WHERE id = %s", (trust_id,))
        trust = mycursor.fetchone()

        if trust:
            return render_template('edit_trust.html', trust=trust)
        else:
            flash('trust not found', 'error')
            return redirect(url_for('trust'))
    else:
        return redirect(url_for('admin_login'))


# Route for deleting a trust
@app.route('/delete_trust/<int:trust_id>', methods=['POST'])
def delete_trust(trust_id):
    if 'admin' in session:
        # Delete the trust from the database
        mycursor.execute("DELETE FROM trust WHERE id = %s", (trust_id,))
        mydb.commit()

        flash('trust deleted successfully', 'success')
        return redirect(url_for('trust'))

    else:
        return redirect(url_for('admin_login'))



@app.route('/welfare')
def welfare():
    welfare_organizations = [
        {
            "name": "Care Trust",
            "location": "CNC Nagar Kalai Nagar, Madurai",
            "category": "Animal Welfare Organisations, NGOS",
            "contact": {
                "type": "07942696185",
            }
        },
        {
            "name": "People For Animals",
            "location": "Periyasamy Nagar Avaniapuram, Madurai",
            "category": "Animal Welfare Organisations, Welfare Organisations",
            "contact": {
                "type": "07942695905",
            }
        },
        {
            "name": "Save Animals Madurai",
            "location": "Golden Hospital Gomathipuram, Madurai",
            "category": "Animal Welfare Organisations, Stray Dog Welfare Organisations",
            "contact": {
                "type": "07942696124",
            }
        },
        {
            "name": "Nisa Foundation",
            "location": "Near Mosque Yagappa Nagar Vandiyur, Madurai",
            "category": "Animal Welfare Organisations, Stray Dog Welfare Organisations",
            "contact": {
                "type": "07942695945",
            }
        }
    ]

    return render_template('welfare.html', welfare=welfare_organizations)


                                    # CONTACT MODULE
# Function to insert data into the database
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve data from the form
        name, email, message = request.form['name'], request.form['email'], request.form['message']
        cursor = mydb.cursor()
        sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        val = (name, email, message)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        mydb.close()
        # Redirect to the about page after successful form submission
        return redirect('/about')
    return render_template('contact.html')


# Route for deleting a volunteer
@app.route('/delete_contact/<int:contact_id>', methods=['GET', 'POST'])
def delete_contact(contact_id):
    if 'admin' in session:
        # Delete the contact from the database
        mycursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        mydb.commit()

        flash('contact deleted successfully', 'success')
        return redirect(url_for('contactdetails'))

    else:
        return redirect(url_for('admin_login'))


# Route for the contactdetails page
@app.route('/contactdetails')
def contactdetails():
    if 'admin' in session:
        # Fetch all contact details
        mycursor.execute("SELECT * FROM contacts")
        contact_details = mycursor.fetchall()
        return render_template('contactdetails.html', contact_details=contact_details)
    else:
        return redirect(url_for('admin_login'))

                                    # FEEDBACK MODULE


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'logged_in' in session:
        if request.method == 'POST':
            # Retrieve form data
            name = request.form['name']
            email = request.form['email']
            experience = request.form['experience']
            professionalism = request.form['professionalism']
            comments = request.form['comments']

            # Insert feedback into the database
            sql = "INSERT INTO feedback (name, email, experience, professionalism, comments) VALUES (%s, %s, %s, %s, %s)"
            val = (name, email, experience, professionalism, comments)

            # Execute the SQL query
            mycursor.execute(sql, val)
            mydb.commit()

            return redirect(url_for('about'))  # Redirect to another route after successful submission
        return render_template('feedback.html')  # Render the feedback.html template for GET requests
    else:
        return redirect(url_for('login'))


# Route for the feedbackdetails page
@app.route('/feedbackdetails')
def feedbackdetails():
    if 'admin' in session:
        # Fetch all feedback details
        mycursor.execute("SELECT * FROM feedback")
        feedback_details = mycursor.fetchall()
        return render_template('feedbackdetails.html', feedback_details=feedback_details)
    else:
        return redirect(url_for('admin_login'))

                                    #OTHER MODULES
# Route for the privacy-policy page
@app.route('/privacy-policy')
def privacypolicy():
    return render_template("privacy-policy.html")


# Route for the termsofservice page
@app.route('/terms-of-service')
def termsofservice():
    return render_template('terms-of-service.html')


# Route for the disclaimer page
@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


# Route for the help page
@app.route('/help')
def help():
    return render_template('help.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the chatbot page
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        # Handle form submission here if needed
        pass

    return render_template('chatbot.html')


if __name__ == '__main__':
    app.run(debug=True)



organizations = [
    {
        "name": "Anu Old Age Home",
        "location": "DRO Colony K Pudhur, Madurai",
        "category": "Institutions For Aged Charitable Old Age Homes",
        "contact": {
            "type": "09724318701",
        }
    },
    {
        "name": "Thaai Paravai Old Age Home",
        "location": "Vel Nagar Iyer Bungalow, Madurai",
        "category": "Institutions For Aged Charitable Old Age Homes",
        "contact": {
            "type": "08128852692",
        }
    },
    {
        "name": "Kirupa Old Age Home (Free Service)",
        "location": "Mangalakudi Village, Madurai",
        "category": "Institutions For Aged Charitable Old Age Homes",
        "contact": {
            "type": "08488925473",
        }
    },
    {
        "name": "Royal Vision",
        "location": "Perungudi Madurai City, Madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698483",
        }
    },
    {
        "name": "Anbu Suzh Ulagu Foundation",
        "location": "Madurai Road Tirumangalam, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698453",
        }
    },
    {
        "name": "Madurai Seed",
        "location": "Behind Gandhi Museum Karumbalai Gandhi Nagar, Madurai",
        "category": "Charitable Old Age Homes NGOS",
        "contact": {
            "type": "07942698542",
        }
    },
    {
        "name": "M S Perumal Social Trust Maravapatty",
        "location": "SREE BHARASAKTHI KALIYAMMAN KOVIL STREET Madurai, Madurai",
        "category": "Charitable Trusts Social Service Organisations",
        "contact": {
            "type": "07942698430",
        }
    },
    {
        "name": "Missionaries Of Charity Annai Teresa Illam",
        "location": "Opposite Fatima College Vilangudi, Madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698348",
        }
    },
    {
        "name": "Voluntary Association For People Service",
        "location": "Behind Ptr Mahal Chinna Chokkikulam, Madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698363",
        }
    },
    {
        "name": "Idhayam Charitable Trust",
        "location": "Ram Nagar, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698419",
        }
    },
    {
        "name": "Kaakum Karangal Charitable Trust",
        "location": "Thirunagar Police Station Opp St Thirunagar, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698212",
        }
    },
    {
        "name": "Mahasemam Trust",
        "location": "Melur, madurai",
        "category": "Charitable Trusts Health Care Centres",
        "contact": {
            "type": "07942698245",
        }
    },
    {
        "name": "M.D. CHARITABLE TRUST",
        "location": "NEAR SELVI HOMEOPATHY MEDICALS, madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698249",
        }
    },
    {
        "name": "Nikhil Foundation",
        "location": "Bharath Nagar Tiruppalai, Madurai",
        "category": "Charitable Old Age Homes NGOS",
        "contact": {
            "type": "07942698250",
        }
    },
    {
        "name": "Sri Rajarajeswari Amman Temple and Charitable Trust",
        "location": "Near Tvs Bus Stop Virattipathu, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698206",
        }
    },
    {
        "name": "She Welfare Trust",
        "location": "J P Kudil Usilampatti, Madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698083",
        }
    },
    {
        "name": "Akshaya's Helping I H.E.L.P Trust",
        "location": "1st Cross Street, Madurai",
        "category": "Orphanages Charitable Trusts",
        "contact": {
            "type": "07942698182",
        }
    },
    {
        "name": "Idhayam Trust",
        "location": "Opposite Ar Police Store Madurai Reserve Lines, Madurai",
        "category": "NGOS Charitable Trusts",
        "contact": {
            "type": "07942698112",
        }
    },
    {
        "name": "Joe Britto Educational And Social Trust",
        "location": "Kathakinaru, madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698174",
        }
    },
    {
        "name": "Madurai Charitable Trust",
        "location": "Near Keshavan Hospital, madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942698111",
        }
    },
    {
        "name": "Sadhana Trust",
        "location": "Madurai Race Course, madurai",
        "category": "Charitable Old Age Homes NGOS",
        "contact": {
            "type": "07942697805",
        }
    },
    {
        "name": "Springs Of Life Charitable Trust",
        "location": "Pykara, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942697961",
        }
    },
    {
        "name": "Masha Trust",
        "location": "rc church Anna Nagar Madurai, Madurai",
        "category": "Charitable Trusts Trustees",
        "contact": {
            "type": "07942697842",
        }
    },
    {
        "name": "LG Relax Home",
        "location": "Near By Golden Hospital Melamadai, madurai",
        "category": "Institutions For Aged Orphanages",
        "contact": {
            "type": "07942697799",
        }
    },
    {
        "name": "Elysium Foundation",
        "location": "Arignar Anna Nagar, Madurai",
        "category": "Charitable Trusts",
        "contact": {
            "type": "07942697764",
        }
    },
    {
        "name": "Bala Memorial Trust",
        "location": "Kurinji Nagar Near K B Yenthal Pillayar Kovil Andar Kottaram, Madurai",
        "category": "Charitable Trusts Welfare Organisations",
        "contact": {
            "type": "07942697732",
        }
    },
    {
        "name": "Thost Trust",
        "location": "Puthur Pudur Bazaar, Madurai",
        "category": "Charitable Trusts Research Centres",
        "contact": {
            "type": "07942697670",
        }
    }
]