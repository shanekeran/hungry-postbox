# Hungry Postbox: Testing

## Testing the User Stories
___

### Site User


<details><summary>Access the website from any device and easily navigate the website regardless of screen size.</summary>

- The website was created with a mobile first design that scales up to any device size. For example, the collapse navigation bar makes it easier to get around on smaller devices.
</details>

<details><summary>Be able to easily read all content and view all images displayed.</summary>

- All images and fonts increase / decrease in size based on screen size.
- Buttons increase in size when hovered over.
- Images contain alt tags in the event that they don't display.
</details>

<details><summary>Create an account with a profile that is customised with my own information and picture.</summary>

- Users are able to register for an account if they provide all the required information.
- Users can personalise their profiles with descriptions about themselves, unique usernames and a profile picture of their choosing.
</details>

<details><summary>Freely edit my profile and if necessary delete my account with ease.</summary>

- Users can edit their profiles from within their profile page without the need for the site owner to assist.
- Users can edit everything they originally entered into the registration form and this new information will be updated.
- Users can also delete their profiles from their profile page. Defensive programming was used to turn this into a 2 step process so users don't accidently delete their account.
</details>

<details><summary>Contact other members who I would like to become pen pals with and likewise for them to be able to contact me.</summary>

- When viewing other member profiles, users will be able to click on the clearly visible 'Contact' button. This will send an email to that member, stating that the user is interested in becoming pen pals. The email will contain the user's email address, username and link to their profile.
</details>

<details><summary>My account password to be securely stored to prevent any unauthorised access to my account.</summary>

-  Werkzeug generate_password_hash is used to securely store user passwords and prevent any unauthorised access.
</details>

### Site Owner

<details><summary>Provide a platform for users who to find new pen pals.</summary>

- Users can register, search through member profiles and contact them so I believe this has been achieved.
</details>

<details><summary>Promote my brand throughout the site, including links to our social media accounts.</summary>

- Each page contains a footer with links to Hungry Postbox Facebook, Twitter and Instagram accounts.
- The navigation bar on each page contains a small Hungry Postbox logo.
- All users are immediately greeted with a large Hungry Postbox logo placed on the Home page.
</details>

<details><summary>Provide clarity to the user on the purpose of the website.</summary>

- The main title on the home page states the purpose of the website.
- The about us section has a paragraph describing why the website was created and what you need to get started.
- The timeline on the home page gives a simplistic overview of what to expect when engaging in letter writing.
</details>

<details><summary>Display visual feedback to the user based on actions they take on the website.</summary>

- Hover effects on navigation bar menu items, buttons and footer icons.
- Progress bar at the bottom of the registration form.
- Flash messages for when users create an account, delete an account, enter the wrong login details and successfully / unsuccessfully contact a member.
- Materialize form validation.
</details>

## Issues and Bugs during development
___

## Validation
___

The W3C Markup Validator, W3C CSS Validator and JSHint were used to validate my code to ensure no syntax errors were overlooked. My Python code was checked to make sure it met PEP8 standards.

- HTML Validator - PASS
- CSS Validator - PASS
-  JSHint - PASS

## Lighthouse
___

Google lighthouse was ran on every page of the website. Overall I was happy with the result of nearly every page giving back scores between 90 - 100. The home page, profile and member page had some results dip down to 87 - 90 but I'm still happy with the feedback.


## Browser Testing

Hungry Postbox was checked on the latest versions of Microsoft Edge, Google Chrome, Firefox and Safari. The only issues found where with the navigation bar items on Safari which were misaligned. This was resolved and now the site functions well on all the browsers tested.

## Responsive Testing

I used https://www.responsinator.com/ and the chrome extension Responsive Viewer to test Hungry Postbox on a variety of screen sizes and orientations. All tests were successful, with the site retaining its function and design across the different device simulations.