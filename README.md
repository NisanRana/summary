# 📦 Summary

This repository contains the backend and frontend code for the KuraKani. The project is organized into two main components:

- `backend/` – The server-side logic and API
- `frontend/` – A Git submodule that contains the client-side application

---

## 🚀 Cloning This Repository

⚠️ Important: This project uses a Git submodule for the frontend.

To clone the repository **with the frontend included**, use the following command:

`git clone --recurse-submodules https://github.com/NisanRana/summary.git`

If you've already cloned the repository without the submodule, run:

`cd summary
git submodule update --init --recursive`

This will initialize and fetch the contents of the `frontend` submodule.

---

## 📁 Project Structure

summary/
├── backend/          # Backend code (API, logic, etc.)
├── frontend/         # Frontend code as a Git submodule
├── .gitmodules       # Git submodule configuration file
└── README.md         # Project documentation

---

## 🧪 Running the Project

Make sure to install the necessary dependencies for both backend and frontend.

### Backend

`cd backend`
# (Activate your virtual environment if needed)
`pip install -r requirements.txt`
# Run your backend server

### Frontend

`cd frontend
npm install
npm start`

Adjust these commands according to your project setup and frameworks used.

---

## 🛠 Troubleshooting

- Frontend folder is empty after clone  
  Run:
  `git submodule update --init --recursive`

- 403 or authentication error when cloning submodule  
  Make sure the submodule repository is public or that you have access (via SSH or GitHub token if private).

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute as needed.

---

## 👤 Author

Nisan Rana  
GitHub: https://github.com/NisanRana
