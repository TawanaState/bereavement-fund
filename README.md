# Bereavement Fund Django Web App 💻💡

## About the Project

Hi there! 👋 This is a Django web application I initially built for a specific organization, the **Harare Institute of Technology Staff Bereavement Fund**, but now I'm open-sourcing it so others can learn and build from it. 

The app helps manage contributions and payments for a bereavement fund. Members can check their balances and payment history, while trustees get tools to view member details, analyze data, and generate reports. I’ve also focused on making it secure, ensuring sensitive settings are not exposed.

## Key Features 🎯

- **Authentication**: Secure email-based sign-up and login.
- **Member Portal**: Members can view their balances and payment history anytime.
- **Trustee Tools**: Trustees get a dashboard to manage member details, review reports, and perform data analysis.
- **Reports & Analytics**: Visualize data using **Chart.js**—super handy for financial insights.
- **Modern UI**: Built with **TailwindCSS**, so it’s lightweight and looks awesome.
- **Data Security**: Sensitive data like user settings are well-protected.

## Why Open Source?

I believe sharing this project will help others learn Django (and maybe TailwindCSS too!) or even use it as a foundation for their own projects. Dive in, break it, improve it, and make it your own. 🚀

## How to Set It Up 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/bereavement-fund.git
   cd bereavement-fund
   ```

2. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser at `http://127.0.0.1:8000/` to check it out!

## Tech Stack 🛠️

- **Backend**: Python Django (the star of the show 🌟).
- **Frontend**: TailwindCSS for styling—it’s minimal and modern!
- **Charts**: Chart.js for all the analytics goodness.
- **Authentication**: Built-in Django user model with email-based login.

## License 📄

This project is open-source under the MIT License. Use it, tweak it, and share it—it’s all yours! 🎉

---

Thanks for checking out the project! 😊 If you have questions or ideas, feel free to reach out or open an issue. Let’s learn and build cool stuff together! 🚀
