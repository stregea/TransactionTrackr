# TransactionTrackr
A Python application that keeps track and visualize your transactions across multiple accounts.

Eventually on <a href="https://www.samueltregea.com/projects/" target="_blank">my website</a> there will be a video demonstration
on this project.


## Requirements
<ul>
    <li>Python 3.6+</li>
</ul>

## Installation For Local Machine
<strong>To be able to successfully run the application, Python dependencies must be installed.</strong>
<br><br>
1. Install Python 3.6 or later. The download can be found <a href="https://www.python.org/downloads/" target="_blank">here</a>.
   * To see your latest version of python execute the command-line command: `/path/to/python3/directory/python3 -V`
2. Install the project dependencies.
   * To download the project dependencies, execute the command: `/path/to/python3/directory/pip3 install -r /path/to/project/directory/requirements.txt`


## Project Arguments
```
optional arguments:
  -h, --help            show this help message and exit
  -c, --show_console    display information on to the console.
  -v, --show_visual     display information from a visualization perspective.
  -u USERNAME, --username USERNAME
                        the username to sign in with.
  -p PASSWORD, --password PASSWORD
                        the password to sign in with.
```

###Side Note On Parameters: 
If `-u` or `-p` are not detected, or a bad sign-in is performed, you will be taken to the main sign in menu.

The parameters `-c` and `-v` are recommended for use since both options will determine whether to actually display the data.

The order of the parameters does not matter.


## Run The Application
To run the program, execute the following command-line command:
`/path/to/python3/directory/python3 /path/to/project/directory/main.py -c -v`

If your account has already been created, execute the command-line command:<br>
`/path/to/python3/directory/python3 /path/to/project/directory/main.py -c -v -u your_username -p your_password`<br>
This command will automatically sign you in, allowing you to skip the sign-in step.


## Uploading Data
Currently, only ESL Federal Credit Union and Apple Card's are the only account types supported.

To upload data, you will have to export `.csv` files from either account type, and place the files within the proper subdirectories.

- Apple Card export information will need to be placed within `/path/to/project/directory/Upload/Apple/`.

- Similarly, ESL export information will need to be placed within `/path/to/project/directory/Upload/ESL/`.

Once the files have been placed into the `Upload` directory, select the 'upload' option from the main menu. 

Upon choosing the 'upload' option, the files are then uploaded to the database allowing for full use of the application.


## Uploading Dummy Data
<strong>If you don't have an ESL Federal Credit Union account, or an Apple Card account, the ability to upload data still exists.</strong>


1. Sign-in
2. Select Settings
3. Upload Random Data

Once 'Upload Random Data' was selected, you will be prompted to enter your password.
If you correctly enter your password, the process of generating and uploading the dummy data will begin.
Otherwise, if the password is incorrect, the application will not generate and upload any data.


## Future Features

<strong>Admin</strong>
This feature will allow any user that is deemed an admin, to directly interact with the database and user accounts.

<strong>Charts</strong>
This feature will add more visualizations into the application. Currently, 'Bar Charts' are supported and 'Pie Charts' are implemented,
but I would like to implement the 'Pie Chart' and other types charts into the application to help better visualize user data.


## Recommendations
If you beleive that there are any improvements that need to be made or want to see certain features added, feel free to <a href="https://samueltregea.com/contact/" target="_blank"> contact me</a>.
