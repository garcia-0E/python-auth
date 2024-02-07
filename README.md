
**Test Instructions**
> This task should take approximately 2 hours to complete
Please send us your solution within 7 days, or let us know if you need more time
Feel free to utilize all available public resources for additional information. The use of AI tools is welcome in this task, if you decide to utilize an AI tool please also provide some guidance for us on what tool you used and how for our reference
If you still have questions about any of the below tasks, feel free to reply to this email

**Background**

Many websites allow their visitors to create a customized personal account. This is usually done through a web interface that allows new users to register by completing a registration form.

- [X] This task includes designing and implementing a backend that possesses the functions outlined below. The necessary data should be stored in an SQL database. Please develop a suitable schema and create a Python module that provides the functionality described below. For this task, you are not expected to connect a website (or even write HTML for the site), maintain web sessions via cookies or similar.

- [X] A new user can register with their email address and password of choice. Once the registration process is complete, the user will receive a confirmation email. This email will contain a link that needs to be clicked on in order to activate the account. Note: Sending an actual email or routing the request when the user clicks on the activation link is not part of the task.

- [X] Users enter their email address and password to log in. The authentication should only be successful if a valid combination of email and password is provided.

### Implementation Notes
Please only use Python 3 standard libraries in your solution. You may use pytest or any other testing framework for testing your code.
For the sake of simplicity, please use sqlite3 in order to connect to the database.
Please record your solution in an appropriate way. We are especially interested in a discussion of your chosen implementation as compared to other possible approaches.
You may use any tools you deem useful for this task - we only ask that you mention if you used any coding assistants.


### Developer Notes

1. The coverage of this test reach the 100% of the requirements, this includes: two endpoints for registration and authentication, tests and a http module that supports the system.

2. It's recommended to install a venv and install all the dependencies in there.

3. The database name used was ableton.db, depending on the OS it might need the relative or absolute path.

4. ChatGPT was used to describe the HTTP module that inherits from http.server library.


-- Thank you and looking forward to hear from you, guys!

Ramon Tomas.